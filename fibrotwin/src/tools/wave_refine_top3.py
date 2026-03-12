import copy
import json
from pathlib import Path

import numpy as np
import yaml

from src.tools.validation_portfolio import run_one

ROOT = Path(__file__).resolve().parents[2]
TOP3 = [
    ('signaling_network', 'd_smad'),
    ('cells', 'myo_switch_threshold'),
    ('signaling_network', 'k_at1r_erk'),
]


def set_params(cfg, vals):
    c = copy.deepcopy(cfg)
    for (sec, key), v in vals.items():
        c.setdefault(sec, {})[key] = float(v)
    return c


def eval6(cfg):
    tg = yaml.safe_load((ROOT / 'data' / 'calibration' / 'targets.yaml').read_text())['targets']
    bands = {
        'myofibro_fraction_high_signal': tg['fibroblast_signaling']['myofibro_fraction_high_signal'],
        'profibrotic_index_high_signal': tg['fibroblast_signaling']['profibrotic_index_high_signal'],
        'alignment_high_load': tg['growth_remodeling']['alignment_high_load'],
        'collagen_fraction_load_signal': tg['growth_remodeling']['collagen_fraction_load_signal'],
        'infarct_core_collagen': tg['infarct_remodeling']['infarct_core_collagen'],
        'infarct_core_to_remote_ratio': tg['infarct_remodeling']['core_to_remote_ratio'],
    }
    hs = run_one(cfg, {'name': 'high_signal_only', 'stretch_x': 0.10, 'tgf_beta': 0.50, 'angII': 0.45})
    hl = run_one(cfg, {'name': 'high_load_only', 'stretch_x': 0.28, 'tgf_beta': 0.05, 'angII': 0.05})
    hls = run_one(cfg, {'name': 'high_load_high_signal', 'stretch_x': 0.28, 'tgf_beta': 0.50, 'angII': 0.45})
    inf = run_one(cfg, {'name': 'infarct_high_load_high_signal', 'stretch_x': 0.28, 'tgf_beta': 0.50, 'angII': 0.45, 'infarct': True})

    vals = {
        'myofibro_fraction_high_signal': float(hs['myo_frac_final']),
        'profibrotic_index_high_signal': float(hs['p_mean_final']),
        'alignment_high_load': float(hl['ac_align_x_final']),
        'collagen_fraction_load_signal': float(hls['c_mean_final']),
        'infarct_core_collagen': float(inf.get('c_core', 0.0)),
        'infarct_core_to_remote_ratio': float(inf.get('core_to_remote_ratio', 0.0)),
    }
    passes = {k: bool(bands[k][0] <= vals[k] <= bands[k][1]) for k in vals}
    n = sum(int(v) for v in passes.values())
    return vals, passes, n


def main(n_samples=70, spread=0.2, seed=55):
    rng = np.random.default_rng(seed)
    cfg = yaml.safe_load((ROOT / 'configs' / 'mvp_2d_stretch.yaml').read_text())

    base = { (s,k): float(cfg.get(s, {}).get(k)) for s,k in TOP3 }
    rows = []
    for i in range(n_samples):
        vals = {}
        for s,k in TOP3:
            b = base[(s,k)]
            lo = b * (1.0 - spread)
            hi = b * (1.0 + spread)
            vals[(s,k)] = rng.uniform(lo, hi)
        c = set_params(cfg, vals)
        v, p, n = eval6(c)
        rows.append({
            'i': i,
            'params': {f'{s}.{k}': float(vals[(s,k)]) for s,k in TOP3},
            'metrics': v,
            'passes': p,
            'pass_count': int(n),
        })

    best = sorted(rows, key=lambda r: r['pass_count'], reverse=True)[:10]
    out = {'n_samples': n_samples, 'top3_params': [f'{s}.{k}' for s,k in TOP3], 'best': best}
    (ROOT / 'outputs' / 'wave_refine_top3.json').write_text(json.dumps(out, indent=2))

    lines = ['# Top-3 Parameter Local Refinement', '', f'- Samples: {n_samples}', f"- Top parameters: {', '.join(out['top3_params'])}", '', '## Best candidates']
    for b in best[:5]:
        lines.append(f"- sample {b['i']}: pass {b['pass_count']}/6, params={b['params']}")
    (ROOT / 'outputs' / 'wave_refine_top3.md').write_text('\n'.join(lines))
    print(json.dumps({'best_pass': best[0]['pass_count'] if best else 0}, indent=2))


if __name__ == '__main__':
    main()
