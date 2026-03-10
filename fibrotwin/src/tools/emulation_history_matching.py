import copy
import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import torch
import yaml

from autoemulate.calibration.history_matching import HistoryMatching
from autoemulate.core.compare import AutoEmulate

from src.tools.validation_portfolio import run_one

ROOT = Path(__file__).resolve().parents[2]

# Expanded parameter set for scaled emulation
PARAMS = [
    ('signaling_network', 'k_tgfr_smad'),
    ('signaling_network', 'k_at1r_erk'),
    ('signaling_network', 'd_smad'),
    ('signaling_network', 'd_erk'),
    ('cells', 'myo_switch_threshold'),
    ('cells', 'myo_switch_softness'),
    ('cells', 'myo_cap'),
    ('infarct', 'collagen_source'),
    ('infarct', 'signal_source'),
    ('infarct', 'dispersion_core'),
    ('infarct', 'dispersion_border'),
    ('infarct', 'dispersion_remote'),
]


def bands_from_registry():
    reg = yaml.safe_load((ROOT / 'data' / 'calibration' / 'parameter_registry.yaml').read_text())
    out = []
    for sec, key in PARAMS:
        k = f'{sec}.{key}'
        if k in reg.get('parameters', {}):
            b = reg['parameters'][k]['literature_band']
            out.append((float(b[0]), float(b[1])))
        else:
            # fallback around current config value
            cfg = yaml.safe_load((ROOT / 'configs' / 'mvp_2d_stretch.yaml').read_text())
            v = float(cfg.get(sec, {}).get(key, 1.0))
            out.append((0.5 * v, 1.5 * v if v != 0 else 1.0))
    return out


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
    return [
        float(hs['myo_frac_final']),
        float(hs['p_mean_final']),
        float(hl['ac_align_x_final']),
        float(hls['c_mean_final']),
        float(inf.get('c_core', 0.0)),
        float(inf.get('core_to_remote_ratio', 0.0)),
    ]


def target_obs_from_yaml():
    tg = yaml.safe_load((ROOT / 'data' / 'calibration' / 'targets.yaml').read_text())['targets']
    bands = {
        'myofibro_fraction_high_signal': tg['fibroblast_signaling']['myofibro_fraction_high_signal'],
        'profibrotic_index_high_signal': tg['fibroblast_signaling']['profibrotic_index_high_signal'],
        'alignment_high_load': tg['growth_remodeling']['alignment_high_load'],
        'collagen_fraction_load_signal': tg['growth_remodeling']['collagen_fraction_load_signal'],
        'infarct_core_collagen': tg['infarct_remodeling']['infarct_core_collagen'],
        'infarct_core_to_remote_ratio': tg['infarct_remodeling']['core_to_remote_ratio'],
    }
    obs = {k: (float(np.mean(v)), float((0.5 * (v[1] - v[0])) ** 2)) for k, v in bands.items()}
    return bands, obs


def in_band(y, bands):
    keys = list(bands.keys())
    flags = []
    for i, k in enumerate(keys):
        lo, hi = bands[k]
        flags.append(bool(lo <= float(y[i]) <= hi))
    return flags


