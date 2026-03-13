import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

NUM = re.compile(r"\b\d+(?:\.\d+)?\b")
RANGE = re.compile(r"\b(\d+(?:\.\d+)?)\s*(?:to|-|–)\s*(\d+(?:\.\d+)?)\b")

RESULT_WORDS = ['increase', 'decrease', 'higher', 'lower', 'reduced', 'elevated', 'upregulated', 'downregulated', 'compared', 'versus', 'vs']
ENDPOINT_WORDS = ['collagen', 'fibrosis', 'scar', 'smad', 'erk', 'myofibro', 'alignment', 'infarct', 'core', 'remote', 'border']


def comparator_from_text(txt):
    s = txt.lower()
    if '%' in s or 'percent' in s:
        return 'percent'
    if 'fold' in s or ' x' in s:
        return 'fold'
    if RANGE.search(s):
        return 'range'
    return 'absolute'


def plausible(snippet):
    s = snippet.lower()
    if not any(w in s for w in RESULT_WORDS):
        return False
    if not any(w in s for w in ENDPOINT_WORDS):
        return False
    if not NUM.search(s):
        return False
    if any(b in s for b in ['orcid', 'doi', 'pmc', 'issn', 'telephone', 'fax', 'copyright']):
        return False
    return True


def main():
    qe = json.loads((ROOT / 'outputs' / 'quantitative_evidence.json').read_text())
    cat = json.loads((ROOT / 'outputs' / 'systematic_test_catalog.json').read_text())
    cby = {t['id']: t for t in cat.get('tests', [])}

    rows = []
    for t in qe.get('tests', []):
        tid = t.get('id')
        for q in t.get('quantitative_mentions', []):
            sn = q.get('snippet', '')
            if not plausible(sn):
                continue
            rows.append({
                'id': tid,
                'pmid': t.get('pmid'),
                'pmcid': t.get('pmcid'),
                'category': cby.get(tid, {}).get('category'),
                'paper_title': t.get('title'),
                'value': q.get('value'),
                'endpoint_guess': q.get('endpoint_guess'),
                'comparator_suggested': comparator_from_text(sn),
                'snippet': sn,
                'status': 'candidate',
            })

    out = {'n_candidates': len(rows), 'candidates': rows}
    (ROOT / 'outputs' / 'strict_anchor_candidates.json').write_text(json.dumps(out, indent=2))

    md = ['# Strict Anchor Candidates', '', f"- Candidates found: {len(rows)}", '', 'Use paper_targets_strict_approved.yaml to accept/reject these candidates.']
    (ROOT / 'outputs' / 'strict_anchor_candidates.md').write_text('\n'.join(md))
    print(json.dumps({'n_candidates': len(rows)}, indent=2))


if __name__ == '__main__':
    main()
