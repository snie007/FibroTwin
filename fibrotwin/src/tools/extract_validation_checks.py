import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

RANGE_RE = re.compile(r"(\d+(?:\.\d+)?)\s*(?:to|-|–)\s*(\d+(?:\.\d+)?)")
NUM_RE = re.compile(r"\d+(?:\.\d+)?")


def infer_comparator(value, snippet, category):
    s = (snippet or '').lower()
    v = (value or '').lower()
    if category == 'infarct_remodeling' and ('core' in s and 'remote' in s):
        if '%' in v or 'percent' in s:
            return 'core_vs_remote_percent'
        if 'fold' in s or ' x' in s:
            return 'core_vs_remote_fold'
        return 'core_absolute'
    if '%' in v or 'percent' in s:
        return 'percent'
    if 'fold' in s or ' x' in s:
        return 'fold'
    return 'absolute'


def infer_band(value, comparator):
    s = (value or '').lower()
    m = RANGE_RE.search(s)
    if m:
        a, b = float(m.group(1)), float(m.group(2))
        return [min(a, b), max(a, b)]
    n = NUM_RE.search(s)
    if not n:
        return None
    x = float(n.group(0))
    if comparator in ('percent', 'core_vs_remote_percent'):
        return [0.8 * x, 1.2 * x]
    if comparator in ('fold', 'core_vs_remote_fold'):
        return [0.8 * x, 1.2 * x]
    return [0.8 * x, 1.2 * x]


def high_signal(snippet):
    s = (snippet or '').lower()
    bad = ['orcid', 'issn', 'doi', 'telephone', 'fax', 'copyright', 'pmc']
    if any(b in s for b in bad):
        return False
    has_endpoint = any(k in s for k in ['collagen', 'fibrosis', 'scar', 'smad', 'erk', 'myofibro', 'alignment', 'infarct'])
    has_comp = any(k in s for k in ['increase', 'decrease', 'higher', 'lower', 'compared', 'versus', 'vs', 'fold', '%'])
    return has_endpoint and has_comp


def main(max_per_test=2):
    se = json.loads((ROOT / 'outputs' / 'schema_extract_report.json').read_text())
    cat = json.loads((ROOT / 'outputs' / 'systematic_test_catalog.json').read_text())
    cby = {t['id']: t for t in cat.get('tests', [])}

    checks = []
    for row in se.get('rows', []):
        tid = row.get('id')
        category = row.get('category')
        pmid = cby.get(tid, {}).get('pmid')
        picked = 0
        for m in row.get('schema_matched', []):
            if picked >= max_per_test:
                break
            val = m.get('value')
            sn = m.get('snippet', '')
            if not high_signal(sn):
                continue
            comp = infer_comparator(val, sn, category)
            band = infer_band(val, comp)
            if not band:
                continue
            checks.append({
                'id': tid,
                'pmid': pmid,
                'category': category,
                'comparator': comp,
                'paper_value': val,
                'target_band': [round(band[0], 4), round(band[1], 4)],
                'snippet': sn,
                'provenance': 'auto_from_fulltext_schema_match',
                'confidence': 'screening',
            })
            picked += 1

    out = {
        'n_checks': len(checks),
        'checks': checks,
        'notes': [
            'Auto-extracted quantitative validation checks from schema-matched fulltext snippets.',
            'These are screening-level candidates and require manual approval before strict scoring.'
        ]
    }
    (ROOT / 'outputs' / 'extracted_validation_checks.json').write_text(json.dumps(out, indent=2))

    lines = ['# Extracted Quantitative Validation Checks', '', f"- Checks extracted: {len(checks)}", '', 'Screening-level auto-extraction; manual approval required.']
    (ROOT / 'outputs' / 'extracted_validation_checks.md').write_text('\n'.join(lines))
    print(json.dumps({'n_checks': len(checks)}, indent=2))


if __name__ == '__main__':
    main()
