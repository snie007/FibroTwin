import copy
import json
from pathlib import Path

import numpy as np
import torch
import yaml

from autoemulate.calibration.history_matching import HistoryMatching
from autoemulate.core.compare import AutoEmulate
from src.tools.validation_portfolio import run_one

ROOT = Path(__file__).resolve().parents[2]
PARAMS = [
    ('signaling_network', 'k_tgfr_smad'), ('signaling_network', 'k_at1r_erk'),
    ('signaling_network', 'd_smad'), ('signaling_network', 'd_erk'),
    ('cells', 'myo_switch_threshold'), ('cells', 'myo_switch_softness'), ('cells', 'myo_cap'),
    ('infarct', 'collagen_source'), ('infarct', 'signal_source'),
    ('infarct', 'dispersion_core'), ('infarct', 'dispersion_border'), ('infarct', 'dispersion_remote'),
]


def set_params(cfg, x):
    c = copy.deepcopy(cfg)
    for (sec, key), v in zip(PARAMS, x):
        c.setdefault(sec, {})[key] = float(v)
    return c


def eval_targets(cfg):
    hs = run_one(cfg, {'name': 'high_signal_only', 'stretch_x': 0.10, 'tgf_beta': 0.50, 'angII': 0.45})
    hl = run_one(cfg, {'name': 'high_load_only', 'stretch_x': 0.28, 'tgf_beta': 0.05, 'angII': 0.05})
    hls = run_one(cfg, {'name': 'high_load_high_signal', 'stretch_x': 0.28, 'tgf_beta': 0.50, 'angII': 0.45})
    inf = run_one(cfg, {'name': 'infarct_high_load_high_signal', 'stretch_x': 0.28, 'tgf_beta': 0.50, 'angII': 0.45, 'infarct': True})
    return np.array([
        hs['myo_frac_final'], hs['p_mean_final'], hl['ac_align_x_final'],
        hls['c_mean_final'], inf.get('c_core', 0.0), inf.get('core_to_remote_ratio', 0.0)
    ], dtype=np.float32)


def get_obs_and_bands():
    tg = yaml.safe_load((ROOT / 'data' / 'calibration' / 'targets.yaml').read_text())['targets']
    bands = {
        'myofibro_fraction_high_signal': tg['fibroblast_signaling']['myofibro_fraction_high_signal'],
        'profibrotic_index_high_signal': tg['fibroblast_signaling']['profibrotic_index_high_signal'],
        'alignment_high_load': tg['growth_remodeling']['alignment_high_load'],
        'collagen_fraction_load_signal': tg['growth_remodeling']['collagen_fraction_load_signal'],
        'infarct_core_collagen': tg['infarct_remodeling']['infarct_core_collagen'],
        'infarct_core_to_remote_ratio': tg['infarct_remodeling']['core_to_remote_ratio'],
    }
    obs = {k: (float(np.mean(v)), float((0.5*(v[1]-v[0]))**2)) for k,v in bands.items()}
    return obs, bands


