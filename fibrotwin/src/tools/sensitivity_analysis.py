import copy
import json
from pathlib import Path

import numpy as np
import torch
import yaml

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
        hs['myo_frac_final'],
        hs['p_mean_final'],
        hl['ac_align_x_final'],
        hls['c_mean_final'],
        inf.get('c_core', 0.0),
        inf.get('core_to_remote_ratio', 0.0),
    ], dtype=np.float32)


def rankdata(v):
    order = np.argsort(v)
    ranks = np.empty_like(order, dtype=float)
    ranks[order] = np.arange(len(v))
    return ranks


def spearman(x, y):
    rx = rankdata(x)
    ry = rankdata(y)
    if np.std(rx) < 1e-12 or np.std(ry) < 1e-12:
        return 0.0
    return float(np.corrcoef(rx, ry)[0, 1])


def objective(y, bands):
    # normalized distance-to-band objective (lower is better)
    s = 0.0
    for i, k in enumerate(bands.keys()):
        lo, hi = bands[k]
        v = float(y[i])
        if lo <= v <= hi:
            continue
        w = max(hi - lo, 1e-8)
        d = (lo - v) if v < lo else (v - hi)
        s += d / w
    return s


def pass_count(y, bands):
    c = 0
    for i, k in enumerate(bands.keys()):
        lo, hi = bands[k]
        if lo <= float(y[i]) <= hi:
            c += 1
    return c


