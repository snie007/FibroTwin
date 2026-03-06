import copy
import json
from pathlib import Path

import torch
import yaml

from src.mechanics.mesh import create_rect_tri_mesh
from src.sim.fields import init_fields
from src.cells.agents import init_agents
from src.sim.io import make_run_dir, log_line
from src.sim.time_integrator import run_sim


SCENARIOS = [
    {"name": "baseline_low_load_low_signal", "stretch_x": 0.10, "tgf_beta": 0.05, "angII": 0.05},
    {"name": "high_load_only", "stretch_x": 0.28, "tgf_beta": 0.05, "angII": 0.05},
    {"name": "high_signal_only", "stretch_x": 0.10, "tgf_beta": 0.50, "angII": 0.45},
    {"name": "high_load_high_signal", "stretch_x": 0.28, "tgf_beta": 0.50, "angII": 0.45},
]


def run_one(cfg, scenario):
    local = copy.deepcopy(cfg)
    local['time']['n_steps'] = 140
    local['mesh']['nx'] = min(local['mesh']['nx'], 10)
    local['mesh']['ny'] = min(local['mesh']['ny'], 5)
    local.setdefault('viz', {})['enable'] = False
    local['viz']['frame_every'] = 10**9
    local['mechanics']['model'] = 'linear'  # fast screening portfolio; Ogden kept for production runs

    local['mechanics']['stretch_x'] = scenario['stretch_x']
    local.setdefault('signaling', {})['tgf_beta'] = scenario['tgf_beta']
    local.setdefault('signaling', {})['angII'] = scenario['angII']

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    torch.manual_seed(local['seed'])

    out_dir = make_run_dir(local['output_root'])
    log_line(out_dir, f"scenario={scenario['name']}")

    nodes, elems = create_rect_tri_mesh(local['mesh']['Lx'], local['mesh']['Ly'], local['mesh']['nx'], local['mesh']['ny'], device=device)
    fields = init_fields(nodes.shape[0], device=device, seed=local['seed'])
    agents = init_agents(local['cells']['n_agents'], local['mesh']['Lx'], local['mesh']['Ly'], device=device, seed=local['seed'])

    fields, agents = run_sim(local, nodes, elems, fields, agents, out_dir)

    metrics = {
        'scenario': scenario['name'],
        'stretch_x': scenario['stretch_x'],
        'tgf_beta': scenario['tgf_beta'],
        'angII': scenario['angII'],
        'c_mean_final': float(fields.c.mean().item()),
        'p_mean_final': float(fields.p.mean().item()),
        'myo_frac_final': float(agents.is_myofibro.float().mean().item()),
        'ac_align_x_final': float(torch.abs(fields.ac[:, 0]).mean().item()),
        'run_dir': out_dir,
    }
    return metrics


def expected_checks(rows):
    by = {r['scenario']: r for r in rows}
    checks = []
    # Qualitative checks inspired by fibroblast signaling literature + mechanobiology
    checks.append({
        'check': 'high_signal_only has higher profibrotic signal than baseline',
        'pass': by['high_signal_only']['p_mean_final'] > by['baseline_low_load_low_signal']['p_mean_final'],
    })
    checks.append({
        'check': 'high_signal_only has higher myofibroblast fraction than baseline',
        'pass': by['high_signal_only']['myo_frac_final'] > by['baseline_low_load_low_signal']['myo_frac_final'],
    })
    checks.append({
        'check': 'high_load_only increases fibre alignment vs baseline',
        'pass': by['high_load_only']['ac_align_x_final'] > by['baseline_low_load_low_signal']['ac_align_x_final'],
    })
    checks.append({
        'check': 'high_load_high_signal yields highest collagen among scenarios',
        'pass': by['high_load_high_signal']['c_mean_final'] == max(r['c_mean_final'] for r in rows),
    })
    return checks


def main(config_path='configs/mvp_2d_stretch.yaml'):
    with open(config_path, 'r') as f:
        cfg = yaml.safe_load(f)

    rows = [run_one(cfg, s) for s in SCENARIOS]
    checks = expected_checks(rows)

    out = {
        'scenarios': rows,
        'checks': checks,
        'n_checks_passed': sum(int(c['pass']) for c in checks),
        'n_checks_total': len(checks),
        'notes': [
            'These are qualitative validation checks against expected trends from fibroblast signaling + load interactions, not full quantitative calibration.',
            'Mismatch cases indicate targets for reparameterization or richer signaling network dynamics.'
        ]
    }

    p = Path('outputs') / 'validation_portfolio.json'
    p.write_text(json.dumps(out, indent=2))
    md = Path('outputs') / 'validation_portfolio.md'
    lines = ['# Validation Portfolio', '', f"Checks passed: {out['n_checks_passed']}/{out['n_checks_total']}", '']
    lines.append('## Scenario outcomes')
    for r in rows:
        lines.append(f"- {r['scenario']}: c={r['c_mean_final']:.3f}, p={r['p_mean_final']:.3f}, myo={r['myo_frac_final']:.3f}, ac_align_x={r['ac_align_x_final']:.3f}")
    lines.append('')
    lines.append('## Checks')
    for c in checks:
        lines.append(f"- [{'PASS' if c['pass'] else 'FAIL'}] {c['check']}")
    md.write_text('\n'.join(lines))

    print(json.dumps(out, indent=2))


if __name__ == '__main__':
    main()
