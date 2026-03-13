import json
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[2]


def main():
    cat = json.loads((ROOT / 'outputs' / 'systematic_test_catalog.json').read_text())
    tests = cat.get('tests', [])

    strict_path = ROOT / 'data' / 'calibration' / 'paper_targets_strict.yaml'
    existing = yaml.safe_load(strict_path.read_text()) if strict_path.exists() else {}
    strict_tests = existing.get('strict_tests', {})
    unanchored = existing.get('unanchored_tests', {})

    for t in tests:
        tid = t.get('id')
        if tid in strict_tests:
            continue
        if tid not in unanchored:
            unanchored[tid] = {'reason': 'pending full-paper manual quantitative curation'}

    out = {
        'version': 1,
        'policy': [
            'Hard anchors only: numeric endpoints explicitly reported in paper results/figures/tables.',
            'No template bands and no inferred placeholders.',
            'If no hard anchor is available, test stays unanchored.'
        ],
        'strict_tests': strict_tests,
        'unanchored_tests': dict(sorted(unanchored.items(), key=lambda kv: kv[0]))
    }

    strict_path.write_text(yaml.safe_dump(out, sort_keys=False))

    report = {
        'n_total_tests': len(tests),
        'n_strict_anchored': len(strict_tests),
        'n_unanchored': len(unanchored),
    }
    (ROOT / 'outputs' / 'strict_curation_progress.json').write_text(json.dumps(report, indent=2))
    (ROOT / 'outputs' / 'strict_curation_progress.md').write_text(
        f"# Strict Curation Progress\n\n- Total tests: {report['n_total_tests']}\n- Strict anchored: {report['n_strict_anchored']}\n- Unanchored: {report['n_unanchored']}\n"
    )
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