def main(config_path='configs/mvp_2d_stretch.yaml', n_train=60, n_candidates=2000, seed=11):
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

    n_test = max(8, n_train // 5)
    Xtr, Ytr = X[:-n_test], Y[:-n_test]
    Xte, Yte = X[-n_test:], Y[-n_test:]

    ae = AutoEmulate(
        Xtr,
        Ytr,
        test_data=(Xte, Yte),
        n_iter=8,
        n_splits=4,
        n_bootstraps=None,
        random_seed=seed,
        log_level='error',
        evaluation_metrics=['r2', 'rmse'],
    )
    best = ae.best_result('r2')

    Xc = np.asarray([[rng.uniform(lo, hi) for lo, hi in bounds] for _ in range(n_candidates)], dtype=np.float32)
    Xc_t = torch.tensor(Xc)
    mean_t, var_t = best.model.predict_mean_and_variance(Xc_t)
    if var_t is None:
        pred_te = best.model.predict_mean(torch.tensor(Xte)).detach().cpu().numpy()
        resid = np.var(Yte - pred_te, axis=0, keepdims=True) + 1e-4
        var_t = torch.tensor(np.repeat(resid, Xc.shape[0], axis=0), dtype=torch.float32)

    bands, obs = target_obs_from_yaml()
    hm = HistoryMatching(obs, threshold=3.0, model_discrepancy=0.01, rank=1)
    I = hm.calculate_implausibility(mean_t, var_t)
    nroy_idx = hm.get_nroy(I)
    nroy_x = Xc_t[nroy_idx]
    nroy_frac = float(len(nroy_idx) / max(len(Xc), 1))

    new_bounds = hm.generate_param_bounds(nroy_x, param_names=[f'{a}.{b}' for a, b in PARAMS])

    # pick best plausible candidate by minimal max implausibility and evaluate true simulator
    maxI = I.max(dim=1).values.detach().cpu().numpy()
    if len(nroy_idx) > 0:
        nroy_np_idx = nroy_idx.detach().cpu().numpy()
        best_idx = int(nroy_np_idx[np.argmin(maxI[nroy_np_idx])])
    else:
        best_idx = int(np.argmin(maxI))
    best_x = Xc[best_idx]
    best_cfg = set_params(cfg, best_x)
    best_y = eval_targets(best_cfg)
    flags = in_band(best_y, bands)

    out = {
        'n_train': int(n_train),
        'n_candidates': int(n_candidates),
        'best_model': best.model_name,
        'nroy_count': int(len(nroy_idx)),
        'nroy_fraction': nroy_frac,
        'nroy_bounds': new_bounds,
        'best_candidate': {
            'params': {f'{a}.{b}': float(v) for (a, b), v in zip(PARAMS, best_x)},
            'simulated_metrics': {
                'myofibro_fraction_high_signal': best_y[0],
                'profibrotic_index_high_signal': best_y[1],
                'alignment_high_load': best_y[2],
                'collagen_fraction_load_signal': best_y[3],
                'infarct_core_collagen': best_y[4],
                'infarct_core_to_remote_ratio': best_y[5],
            },
            'target_pass_flags': {
                k: bool(v) for k, v in zip(list(bands.keys()), flags)
            },
            'n_targets_passed': int(sum(flags)),
            'n_targets_total': 6,
        },
    }
    (ROOT / 'outputs' / 'emulation_report.json').write_text(json.dumps(out, indent=2))

    lines = [
        '# Emulation + History Matching Report',
        '',
        f"- Training runs: {out['n_train']}",
        f"- Candidate points screened by emulator: {out['n_candidates']}",
        f"- Best emulator: {out['best_model']}",
        f"- NROY count: {out['nroy_count']} ({100*out['nroy_fraction']:.1f}%)",
        '',
        '## Best plausible candidate (checked in full simulator)',
        f"- Targets passed: {out['best_candidate']['n_targets_passed']}/{out['best_candidate']['n_targets_total']}",
    ]
    for k, v in out['best_candidate']['simulated_metrics'].items():
        lo, hi = bands[k]
        ok = out['best_candidate']['target_pass_flags'][k]
        lines.append(f"- {k}: {v:.4f} vs [{lo}, {hi}] -> {'PASS' if ok else 'FAIL'}")

    lines += ['', '## Plausible parameter-space bounds (NROY envelope)']
    if new_bounds:
        for k, b in new_bounds.items():
            lines.append(f"- {k}: [{b[0]:.4g}, {b[1]:.4g}]")

    lines += [
        '',
        '## History matching usage guidance',
        '1. Start with broad physically credible parameter bounds and a small training design (20-40).',
        '2. Fit emulator and inspect predictive quality (R2/RMSE). If poor, add design points.',
        '3. Define observations as target means + uncertainty variances from literature bands.',
        '4. Compute implausibility and NROY region; do not trust single-wave NROY blindly.',
        '5. Iterate waves: sample within NROY, run simulator, refit emulator, shrink bounds.',
        '6. QC at each wave: emulator accuracy on holdout, NROY fraction trend, and simulator re-check of selected NROY points.',
    ]

    (ROOT / 'outputs' / 'emulation_report.md').write_text('\n'.join(lines))

    qc = [
        '# Emulation QC Checklist',
        '',
        '- [ ] Training design covers full parameter ranges (no collapsed dimensions).',
        '- [ ] Emulator holdout metrics acceptable (R2 not strongly negative across outputs).',
        '- [ ] NROY fraction decreases across waves (or justified if not).',
        '- [ ] At least 10 NROY points re-evaluated in full simulator and compared to emulator.',
        '- [ ] Best candidate verified against all 6 calibration targets using full simulator.',
        '- [ ] Parameter bounds for next wave generated from NROY with modest buffer (5-10%).',
    ]
    (ROOT / 'outputs' / 'emulation_qc.md').write_text('\n'.join(qc))

    guide = [
        '# History Matching Quick Guide for FibroTwin',
        '',
        'This project uses AutoEmulate as a surrogate model to accelerate calibration.',
        '',
        '## Prompt template to run',
        '"Run emulation history matching with N=<n_train> simulator runs, M=<n_candidates> emulator candidate points, and report NROY bounds + best plausible parameter set with target pass count."',
        '',
        '## Evaluation criteria',
        '- Emulator quality: R2/RMSE on held-out points.',
        '- Plausibility: size and stability of NROY region.',
        '- Ground truth: full simulator confirms selected NROY points.',
        '- Success condition: a candidate set passing all 6 calibration tasks in simulator checks.',
    ]
    (ROOT / 'docs' / '06_emulation_history_matching_guide.md').write_text('\n'.join(guide))

    plt.figure(figsize=(6.2, 3.8))
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
