import json
from pathlib import Path
from collections import Counter, defaultdict

ROOT = Path(__file__).resolve().parents[2]


def norm(s):
    return ' '.join(str(s or '').lower().replace('-', ' ').replace('_', ' ').split())


def main(inp='outputs/systematic_test_catalog_unique.json'):
    p = ROOT / inp
    if not p.exists():
        p = ROOT / 'outputs' / 'systematic_test_catalog.json'
    d = json.loads(p.read_text())
    tests = d.get('tests', [])

    cat_counts = Counter(t.get('category', 'unknown') for t in tests)

    # intent = expected statement template + category
    intents = defaultdict(list)
    for t in tests:
        iid = f"{t.get('category','unknown')}::{norm(t.get('expected',''))}"
        intents[iid].append(t)

    intent_rows = []
    for i, (iid, arr) in enumerate(sorted(intents.items(), key=lambda kv: len(kv[1]), reverse=True), start=1):
        intent_rows.append({
            'intent_id': f'I{i:03d}',
            'category': arr[0].get('category', 'unknown'),
            'expected_template': arr[0].get('expected', ''),
            'n_studies': len(arr),
            'study_ids': [x.get('id') for x in arr],
            'pmids': [x.get('pmid') for x in arr],
        })

    out = {
        'n_studies': len(tests),
        'n_domains': len(cat_counts),
        'domain_counts': dict(cat_counts),
        'n_intents': len(intent_rows),
        'intent_rows': intent_rows,
    }
    (ROOT / 'outputs' / 'validation_coverage.json').write_text(json.dumps(out, indent=2))

    lines = [
        '# Validation Coverage Matrix Summary',
        '',
        f"- Studies (PMID-linked tests): {out['n_studies']}",
        f"- Model domains: {out['n_domains']}",
        f"- Distinct validation intents (mechanism/observable templates): {out['n_intents']}",
        '',
        '## Why 80 studies but few domains?',
        'Domains are broad model modules (e.g., infarct_remodeling, fibroblast_signaling).',
        'Each study is linked to one domain and one intent template. Multiple studies can support the same mechanistic intent.',
        '',
        '## Domain distribution',
        '| Domain | N studies |',
        '|---|---:|',
    ]
    for k, v in sorted(cat_counts.items(), key=lambda kv: kv[1], reverse=True):
        lines.append(f'| {k} | {v} |')

    lines += ['', '## Intent coverage (top)', '| Intent ID | Domain | N studies | Expected template |', '|---|---|---:|---|']
    for r in intent_rows[:20]:
        lines.append(f"| {r['intent_id']} | {r['category']} | {r['n_studies']} | {r['expected_template']} |")

    lines += ['', '## Interpretation', '- Uniqueness should be read at the **study record** level and **intent ID** level.', '- If many studies map to the same intent, this is evidence depth, not new mechanism breadth.', '- To increase mechanism breadth, add new intent templates and corresponding simulation protocols.']

    (ROOT / 'outputs' / 'validation_coverage.md').write_text('\n'.join(lines))
    print(json.dumps({'n_studies': out['n_studies'], 'n_domains': out['n_domains'], 'n_intents': out['n_intents']}, indent=2))


if __name__ == '__main__':
    main()