def main(n_waves=3, n_train=18, n_candidates=350, seed=17):
    rng = np.random.default_rng(seed)
    cfg = yaml.safe_load((ROOT / 'configs' / 'mvp_2d_stretch.yaml').read_text())
    reg = yaml.safe_load((ROOT / 'data' / 'calibration' / 'parameter_registry.yaml').read_text())
    bounds = {}
    for s, k in PARAMS:
        kk = f'{s}.{k}'
        if kk in reg.get('parameters', {}):
            bounds[kk] = tuple(reg['parameters'][kk]['literature_band'])
        else:
            v = float(cfg.get(s, {}).get(k, 1.0))
            bounds[kk] = (0.5 * v, 1.5 * v if v != 0 else 1.0)

    obs, bands = get_obs_and_bands()
    waves = []

    for w in range(1, n_waves+1):
        X, Y = [], []
        keys = list(bounds.keys())
        for _ in range(n_train):
            x = [rng.uniform(*bounds[k]) for k in keys]
            y = eval_targets(set_params(cfg, x))
            X.append(x); Y.append(y)
        X = np.asarray(X, dtype=np.float32); Y = np.asarray(Y, dtype=np.float32)
        n_test = max(2, n_train // 5)
        train_n = X.shape[0] - n_test
        n_splits = min(3, max(2, train_n - 1))
        ae = AutoEmulate(
            X[:-n_test],
            Y[:-n_test],
            test_data=(X[-n_test:], Y[-n_test:]),
            models=['GaussianProcessRBF', 'GaussianProcessMatern32', 'PolynomialRegression'],
            n_iter=4,
            n_splits=n_splits,
            n_bootstraps=None,
            random_seed=seed+w,
            log_level='error',
        )
        best = ae.best_result('r2')

        Xc = np.asarray([[rng.uniform(*bounds[k]) for k in keys] for _ in range(n_candidates)], dtype=np.float32)
        mean_t, var_t = best.model.predict_mean_and_variance(torch.tensor(Xc))
        if var_t is None:
            pred_te = best.model.predict_mean(torch.tensor(X[-n_test:])).detach().cpu().numpy()
            resid = np.var(Y[-n_test:] - pred_te, axis=0, keepdims=True) + 1e-4
            var_t = torch.tensor(np.repeat(resid, Xc.shape[0], axis=0), dtype=torch.float32)

        hm = HistoryMatching(obs, threshold=3.0, model_discrepancy=0.01, rank=1)
        I = hm.calculate_implausibility(mean_t, var_t)
        nroy_idx = hm.get_nroy(I)
        nroy_x = torch.tensor(Xc)[nroy_idx]
        nroy_frac = float(len(nroy_idx)/max(len(Xc),1))

        newb = hm.generate_param_bounds(nroy_x, param_names=keys) if len(nroy_idx) > 0 else None
        if newb:
            bounds = {k: (float(v[0]), float(v[1])) for k,v in newb.items()}

        # evaluate best NROY candidate in simulator
        maxI = I.max(dim=1).values.detach().cpu().numpy()
        if len(nroy_idx) > 0:
            idx = int(nroy_idx.detach().cpu().numpy()[np.argmin(maxI[nroy_idx.detach().cpu().numpy()])])
        else:
            idx = int(np.argmin(maxI))
        ybest = eval_targets(set_params(cfg, Xc[idx]))
        pass_flags = []
        for i,k in enumerate(bands.keys()):
            lo, hi = bands[k]
            pass_flags.append(bool(lo <= float(ybest[i]) <= hi))

        waves.append({
            'wave': w,
            'best_model': best.model_name,
            'nroy_fraction': nroy_frac,
            'nroy_count': int(len(nroy_idx)),
            'n_candidates': int(n_candidates),
            'targets_passed': int(sum(pass_flags)),
            'targets_total': 6,
            'sim_targets': {k: float(ybest[i]) for i,k in enumerate(bands.keys())},
            'pass_flags': {k: bool(pass_flags[i]) for i,k in enumerate(bands.keys())},
            'bounds': bounds,
        })

    out = {'waves': waves, 'final_bounds': bounds}
    (ROOT / 'outputs' / 'emulation_waves.json').write_text(json.dumps(out, indent=2))

    lines = ['# Emulation History-Matching Waves', '']
    for w in waves:
        lines += [f"## Wave {w['wave']}", f"- Best emulator: {w['best_model']}", f"- NROY: {w['nroy_count']}/{w['n_candidates']} ({100*w['nroy_fraction']:.1f}%)", f"- Full-simulator pass count: {w['targets_passed']}/{w['targets_total']}", '']
    lines += ['## Final bounds']
    for k,v in bounds.items():
        lines.append(f'- {k}: [{v[0]:.4g}, {v[1]:.4g}]')
    (ROOT / 'outputs' / 'emulation_waves.md').write_text('\n'.join(lines))
    print(json.dumps({'n_waves': n_waves, 'final_pass': waves[-1]['targets_passed']}, indent=2))


if __name__ == '__main__':
    main()
