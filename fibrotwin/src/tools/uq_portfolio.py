import copy
import json
from pathlib import Path

import numpy as np
import yaml

from src.tools.validation_portfolio import SCENARIOS, run_one, expected_checks


def sample_cfg(cfg, rng):
    c = copy.deepcopy(cfg)
    # modest uncertainty ranges around calibrated values
    c['cells']['mech_dep_gain'] = float(np.clip(rng.normal(c['cells'].get('mech_dep_gain', 0.7), 0.12), 0.2, 1.4))
    c['cells']['synergy_dep_gain'] = float(np.clip(rng.normal(c['cells'].get('synergy_dep_gain', 1.0), 0.2), 0.2, 2.0))
    c['remodeling']['mech_align_gain'] = float(np.clip(rng.normal(c['remodeling'].get('mech_align_gain', 2.0), 0.3), 0.5, 4.0))
    c['collagen_mixture']['k_maturation'] = float(np.clip(rng.normal(c['collagen_mixture'].get('k_maturation', 0.06), 0.015), 0.01, 0.2))
    c['collagen_mixture']['k_deg_young'] = float(np.clip(rng.normal(c['collagen_mixture'].get('k_deg_young', 0.02), 0.005), 0.002, 0.08))
    c['collagen_mixture']['k_deg_mature'] = float(np.clip(rng.normal(c['collagen_mixture'].get('k_deg_mature', 0.008), 0.002), 0.001, 0.04))
    return c


def q(v, p):
    return float(np.quantile(np.array(v, dtype=float), p))


def main(config_path='configs/mvp_2d_stretch.yaml', n_samples=10, seed=42):
    with open(config_path, 'r') as f:
        base = yaml.safe_load(f)

    rng = np.random.default_rng(seed)
    sample_results = []
    check_pass_rates = {}

    for i in range(n_samples):
        cfg = sample_cfg(base, rng)
        rows = [run_one(cfg, s) for s in SCENARIOS]
        checks = expected_checks(rows)
        sample_results.append({'rows': rows, 'checks': checks})
        for ch in checks:
            key = ch['check']
            check_pass_rates.setdefault(key, []).append(1 if ch['pass'] else 0)

    # aggregate uncertainty by scenario and metric
    scen_names = [s['name'] for s in SCENARIOS]
    agg = {}
    for name in scen_names:
        vals_c, vals_p, vals_a = [], [], []
        for sr in sample_results:
            row = [r for r in sr['rows'] if r['scenario'] == name][0]
            vals_c.append(row['c_mean_final'])
            vals_p.append(row['p_mean_final'])
            vals_a.append(row['ac_align_x_final'])
        agg[name] = {
            'c_mean_final': {'q05': q(vals_c, 0.05), 'q50': q(vals_c, 0.50), 'q95': q(vals_c, 0.95)},
            'p_mean_final': {'q05': q(vals_p, 0.05), 'q50': q(vals_p, 0.50), 'q95': q(vals_p, 0.95)},
            'ac_align_x_final': {'q05': q(vals_a, 0.05), 'q50': q(vals_a, 0.50), 'q95': q(vals_a, 0.95)},
        }

    out = {
        'n_samples': n_samples,
        'scenario_uncertainty': agg,
        'check_pass_probability': {k: float(np.mean(v)) for k, v in check_pass_rates.items()},
        'notes': [
            'Monte Carlo UQ over selected model parameters around calibrated baseline.',
            'q05/q50/q95 summarize uncertainty bands for key outcomes.'
        ],
    }

    p = Path('outputs') / 'uq_portfolio.json'
    p.write_text(json.dumps(out, indent=2))

    md = Path('outputs') / 'uq_portfolio.md'
    lines = ['# UQ Portfolio Summary', '', f"Samples: {n_samples}", '']
    lines.append('## Check pass probabilities')
    for k, v in out['check_pass_probability'].items():
        lines.append(f"- {k}: {v:.2f}")
    lines.append('')
    lines.append('## Scenario uncertainty (q05/q50/q95)')
    for s, m in agg.items():
        lines.append(f"- {s}:")
        lines.append(f"  - c_mean_final: {m['c_mean_final']['q05']:.3f} / {m['c_mean_final']['q50']:.3f} / {m['c_mean_final']['q95']:.3f}")
        lines.append(f"  - p_mean_final: {m['p_mean_final']['q05']:.3f} / {m['p_mean_final']['q50']:.3f} / {m['p_mean_final']['q95']:.3f}")
        lines.append(f"  - ac_align_x_final: {m['ac_align_x_final']['q05']:.3f} / {m['ac_align_x_final']['q50']:.3f} / {m['ac_align_x_final']['q95']:.3f}")
    md.write_text('\n'.join(lines))

    print(json.dumps({'n_samples': n_samples, 'checks': out['check_pass_probability']}, indent=2))


if __name__ == '__main__':
    main()
