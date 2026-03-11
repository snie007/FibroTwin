import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def review(iteration=1):
    html = (ROOT / 'site' / 'pages' / 'validation.html').read_text()
    h2 = re.findall(r'<h2>(.*?)</h2>', html)
    norm = [re.sub(r'\s+', ' ', x.strip().lower()) for x in h2]
    dup = sorted(set([x for x in norm if norm.count(x) > 1]))

    has_shells = all(x in html for x in ['1) Model QA', '2) Core validation outcomes', '3) Method QA', '4) Coverage and evidence'])
    no_legacy = all(x not in html for x in ['03 — Validation and Sanity Checks', '04 — Systematic Improvement Review', '05 — Validation Gap'])
    human_names = ('Load 0.' in html) or ('Baseline (low load + low signal)' in html)

    out = {
        'iteration': iteration,
        'n_h2': len(h2),
        'duplicate_h2_normalized': dup,
        'has_unified_section_shells': has_shells,
        'removed_legacy_appendix_cards': no_legacy,
        'human_readable_scenario_labels_present': human_names,
        'consistency_score_0_4': int(has_shells) + int(no_legacy) + int(human_names) + int(len(dup) <= 1),
    }
    p = ROOT / 'outputs' / f'validation_consistency_review_iter{iteration}.json'
    p.write_text(json.dumps(out, indent=2))
    return out


def main():
    all_out = []
    for i in range(1, 5):
        all_out.append(review(i))
    (ROOT / 'outputs' / 'validation_consistency_review.json').write_text(json.dumps({'iterations': all_out}, indent=2))

    lines = ['# Validation Consistency Review (4-pass loop)', '']
    for o in all_out:
        lines += [
            f"## Iteration {o['iteration']}",
            f"- Consistency score: {o['consistency_score_0_4']}/4",
            f"- Unified shells: {o['has_unified_section_shells']}",
            f"- Legacy appendix removed: {o['removed_legacy_appendix_cards']}",
            f"- Human scenario labels: {o['human_readable_scenario_labels_present']}",
            f"- Duplicate headings: {o['duplicate_h2_normalized']}",
            ''
        ]
    (ROOT / 'outputs' / 'validation_consistency_review.md').write_text('\n'.join(lines))
    print(json.dumps({'final_score': all_out[-1]['consistency_score_0_4']}, indent=2))


if __name__ == '__main__':
    main()
