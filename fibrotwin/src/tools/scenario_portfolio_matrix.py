import copy
import json
from pathlib import Path

import yaml

from src.tools.validation_portfolio import run_one


LOADS = [0.10, 0.20, 0.30]
SIGNALS = [(0.05, 0.05), (0.25, 0.20), (0.50, 0.45)]
FIBS = [40, 80, 140]


def main(config_path='configs/mvp_2d_stretch.yaml'):
    with open(config_path, 'r') as f:
        base = yaml.safe_load(f)

    rows = []
    for load in LOADS:
        for tgf, ang in SIGNALS:
            for nf in FIBS:
                scenario = {
                    'name': f'L{load:.2f}_T{tgf:.2f}_A{ang:.2f}_N{nf}',
                    'stretch_x': load,
                    'tgf_beta': tgf,
                    'angII': ang,
                    'infarct': False,
                }
                c = copy.deepcopy(base)
                c['cells']['n_agents'] = nf
                r = run_one(c, scenario)
                rows.append(r)

    # add infarct stress tests
    for nf in [80, 140]:
        scenario = {
            'name': f'INFARCT_L0.28_T0.50_A0.45_N{nf}',
            'stretch_x': 0.28,
            'tgf_beta': 0.50,
            'angII': 0.45,
            'infarct': True,
        }
        c = copy.deepcopy(base)
        c['cells']['n_agents'] = nf
        rows.append(run_one(c, scenario))

    out = {
        'n_scenarios': len(rows),
        'scenarios': rows,
        'summary': {
            'max_collagen': max(r['c_mean_final'] for r in rows),
            'min_collagen': min(r['c_mean_final'] for r in rows),
            'max_alignment': max(r['ac_align_x_final'] for r in rows),
            'min_alignment': min(r['ac_align_x_final'] for r in rows),
        }
    }

    p = Path('outputs') / 'scenario_portfolio_matrix.json'
    p.write_text(json.dumps(out, indent=2))

    md = Path('outputs') / 'scenario_portfolio_matrix.md'
    lines = ['# Scenario Portfolio Matrix', '', f"Scenarios: {len(rows)}", '']
    lines.append('## Key ranges')
    lines.append(f"- Collagen: {out['summary']['min_collagen']:.3f} .. {out['summary']['max_collagen']:.3f}")
    lines.append(f"- Alignment: {out['summary']['min_alignment']:.3f} .. {out['summary']['max_alignment']:.3f}")
    lines.append('')
    lines.append('## Scenarios')
    for r in rows:
        lines.append(f"- {r['scenario']}: c={r['c_mean_final']:.3f}, p={r['p_mean_final']:.3f}, myo={r['myo_frac_final']:.3f}, ac_align={r['ac_align_x_final']:.3f}")
    md.write_text('\n'.join(lines))

    print(json.dumps({'n_scenarios': len(rows), 'summary': out['summary']}, indent=2))


if __name__ == '__main__':
    main()
