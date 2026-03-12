import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PY = '/home/snie007/Documents/project/2026/freeze_combined_out7/.venv/bin/python'


def run_module(module, args=None, timeout=420):
    cmd = [PY, '-m', module] + (args or [])
    try:
        p = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, timeout=timeout)
        return {'cmd': ' '.join(cmd), 'code': p.returncode, 'stdout': p.stdout[-2000:], 'stderr': p.stderr[-2000:]}
    except subprocess.TimeoutExpired:
        return {'cmd': ' '.join(cmd), 'code': 124, 'stdout': '', 'stderr': f'timeout after {timeout}s'}


def run_inline(code: str, label: str, timeout=420):
    cmd = [PY, '-c', code]
    try:
        p = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, timeout=timeout)
        return {'cmd': label, 'code': p.returncode, 'stdout': p.stdout[-2000:], 'stderr': p.stderr[-2000:]}
    except subprocess.TimeoutExpired:
        return {'cmd': label, 'code': 124, 'stdout': '', 'stderr': f'timeout after {timeout}s'}

def load_json(path):
    p = ROOT / path
    return json.loads(p.read_text()) if p.exists() else None


def classify_fails(qmr):
    rows = (qmr or {}).get('rows', [])
    out = {'parameter_miss': 0, 'observation_mismatch': 0, 'missing_mechanism_or_unmapped': 0}
    for r in rows:
        st = r.get('status')
        if st == 'UNMAPPED':
            out['missing_mechanism_or_unmapped'] += 1
            continue
        ne = float(r.get('normalized_error', 0.0))
        kind = r.get('kind', '')
        anchor = str(r.get('paper_anchor', '')).lower()
        if st == 'FAIL':
            if ('p <' in anchor) or ('week' in anchor) or ('day' in anchor) or kind in ('absolute',) and (r.get('model_value', 0) < 2 and r.get('paper_band', [0,0])[0] > 20):
                out['observation_mismatch'] += 1
            else:
                out['parameter_miss'] += 1
        elif st == 'PARTIAL':
            out['parameter_miss'] += 1
    return out


def main(mode='fast'):
    steps = []
    steps.append(run_module('src.tools.extract_quantitative_evidence', timeout=1200))
    steps.append(run_module('src.tools.quantitative_match_metric', timeout=600))

    if mode == 'deep':
        steps.append(run_inline("from src.tools.emulation_waves import main; main(n_waves=4, n_train=24, n_candidates=300, seed=41)", 'emulation_waves.main(n_waves=4,n_train=24,n_candidates=300)', timeout=3600))
        steps.append(run_inline("from src.tools.sensitivity_analysis import main; main(n_train=18, n_candidates=260, n_verify=10, seed=43)", 'sensitivity_analysis.main(n_train=18,n_candidates=260,n_verify=10)', timeout=3600))
    else:
        # bounded wave run to avoid long hangs
        steps.append(run_inline("from src.tools.emulation_waves import main; main(n_waves=2, n_train=10, n_candidates=90, seed=29)", 'emulation_waves.main(n_waves=2,n_train=10,n_candidates=90)', timeout=1200))

    qmr = load_json('outputs/quantitative_match_report.json')
    ew = load_json('outputs/emulation_waves.json')
    cr = load_json('outputs/calibration_report.json')

    fail_tax = classify_fails(qmr)

    waves = (ew or {}).get('waves', [])
    nroy_trend = [w.get('nroy_fraction') for w in waves]
    pass_trend = [w.get('targets_passed') for w in waves]

    diagnosis = []
    if cr:
        diagnosis.append(f"Calibration targets pass: {cr.get('n_pass')}/{cr.get('n')}")
    if qmr:
        c = qmr.get('counts', {})
        diagnosis.append(f"Paper-anchored quantitative match: PASS {c.get('PASS',0)}, PARTIAL {c.get('PARTIAL',0)}, FAIL {c.get('FAIL',0)}, UNMAPPED {c.get('UNMAPPED',0)}")
    if pass_trend:
        diagnosis.append(f"History matching wave pass trend: {pass_trend}")
    if nroy_trend:
        diagnosis.append(f"NROY fraction trend: {[round(x,3) for x in nroy_trend]}")

    prioritized_extensions = [
        'Add observation-model mapping layer (paper endpoint -> model observable transform) to reduce observation mismatch fails.',
        'Expand signaling complexity: VEGF/Notch/HIF modules for angiogenesis-related studies.',
        'Refine infarct zone kinetics (core/border/remote separate source/decay kernels).',
        'Constrain tuning to top sensitive parameters and re-run waves with narrowed bounds.'
    ]

    out = {
        'steps': steps,
        'diagnosis': diagnosis,
        'fail_taxonomy': fail_tax,
        'wave_summary': {
            'nroy_fraction_trend': nroy_trend,
            'targets_passed_trend': pass_trend,
        },
        'prioritized_extensions': prioritized_extensions,
    }

    (ROOT / 'outputs' / 'wave_orchestrator_report.json').write_text(json.dumps(out, indent=2))

    md = ['# Wave Orchestrator Report', '']
    md += ['## Pipeline steps']
    for s in steps:
        md.append(f"- `{s['cmd']}` -> code {s['code']}")
    md += ['', '## Diagnosis'] + [f"- {d}" for d in diagnosis]
    md += ['', '## Fail taxonomy'] + [f"- {k}: {v}" for k, v in fail_tax.items()]
    md += ['', '## Suggested next actions'] + [f"- {x}" for x in prioritized_extensions]
    (ROOT / 'outputs' / 'wave_orchestrator_report.md').write_text('\n'.join(md))

    print(json.dumps({'ok': True, 'steps': len(steps)}, indent=2))


if __name__ == '__main__':
    import argparse
    ap = argparse.ArgumentParser(description='Wave Orchestrator')
    ap.add_argument('--mode', choices=['fast', 'deep'], default='fast')
    args = ap.parse_args()
    main(mode=args.mode)