def main(n_train=24, n_candidates=400, n_verify=8, seed=31):
    rng = np.random.default_rng(seed)
    cfg = yaml.safe_load((ROOT / 'configs' / 'mvp_2d_stretch.yaml').read_text())
    reg = yaml.safe_load((ROOT / 'data' / 'calibration' / 'parameter_registry.yaml').read_text())
    tg = yaml.safe_load((ROOT / 'data' / 'calibration' / 'targets.yaml').read_text())['targets']

    bands = {
        'myofibro_fraction_high_signal': tg['fibroblast_signaling']['myofibro_fraction_high_signal'],
        'profibrotic_index_high_signal': tg['fibroblast_signaling']['profibrotic_index_high_signal'],
        'alignment_high_load': tg['growth_remodeling']['alignment_high_load'],
        'collagen_fraction_load_signal': tg['growth_remodeling']['collagen_fraction_load_signal'],
        'infarct_core_collagen': tg['infarct_remodeling']['infarct_core_collagen'],
        'infarct_core_to_remote_ratio': tg['infarct_remodeling']['core_to_remote_ratio'],
    }

    bounds = []
    for s, k in PARAMS:
        kk = f'{s}.{k}'
        b = reg.get('parameters', {}).get(kk, {}).get('literature_band')
        if b is None:
            v = float(cfg.get(s, {}).get(k, 1.0))
            b = [0.5 * v, 1.5 * v if v != 0 else 1.0]
        bounds.append((float(b[0]), float(b[1])))

    X, Y, obj = [], [], []
    for _ in range(n_train):
        x = np.array([rng.uniform(lo, hi) for lo, hi in bounds], dtype=np.float32)
        y = eval_targets(set_params(cfg, x))
        X.append(x); Y.append(y); obj.append(objective(y, bands))
    X = np.asarray(X, dtype=np.float32)
    Y = np.asarray(Y, dtype=np.float32)
    obj = np.asarray(obj, dtype=np.float32)

    n_test = max(4, n_train // 4)
    ae = AutoEmulate(
        X[:-n_test], Y[:-n_test], test_data=(X[-n_test:], Y[-n_test:]),
        models=['GaussianProcessRBF', 'GaussianProcessMatern32', 'PolynomialRegression'],
        n_iter=4, n_splits=3, n_bootstraps=None, random_seed=seed, log_level='error'
    )
    best = ae.best_result('r2')

    # Global sensitivity proxy: Spearman correlation with objective
    sens = []
    for j, (s, k) in enumerate(PARAMS):
        rho = spearman(X[:, j], obj)
        sens.append({'parameter': f'{s}.{k}', 'spearman_obj': rho, 'abs_spearman_obj': abs(rho)})
    sens = sorted(sens, key=lambda r: r['abs_spearman_obj'], reverse=True)

    # Surrogate-guided candidate search and true verification
    Xc = np.asarray([[rng.uniform(lo, hi) for lo, hi in bounds] for _ in range(n_candidates)], dtype=np.float32)
    mean_t = best.model.predict_mean(torch.tensor(Xc)).detach().cpu().numpy()
    pred_obj = np.array([objective(y, bands) for y in mean_t], dtype=np.float32)
    idx = np.argsort(pred_obj)[:n_verify]

    verified = []
    for i in idx:
        x = Xc[int(i)]
        y = eval_targets(set_params(cfg, x))
        verified.append({
            'idx': int(i),
            'pred_obj': float(pred_obj[int(i)]),
            'true_obj': float(objective(y, bands)),
            'pass_count': int(pass_count(y, bands)),
            'params': {f'{a}.{b}': float(v) for (a, b), v in zip(PARAMS, x)},
        })
    verified = sorted(verified, key=lambda r: (r['true_obj'], -r['pass_count']))

    # Complexity diagnosis
    qmr = json.loads((ROOT / 'outputs' / 'quantitative_match_report.json').read_text()) if (ROOT / 'outputs' / 'quantitative_match_report.json').exists() else None
    quant_pass_rate = None
    if qmr:
        den = max(1, qmr['n_with_numeric_mentions'])
        quant_pass_rate = qmr['counts'].get('PASS', 0) / den

    best_pass = verified[0]['pass_count'] if verified else 0
    top3 = [s['parameter'] for s in sens[:3]]
    diagnosis = []
    diagnosis.append(f"Top objective-sensitive parameters: {', '.join(top3)}")
    if best_pass >= 6:
        diagnosis.append('Parameter issue is solvable in current model structure for 6-target calibration.')
    elif best_pass >= 5:
        diagnosis.append('Parameter tuning gets close, but structural constraints likely limit simultaneous fit.')
    else:
        diagnosis.append('Current parameter space did not produce high calibration fit; likely structural/model-form limitation.')
    if quant_pass_rate is not None and quant_pass_rate < 0.25:
        diagnosis.append('Paper-anchored quantitative agreement remains low; missing pathway/detail complexity is a major contributor.')

    suggestions = [
        'Extend signaling modules with explicit VEGF/Notch/HIF axis where literature anchors are abundant.',
        'Introduce zone-specific infarct signaling/deposition kernels (core/border/remote separate kinetics).',
        'Separate phenotype activation vs matrix deposition coupling to reduce over-coupled tradeoffs.',
        'Use multi-wave history matching with adaptive bounds around top sensitive parameters only.'
    ]

    out = {
        'n_train': int(n_train),
        'n_candidates': int(n_candidates),
        'best_model': best.model_name,
        'sensitivity_rank': sens,
        'verified_candidates': verified,
        'best_verified_pass_count': int(best_pass),
        'diagnosis': diagnosis,
        'suggested_extensions': suggestions,
    }
    (ROOT / 'outputs' / 'sensitivity_report.json').write_text(json.dumps(out, indent=2))

    lines = [
        '# Sensitivity + Emulation Diagnosis', '',
        f"- Training points: {n_train}",
        f"- Candidate points screened (emulator): {n_candidates}",
        f"- Best emulator: {best.model_name}",
        f"- Best verified pass count: {best_pass}/6", '',
        '## Top parameter sensitivities (Spearman vs objective)'
    ]
    for r in sens[:8]:
        lines.append(f"- {r['parameter']}: rho={r['spearman_obj']:.3f}")
    lines += ['', '## Diagnosis'] + [f"- {d}" for d in diagnosis] + ['', '## Suggested model extensions'] + [f"- {s}" for s in suggestions]
    (ROOT / 'outputs' / 'sensitivity_report.md').write_text('\n'.join(lines))

    print(json.dumps({'best_verified_pass_count': best_pass, 'top_sensitive': top3}, indent=2))


if __name__ == '__main__':
    main()
