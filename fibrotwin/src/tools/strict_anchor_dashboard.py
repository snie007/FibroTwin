import json
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[2]


def main():
    cand = json.loads((ROOT / 'outputs' / 'strict_anchor_candidates.json').read_text()) if (ROOT / 'outputs' / 'strict_anchor_candidates.json').exists() else {'n_candidates': 0, 'candidates': []}
    app = yaml.safe_load((ROOT / 'data' / 'calibration' / 'paper_targets_strict_approved.yaml').read_text()) if (ROOT / 'data' / 'calibration' / 'paper_targets_strict_approved.yaml').exists() else {'approved': {}, 'rejected': {}}
    strict = json.loads((ROOT / 'outputs' / 'quantitative_match_strict.json').read_text()) if (ROOT / 'outputs' / 'quantitative_match_strict.json').exists() else {'n_strict_anchored': 0, 'counts': {}}

    out = {
        'candidate_count': cand.get('n_candidates', 0),
        'approved_count': len(app.get('approved', {})),
        'rejected_count': len(app.get('rejected', {})),
        'strict_scored_count': strict.get('n_strict_anchored', 0),
        'strict_counts': strict.get('counts', {}),
    }
    (ROOT / 'outputs' / 'strict_anchor_dashboard.json').write_text(json.dumps(out, indent=2))

    md = [
        '# Strict Anchor Yield Dashboard', '',
        f"- Candidates found: {out['candidate_count']}",
        f"- Approved anchors: {out['approved_count']}",
        f"- Rejected anchors: {out['rejected_count']}",
        f"- Strict scored tests: {out['strict_scored_count']}",
        f"- Strict counts: {out['strict_counts']}"
    ]
    (ROOT / 'outputs' / 'strict_anchor_dashboard.md').write_text('\n'.join(md))
    print(json.dumps(out, indent=2))


if __name__ == '__main__':
    main()
