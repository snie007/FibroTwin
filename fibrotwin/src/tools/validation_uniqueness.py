import json
from pathlib import Path
from collections import defaultdict


def norm(s):
    return ' '.join(str(s or '').lower().replace('-', ' ').replace('_', ' ').split())


def signature(t):
    # uniqueness key by study intent: PMID + category + expected statement
    return (str(t.get('pmid', '')), norm(t.get('category', '')), norm(t.get('expected', '')))


def main(inp='outputs/systematic_test_catalog.json'):
    p = Path(inp)
    if not p.exists():
        raise SystemExit('systematic_test_catalog.json missing')
    d = json.loads(p.read_text())
    tests = d.get('tests', [])

    groups = defaultdict(list)
    for t in tests:
        groups[signature(t)].append(t)

    duplicate_groups = {k: v for k, v in groups.items() if len(v) > 1}

    # create unique representative list (keep first by id sort)
    unique_tests = []
    duplicate_map = []
    for k, vv in groups.items():
        vv_sorted = sorted(vv, key=lambda x: x.get('id', ''))
        keep = vv_sorted[0]
        unique_tests.append(keep)
        if len(vv_sorted) > 1:
            duplicate_map.append({
                'signature': {'pmid': k[0], 'category': k[1], 'expected': k[2]},
                'kept': keep.get('id'),
                'merged_ids': [x.get('id') for x in vv_sorted[1:]],
                'n_group': len(vv_sorted),
            })

    unique_tests = sorted(unique_tests, key=lambda x: x.get('id', ''))

    out = {
        'n_original': len(tests),
        'n_unique': len(unique_tests),
        'n_duplicate_groups': len(duplicate_groups),
        'duplicate_groups': duplicate_map,
        'unique_tests': unique_tests,
    }
    Path('outputs/validation_uniqueness.json').write_text(json.dumps(out, indent=2))

    # publish reduced catalog for site use
    reduced = dict(d)
    reduced['tests'] = unique_tests
    reduced['n_tests'] = len(unique_tests)
    Path('outputs/systematic_test_catalog_unique.json').write_text(json.dumps(reduced, indent=2))

    lines = [
        '# Validation Uniqueness Report',
        '',
        f"- Original tests: {len(tests)}",
        f"- Unique tests: {len(unique_tests)}",
        f"- Duplicate groups: {len(duplicate_groups)}",
        '',
        '## Duplicate groups merged'
    ]
    if duplicate_map:
        for g in duplicate_map[:200]:
            lines.append(f"- PMID {g['signature']['pmid']} | {g['signature']['category']} | kept {g['kept']} | merged {g['merged_ids']}")
    else:
        lines.append('- None detected.')

    Path('outputs/validation_uniqueness.md').write_text('\n'.join(lines))
    print(json.dumps({'n_original': len(tests), 'n_unique': len(unique_tests), 'n_duplicate_groups': len(duplicate_groups)}, indent=2))


if __name__ == '__main__':
    main()
