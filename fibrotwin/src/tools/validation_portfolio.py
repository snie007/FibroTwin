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
    {"name": "infarct_high_load_high_signal", "stretch_x": 0.28, "tgf_beta": 0.50, "angII": 0.45, "infarct": True},
    {"name": "drug_tgfr_block", "stretch_x": 0.28, "tgf_beta": 0.50, "angII": 0.45, "pharmacology": {"tgfr_block": 0.7, "at1r_block": 0.0}},
    {"name": "drug_at1r_block", "stretch_x": 0.28, "tgf_beta": 0.50, "angII": 0.45, "pharmacology": {"tgfr_block": 0.0, "at1r_block": 0.7}},
    {"name": "drug_dual_block", "stretch_x": 0.28, "tgf_beta": 0.50, "angII": 0.45, "pharmacology": {"tgfr_block": 0.7, "at1r_block": 0.7}},
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
    local.setdefault('infarct', {})['enabled'] = bool(scenario.get('infarct', False))
    pharm = scenario.get('pharmacology', {})
    local.setdefault('pharmacology', {})['tgfr_block'] = pharm.get('tgfr_block', 0.0)
    local.setdefault('pharmacology', {})['at1r_block'] = pharm.get('at1r_block', 0.0)

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

    if local.get('infarct', {}).get('enabled', False):
        cx = local['infarct'].get('center_x', 0.5 * local['mesh']['Lx'])
        cy = local['infarct'].get('center_y', 0.5 * local['mesh']['Ly'])
        rad = local['infarct'].get('radius', 0.2 * min(local['mesh']['Lx'], local['mesh']['Ly']))
        rr = torch.sqrt((nodes[:, 0] - cx) ** 2 + (nodes[:, 1] - cy) ** 2)
        core = rr <= rad
        border = (rr > rad) & (rr <= 2.0 * rad)
        remote = rr > 2.0 * rad
        c_core = float(fields.c[core].mean().item()) if core.any() else None
        c_remote = float(fields.c[remote].mean().item()) if remote.any() else None
        metrics.update({
            'c_core': c_core,
            'c_border': float(fields.c[border].mean().item()) if border.any() else None,
            'c_remote': c_remote,
            'p_core': float(fields.p[core].mean().item()) if core.any() else None,
            'p_border': float(fields.p[border].mean().item()) if border.any() else None,
            'p_remote': float(fields.p[remote].mean().item()) if remote.any() else None,
            'core_to_remote_ratio': (c_core / max(c_remote, 1e-8)) if (c_core is not None and c_remote is not None) else None,
            'disp_core': float(fields.scar_dispersion[core].mean().item()) if core.any() else None,
            'disp_border': float(fields.scar_dispersion[border].mean().item()) if border.any() else None,
            'disp_remote': float(fields.scar_dispersion[remote].mean().item()) if remote.any() else None,
        })
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
        'check': 'high_load_high_signal yields highest collagen among non-infarct baseline/mech/signal scenarios',
        'pass': by['high_load_high_signal']['c_mean_final'] >= max(by[k]['c_mean_final'] for k in ['baseline_low_load_low_signal','high_load_only','high_signal_only']),
    })
    if 'infarct_high_load_high_signal' in by:
        checks.append({
            'check': 'infarct core collagen exceeds non-infarct high_load_high_signal global collagen',
            'pass': by['infarct_high_load_high_signal'].get('c_core', 0.0) > by['high_load_high_signal']['c_mean_final'],
        })
    if 'drug_tgfr_block' in by:
        checks.append({
            'check': 'TGFβR blockade reduces profibrotic signal vs high_load_high_signal',
            'pass': by['drug_tgfr_block']['p_mean_final'] < by['high_load_high_signal']['p_mean_final'],
        })
    if 'drug_at1r_block' in by:
        checks.append({
            'check': 'AT1R blockade reduces collagen vs high_load_high_signal',
            'pass': by['drug_at1r_block']['c_mean_final'] < by['high_load_high_signal']['c_mean_final'],
        })
    if 'drug_dual_block' in by:
        checks.append({
            'check': 'Dual blockade gives strongest suppression (collagen) among drug scenarios',
            'pass': by['drug_dual_block']['c_mean_final'] <= min(by['drug_tgfr_block']['c_mean_final'], by['drug_at1r_block']['c_mean_final']),
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
