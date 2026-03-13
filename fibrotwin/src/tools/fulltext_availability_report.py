import json
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[2]


def main():
    qe = json.loads((ROOT / 'outputs' / 'quantitative_evidence.json').read_text())
    cat = json.loads((ROOT / 'outputs' / 'systematic_test_catalog.json').read_text())
    strict = yaml.safe_load((ROOT / 'data' / 'calibration' / 'paper_targets_strict_approved.yaml').read_text())

    approved = set((strict.get('approved') or {}).keys())
    qby = {t['id']: t for t in qe.get('tests', [])}

    rows = []
    for t in cat.get('tests', []):
        tid = t['id']
        q = qby.get(tid, {})
        rows.append({
            'id': tid,
            'pmid': t.get('pmid'),
            'title': t.get('title'),
            'strict_approved': tid in approved,
            'pmcid': q.get('pmcid'),
            'has_fulltext_extraction': bool(q.get('has_fulltext_extraction')),
            'fulltext_route': q.get('fulltext_route'),
            'n_numeric_mentions': q.get('n_numeric_mentions', 0),
        })

    out = {
        'n_total': len(rows),
        'n_strict_approved': sum(int(r['strict_approved']) for r in rows),
        'n_with_pmcid': sum(int(bool(r['pmcid'])) for r in rows),
        'n_with_fulltext_extraction': sum(int(r['has_fulltext_extraction']) for r in rows),
        'rows': rows,
    }
    (ROOT / 'outputs' / 'fulltext_availability_report.json').write_text(json.dumps(out, indent=2))

    md = [
        '# Fulltext Availability Report', '',
        f"- Total tests: {out['n_total']}",
        f"- Strict approved tests: {out['n_strict_approved']}",
        f"- With PMCID: {out['n_with_pmcid']}",
        f"- With fulltext extraction: {out['n_with_fulltext_extraction']}",
    ]
    (ROOT / 'outputs' / 'fulltext_availability_report.md').write_text('\n'.join(md))
    print(json.dumps({k: out[k] for k in ['n_total','n_strict_approved','n_with_pmcid','n_with_fulltext_extraction']}, indent=2))


if __name__ == '__main__':
    main()
