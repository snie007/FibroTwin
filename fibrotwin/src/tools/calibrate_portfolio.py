import copy
import json
from pathlib import Path

import yaml

from src.tools.validation_portfolio import run_one, SCENARIOS, expected_checks


def main(config_path='configs/mvp_2d_stretch.yaml'):
    with open(config_path, 'r') as f:
        cfg = yaml.safe_load(f)

    grid = []
    for mech_dep in [0.7, 1.0]:
        for synergy in [1.0, 1.5]:
            for mech_align in [2.0, 3.0]:
                c = copy.deepcopy(cfg)
                c['cells']['mech_dep_gain'] = mech_dep
                c['cells']['synergy_dep_gain'] = synergy
                c['remodeling']['mech_align_gain'] = mech_align
                rows = [run_one(c, s) for s in SCENARIOS]
                checks = expected_checks(rows)
                score = sum(int(ch['pass']) for ch in checks)
                grid.append({
                    'params': {'mech_dep_gain': mech_dep, 'synergy_dep_gain': synergy, 'mech_align_gain': mech_align},
                    'score': score,
                    'rows': rows,
                    'checks': checks,
                })

    best = max(grid, key=lambda g: g['score'])
    out = {
        'best_score': best['score'],
        'best_params': best['params'],
        'best_checks': best['checks'],
        'best_rows': best['rows'],
    }
    p = Path('outputs') / 'calibration_portfolio.json'
    p.write_text(json.dumps(out, indent=2))
    print(json.dumps(out, indent=2))


if __name__ == '__main__':
    main()
