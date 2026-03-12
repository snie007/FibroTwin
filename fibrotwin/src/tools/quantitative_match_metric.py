import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

RANGE_RE = re.compile(r"(\d+(?:\.\d+)?)\s*(?:to|-|–)\s*(\d+(?:\.\d+)?)")
NUM_RE = re.compile(r"\d+(?:\.\d+)?")


def parse_anchor(value: str):
    v = (value or '').lower().strip()
    # observation-layer guardrails: skip p-values and pure time/dose anchors
    if 'p <' in v or 'p<' in v or 'p=' in v:
        return None
    if any(u in v for u in ['day', 'days', 'week', 'weeks', 'month', 'months', 'year', 'years', 'hour', 'hours', 'min']) and ('%' not in v and 'fold' not in v):
        return None
    if any(u in v for u in ['mg', 'ug', 'μg', 'ng', 'pg']) and ('%' not in v and 'fold' not in v):
        return None

    m = RANGE_RE.search(v)
    if m:
        a, b = float(m.group(1)), float(m.group(2))
        return {'kind': 'range', 'band': [min(a, b), max(a, b)], 'raw': value}
    n = NUM_RE.search(v)
    if not n:
        return None
    x = float(n.group(0))
    if '%' in v or 'percent' in v:
        return {'kind': 'percent', 'target': x, 'band': [0.8 * x, 1.2 * x], 'raw': value}
    if 'fold' in v or v.endswith('x') or ' x' in v:
        return {'kind': 'fold', 'target': x, 'band': [0.8 * x, 1.2 * x], 'raw': value}
    return {'kind': 'absolute', 'target': x, 'band': [0.8 * x, 1.2 * x], 'raw': value}


def choose_anchor(test, category):
    mentions = test.get('quantitative_mentions', [])
    pref = {
        'infarct_remodeling': {'infarct zoning', 'collagen/fibrosis'},
        'fibroblast_signaling': {'signaling pathway', 'myofibroblast activation'},
        'collagen_dynamics': {'collagen/fibrosis'},
        'growth_remodeling': {'alignment/anisotropy'},
    }.get(category, set())

    best = None
    best_score = -1
    for q in mentions:
        p = parse_anchor(q.get('value', ''))
        if not p:
            continue
        s = 0
        if q.get('endpoint_guess') in pref:
            s += 3
        if p['kind'] in ('percent', 'fold', 'range'):
            s += 2
        if p['kind'] == 'absolute':
            s += 1
        if s > best_score:
            best_score = s
            best = {'parsed': p, 'mention': q}
    return best


def model_value_for_category(cat, vp_by):
    base = vp_by.get('baseline_low_load_low_signal', {})
    hs = vp_by.get('high_signal_only', {})
    hl = vp_by.get('high_load_only', {})
    hls = vp_by.get('high_load_high_signal', {})
    inf = vp_by.get('infarct_high_load_high_signal', {})

    if cat == 'infarct_remodeling':
        c_remote = inf.get('c_remote')
        c_core = inf.get('c_core')
        if c_remote and c_core is not None:
            pct = 100.0 * (c_core - c_remote) / max(abs(c_remote), 1e-8)
            fold = c_core / max(c_remote, 1e-8)
            return {'percent': pct, 'fold': fold, 'absolute': c_core}
    if cat == 'fibroblast_signaling':
        b = base.get('p_mean_final')
        x = hs.get('p_mean_final')
        if b and x is not None:
            pct = 100.0 * (x - b) / max(abs(b), 1e-8)
            fold = x / max(b, 1e-8)
            return {'percent': pct, 'fold': fold, 'absolute': x}
    if cat == 'collagen_dynamics':
        b = base.get('c_mean_final')
        x = hls.get('c_mean_final')
        if b and x is not None:
            pct = 100.0 * (x - b) / max(abs(b), 1e-8)
            fold = x / max(b, 1e-8)
            return {'percent': pct, 'fold': fold, 'absolute': x}
    if cat == 'growth_remodeling':
        b = base.get('ac_align_x_final')
        x = hl.get('ac_align_x_final')
        if b is not None and x is not None:
            pct = 100.0 * (x - b) / max(abs(b), 1e-8)
            fold = x / max(b, 1e-8)
            return {'percent': pct, 'fold': fold, 'absolute': x}
    return None


def classify(model_v, band):
    lo, hi = band
    if lo <= model_v <= hi:
        return 'PASS', 0.0
    width = max(hi - lo, 1e-8)
    dist = (lo - model_v) if model_v < lo else (model_v - hi)
    nerr = dist / width
    if nerr <= 0.5:
        return 'PARTIAL', nerr
    return 'FAIL', nerr


def main():
    qe = json.loads((ROOT / 'outputs' / 'quantitative_evidence.json').read_text())
    cat = json.loads((ROOT / 'outputs' / 'systematic_test_catalog.json').read_text())
    vp = json.loads((ROOT / 'outputs' / 'validation_portfolio.json').read_text())

    cat_by_id = {t['id']: t for t in cat.get('tests', [])}
    vp_by = {r['scenario']: r for r in vp.get('scenarios', [])}

    rows = []
    for t in qe.get('tests', []):
        tid = t.get('id')
        if t.get('n_numeric_mentions', 0) <= 0:
            continue
        meta = cat_by_id.get(tid, {})
        category = meta.get('category', '')
        anchor = choose_anchor(t, category)
        model = model_value_for_category(category, vp_by)
        if not anchor or not model:
            rows.append({'id': tid, 'category': category, 'status': 'UNMAPPED'})
            continue
        p = anchor['parsed']
        model_v = model.get(p['kind'], model.get('absolute'))
        status, nerr = classify(float(model_v), p['band'])
        rows.append({
            'id': tid,
            'category': category,
            'status': status,
            'normalized_error': float(nerr),
            'paper_anchor': anchor['mention'].get('value'),
            'paper_band': p['band'],
            'model_value': float(model_v),
            'kind': p['kind'],
        })

    counts = {'PASS': 0, 'PARTIAL': 0, 'FAIL': 0, 'UNMAPPED': 0}
    for r in rows:
        counts[r['status']] = counts.get(r['status'], 0) + 1

    out = {
        'n_with_numeric_mentions': len(rows),
        'counts': counts,
        'rows': rows,
        'metric_definition': 'PASS if model value within inferred paper anchor band; PARTIAL if normalized distance to band <= 0.5; else FAIL. UNMAPPED if no valid anchor-model mapping.',
    }
    (ROOT / 'outputs' / 'quantitative_match_report.json').write_text(json.dumps(out, indent=2))

    md = [
        '# Quantitative Match Report', '',
        f"- Tests evaluated (with numeric mentions): {out['n_with_numeric_mentions']}",
        f"- PASS: {counts['PASS']}",
        f"- PARTIAL: {counts['PARTIAL']}",
        f"- FAIL: {counts['FAIL']}",
        f"- UNMAPPED: {counts['UNMAPPED']}", '',
        out['metric_definition']
    ]
    (ROOT / 'outputs' / 'quantitative_match_report.md').write_text('\n'.join(md))
    print(json.dumps({'evaluated': out['n_with_numeric_mentions'], **counts}, indent=2))


if __name__ == '__main__':
    main()
