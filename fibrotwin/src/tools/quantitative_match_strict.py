import json
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]


def model_vals(cat, vp):
    b = vp.get('baseline_low_load_low_signal', {})
    hs = vp.get('high_signal_only', {})
    hl = vp.get('high_load_only', {})
    hls = vp.get('high_load_high_signal', {})
    inf = vp.get('infarct_high_load_high_signal', {})
    out = {}
    if cat == 'infarct_remodeling' and inf.get('c_remote'):
        cr, cc = inf['c_remote'], inf['c_core']
        out['fold'] = cc / max(cr, 1e-8)
        out['absolute'] = cc
        out['percent'] = 100.0 * (cc - cr) / max(abs(cr), 1e-8)
    elif cat == 'fibroblast_signaling' and b.get('p_mean_final'):
        x0, x1 = b['p_mean_final'], hs['p_mean_final']
        out['fold'] = x1 / max(x0, 1e-8)
        out['absolute'] = x1
        out['percent'] = 100.0 * (x1 - x0) / max(abs(x0), 1e-8)
    elif cat == 'collagen_dynamics' and b.get('c_mean_final'):
        x0, x1 = b['c_mean_final'], hls['c_mean_final']
        out['fold'] = x1 / max(x0, 1e-8)
        out['absolute'] = x1
        out['percent'] = 100.0 * (x1 - x0) / max(abs(x0), 1e-8)
    elif cat == 'growth_remodeling' and b.get('ac_align_x_final') is not None:
        x0, x1 = b['ac_align_x_final'], hl['ac_align_x_final']
        out['fold'] = x1 / max(x0, 1e-8)
        out['absolute'] = x1
        out['percent'] = 100.0 * (x1 - x0) / max(abs(x0), 1e-8)
    return out


def main():
    strict_path = ROOT / 'data' / 'calibration' / 'paper_targets_strict.yaml'
    st = yaml.safe_load(strict_path.read_text()) if strict_path.exists() else {'strict_tests': {}}
    strict_tests = st.get('strict_tests', {})

    cat = json.loads((ROOT / 'outputs' / 'systematic_test_catalog.json').read_text())
    cat_by = {t['id']: t for t in cat.get('tests', [])}
    vp = json.loads((ROOT / 'outputs' / 'validation_portfolio.json').read_text())
    vp_by = {r['scenario']: r for r in vp.get('scenarios', [])}

    rows = []
    for tid, cfg in strict_tests.items():
        meta = cat_by.get(tid, {})
        c = meta.get('category', '')
        m = model_vals(c, vp_by)
        comp = cfg.get('comparator', 'absolute')
        band = cfg.get('band', [None, None])
        mv = m.get(comp)
        if mv is None or band[0] is None:
            rows.append({'id': tid, 'status': 'UNAVAILABLE_MODEL_COMPARATOR'})
            continue
        stt = 'PASS' if band[0] <= mv <= band[1] else 'FAIL'
        rows.append({
            'id': tid,
            'pmid': cfg.get('pmid'),
            'category': c,
            'status': stt,
            'comparator': comp,
            'paper_band': band,
            'model_value': float(mv),
            'endpoint': cfg.get('endpoint'),
            'source_excerpt': cfg.get('source_excerpt'),
            'source_level': cfg.get('source_level'),
        })

    counts = {'PASS': 0, 'FAIL': 0, 'UNAVAILABLE_MODEL_COMPARATOR': 0}
    for r in rows:
        counts[r['status']] = counts.get(r['status'], 0) + 1

    out = {
        'n_strict_anchored': len(rows),
        'counts': counts,
        'rows': rows,
        'n_unanchored_declared': len(st.get('unanchored_tests', {})),
        'definition': 'Strict hard-anchored mode: only manually curated paper-reported quantitative endpoints are scored.',
    }
    (ROOT / 'outputs' / 'quantitative_match_strict.json').write_text(json.dumps(out, indent=2))

    lines = [
        '# Strict Paper-Anchored Match', '',
        f"- Strict anchored tests scored: {out['n_strict_anchored']}",
        f"- PASS: {counts['PASS']}",
        f"- FAIL: {counts['FAIL']}",
        f"- Unavailable comparator: {counts['UNAVAILABLE_MODEL_COMPARATOR']}",
        f"- Declared unanchored tests (current batch): {out['n_unanchored_declared']}",
        '',
        out['definition']
    ]
    (ROOT / 'outputs' / 'quantitative_match_strict.md').write_text('\n'.join(lines))
    print(json.dumps({'n_strict_anchored': out['n_strict_anchored'], 'counts': counts}, indent=2))


if __name__ == '__main__':
    main()
