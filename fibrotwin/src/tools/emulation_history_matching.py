import copy
import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import torch
import yaml

from autoemulate.core.compare import AutoEmulate
from autoemulate.calibration.history_matching import HistoryMatching

from src.tools.validation_portfolio import run_one

ROOT = Path(__file__).resolve().parents[2]

PARAMS = [
    ('signaling_network', 'k_tgfr_smad'),
    ('signaling_network', 'k_at1r_erk'),
    ('signaling_network', 'd_smad'),
    ('signaling_network', 'd_erk'),
    ('infarct', 'collagen_source'),
    ('infarct', 'signal_source'),
]


def bands_from_registry():
    reg = yaml.safe_load((ROOT / 'data' / 'calibration' / 'parameter_registry.yaml').read_text())
    out = []
    for sec, key in PARAMS:
        k = f'{sec}.{key}'
        b = reg['parameters'][k]['literature_band']
        out.append((float(b[0]), float(b[1])))
    return out


def set_params(cfg, x):
    c = copy.deepcopy(cfg)
    for (sec, key), v in zip(PARAMS, x):
        c.setdefault(sec, {})[key] = float(v)
    return c


def eval_targets(cfg):
    hs = run_one(cfg, {'name': 'high_signal_only', 'stretch_x': 0.10, 'tgf_beta': 0.50, 'angII': 0.45})
    inf = run_one(cfg, {'name': 'infarct_high_load_high_signal', 'stretch_x': 0.28, 'tgf_beta': 0.50, 'angII': 0.45, 'infarct': True})
    return [float(hs['myo_frac_final']), float(hs['p_mean_final']), float(inf.get('core_to_remote_ratio', 0.0))]


def main(config_path='configs/mvp_2d_stretch.yaml', n_train=20, n_candidates=300, seed=7):
    rng = np.random.default_rng(seed)
    cfg = yaml.safe_load((ROOT / config_path).read_text())
    bounds = bands_from_registry()

    X = []
    Y = []
    for _ in range(n_train):
        x = [rng.uniform(lo, hi) for lo, hi in bounds]
        y = eval_targets(set_params(cfg, x))
        X.append(x)
        Y.append(y)

    X = np.asarray(X, dtype=np.float32)
    Y = np.asarray(Y, dtype=np.float32)

    n_test = max(4, n_train // 4)
    Xtr, Ytr = X[:-n_test], Y[:-n_test]
    Xte, Yte = X[-n_test:], Y[-n_test:]

    ae = AutoEmulate(Xtr, Ytr, test_data=(Xte, Yte), n_iter=5, n_splits=3, n_bootstraps=None, random_seed=seed, log_level='error')
    best = ae.best_result('r2')

    Xc = np.asarray([[rng.uniform(lo, hi) for lo, hi in bounds] for _ in range(n_candidates)], dtype=np.float32)
    Xc_t = torch.tensor(Xc)
    mean_t, var_t = best.model.predict_mean_and_variance(Xc_t)
    if var_t is None:
        # fallback variance from test residuals
        pred_te = best.model.predict_mean(torch.tensor(Xte)).detach().cpu().numpy()
        resid = np.var(Yte - pred_te, axis=0, keepdims=True) + 1e-4
        var_t = torch.tensor(np.repeat(resid, Xc.shape[0], axis=0), dtype=torch.float32)

    tg = yaml.safe_load((ROOT / 'data' / 'calibration' / 'targets.yaml').read_text())['targets']
    obs = {
        'myofibro_fraction_high_signal': (np.mean(tg['fibroblast_signaling']['myofibro_fraction_high_signal']), (0.5*(tg['fibroblast_signaling']['myofibro_fraction_high_signal'][1]-tg['fibroblast_signaling']['myofibro_fraction_high_signal'][0]))**2),
        'profibrotic_index_high_signal': (np.mean(tg['fibroblast_signaling']['profibrotic_index_high_signal']), (0.5*(tg['fibroblast_signaling']['profibrotic_index_high_signal'][1]-tg['fibroblast_signaling']['profibrotic_index_high_signal'][0]))**2),
        'infarct_core_to_remote_ratio': (np.mean(tg['infarct_remodeling']['core_to_remote_ratio']), (0.5*(tg['infarct_remodeling']['core_to_remote_ratio'][1]-tg['infarct_remodeling']['core_to_remote_ratio'][0]))**2),
    }

    hm = HistoryMatching(obs, threshold=3.0, model_discrepancy=0.01, rank=1)
    I = hm.calculate_implausibility(mean_t, var_t)
    nroy_idx = hm.get_nroy(I)
    nroy_x = Xc_t[nroy_idx]
    nroy_frac = float(len(nroy_idx) / max(len(Xc), 1))

    new_bounds = hm.generate_param_bounds(nroy_x, param_names=[f'{a}.{b}' for a, b in PARAMS])

    out = {
        'n_train': int(n_train),
        'n_candidates': int(n_candidates),
        'best_model': best.model_name,
        'best_r2_test': float(best.test_metrics[next(iter(best.test_metrics))][0]),
        'nroy_count': int(len(nroy_idx)),
        'nroy_fraction': nroy_frac,
        'nroy_bounds': new_bounds,
    }
    (ROOT / 'outputs' / 'emulation_report.json').write_text(json.dumps(out, indent=2))

    lines = [
        '# Emulation + History Matching Report',
        '',
        f"- Training runs: {out['n_train']}",
        f"- Candidate parameter points evaluated by emulator: {out['n_candidates']}",
        f"- Best emulator: {out['best_model']}",
        f"- NROY count: {out['nroy_count']} ({100*out['nroy_fraction']:.1f}%)",
        '',
        '## Plausible parameter-space bounds (NROY envelope)',
    ]
    if new_bounds:
        for k, b in new_bounds.items():
            lines.append(f"- {k}: [{b[0]:.4g}, {b[1]:.4g}]")
    else:
        lines.append('- No NROY bounds identified (all points ruled out or insufficient samples).')
    (ROOT / 'outputs' / 'emulation_report.md').write_text('\n'.join(lines))

    plt.figure(figsize=(6.2, 3.8))
    maxI = I.max(dim=1).values.detach().cpu().numpy()
    plt.hist(maxI, bins=28, color='#2563eb', alpha=0.85)
    plt.axvline(3.0, color='crimson', linestyle='--', label='implausibility threshold')
    plt.xlabel('Max implausibility score')
    plt.ylabel('Count')
    plt.title('History matching: implausibility distribution')
    plt.legend()
    (ROOT / 'site' / 'assets' / 'img').mkdir(parents=True, exist_ok=True)
    plt.tight_layout(); plt.savefig(ROOT / 'site' / 'assets' / 'img' / 'emulation_implausibility_hist.png', dpi=220); plt.close()

    print(json.dumps(out, indent=2))


if __name__ == '__main__':
    main()
