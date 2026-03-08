import copy
import tempfile
from pathlib import Path

import yaml

from src.main import main as run_main


def run_with_cfg(cfg, name):
    with tempfile.NamedTemporaryFile('w', suffix=f'_{name}.yaml', delete=False) as f:
        yaml.safe_dump(cfg, f)
        p = f.name
    import sys
    argv_bak = sys.argv
    try:
        sys.argv = ['python', '--config', p]
        run_main()
    finally:
        sys.argv = argv_bak


def main(base='configs/mvp_2d_stretch.yaml'):
    with open(base, 'r') as f:
        cfg = yaml.safe_load(f)

    common = copy.deepcopy(cfg)
    common['time']['n_steps'] = 520
    common['viz']['frame_every'] = 5
    common['viz']['fps'] = 20
    common['mechanics']['model'] = 'linear'  # faster for interactive scenario batch

    scenarios = [
        ('baseline', {'mechanics': {'stretch_x': 0.10}, 'signaling': {'tgf_beta': 0.05, 'angII': 0.05}, 'infarct': {'enabled': False}}),
        ('high_load', {'mechanics': {'stretch_x': 0.28}, 'signaling': {'tgf_beta': 0.05, 'angII': 0.05}, 'infarct': {'enabled': False}}),
        ('high_signal', {'mechanics': {'stretch_x': 0.10}, 'signaling': {'tgf_beta': 0.50, 'angII': 0.45}, 'infarct': {'enabled': False}}),
        ('load_signal', {'mechanics': {'stretch_x': 0.28}, 'signaling': {'tgf_beta': 0.50, 'angII': 0.45}, 'infarct': {'enabled': False}}),
        ('infarct_load_signal', {'mechanics': {'stretch_x': 0.28}, 'signaling': {'tgf_beta': 0.50, 'angII': 0.45}, 'infarct': {'enabled': True}}),
    ]

    for name, patch in scenarios:
        c = copy.deepcopy(common)
        for sec, vals in patch.items():
            c.setdefault(sec, {}).update(vals)
        run_with_cfg(c, name)


if __name__ == '__main__':
    main()
