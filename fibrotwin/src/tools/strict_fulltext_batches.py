import json
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[2]


def main(batch_index=1, batch_size=10):
    qe = json.loads((ROOT / 'outputs' / 'quantitative_evidence.json').read_text())
    strict = yaml.safe_load((ROOT / 'data' / 'calibration' / 'paper_targets_strict_approved.yaml').read_text())
    approved = set((strict.get('approved') or {}).keys())
    rejected = set((strict.get('rejected') or {}).keys())

    rows = []
    for t in qe.get('tests', []):
        tid = t.get('id')
        if tid in approved or tid in rejected:
            continue
        if not t.get('has_fulltext_extraction'):
            continue
        rows.append({
            'id': tid,
            'pmid': t.get('pmid'),
            'pmcid': t.get('pmcid'),
            'title': t.get('title'),
            'n_numeric_mentions': t.get('n_numeric_mentions', 0),
            'fulltext_route': t.get('fulltext_route'),
            'top_mentions': [m.get('value') for m in (t.get('quantitative_mentions') or [])[:6]],
        })

    rows.sort(key=lambda r: r['n_numeric_mentions'], reverse=True)
    total = len(rows)
    start = (batch_index - 1) * batch_size
    end = start + batch_size
    batch = rows[start:end]

    out = {
        'batch_index': batch_index,
        'batch_size': batch_size,
        'n_fulltext_unreviewed': total,
        'rows': batch,
    }

    (ROOT / 'outputs' / f'strict_fulltext_batch_{batch_index:02d}.json').write_text(json.dumps(out, indent=2))
    lines = [
        f"# Strict Fulltext Batch {batch_index:02d}",
        '',
        f"- Unreviewed fulltext-accessible tests: {total}",
        f"- This batch size: {len(batch)}",
        ''
    ]
    for r in batch:
        lines.append(f"- {r['id']} | PMID {r['pmid']} | mentions={r['n_numeric_mentions']} | route={r['fulltext_route']}")
    (ROOT / 'outputs' / f'strict_fulltext_batch_{batch_index:02d}.md').write_text('\n'.join(lines))

    print(json.dumps({'n_fulltext_unreviewed': total, 'batch_items': len(batch)}, indent=2))


if __name__ == '__main__':
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument('--batch-index', type=int, default=1)
    ap.add_argument('--batch-size', type=int, default=10)
    args = ap.parse_args()
    main(batch_index=args.batch_index, batch_size=args.batch_size)
