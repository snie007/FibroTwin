import json
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[2]


def main(batch_size=10):
    strict = yaml.safe_load((ROOT / 'data' / 'calibration' / 'paper_targets_strict.yaml').read_text())
    un = strict.get('unanchored_tests', {})
    qe = json.loads((ROOT / 'outputs' / 'quantitative_evidence.json').read_text())
    cat = json.loads((ROOT / 'outputs' / 'systematic_test_catalog.json').read_text())
    qe_by = {t['id']: t for t in qe.get('tests', [])}
    cat_by = {t['id']: t for t in cat.get('tests', [])}

    # prioritize tests with fulltext + numeric mentions
    candidates = []
    for tid in sorted(un.keys()):
        q = qe_by.get(tid, {})
        c = cat_by.get(tid, {})
        score = int(bool(q.get('has_fulltext_extraction'))) * 2 + int(q.get('n_numeric_mentions', 0) > 0)
        candidates.append((score, q.get('n_numeric_mentions', 0), tid, q, c))
    candidates.sort(key=lambda x: (x[0], x[1]), reverse=True)

    batch = candidates[:batch_size]
    rows = []
    for _, _, tid, q, c in batch:
        rows.append({
            'id': tid,
            'pmid': c.get('pmid'),
            'pmcid': q.get('pmcid'),
            'title': c.get('title'),
            'category': c.get('category'),
            'pubmed_url': c.get('pubmed_url'),
            'pmc_url': f"https://pmc.ncbi.nlm.nih.gov/articles/{q.get('pmcid')}/" if q.get('pmcid') else None,
            'n_numeric_mentions': q.get('n_numeric_mentions', 0),
            'source_level': 'fulltext' if q.get('has_fulltext_extraction') else 'abstract',
        })

    out = {'batch_size': batch_size, 'rows': rows}
    (ROOT / 'outputs' / 'strict_batch_01.json').write_text(json.dumps(out, indent=2))

    md = ['# Strict Curation Batch 01', '', f"- Items: {len(rows)}", '']
    for r in rows:
        md.append(f"- {r['id']} | PMID {r['pmid']} | {r['category']} | mentions={r['n_numeric_mentions']} | source={r['source_level']}")
        if r.get('pmc_url'):
            md.append(f"  - PMC: {r['pmc_url']}")
        if r.get('pubmed_url'):
            md.append(f"  - PubMed: {r['pubmed_url']}")
    (ROOT / 'outputs' / 'strict_batch_01.md').write_text('\n'.join(md))
    print(json.dumps({'batch_items': len(rows)}, indent=2))


if __name__ == '__main__':
    main()
