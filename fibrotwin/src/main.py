import argparse
import os
import random
import numpy as np
import torch
import yaml

from .mechanics.mesh import create_rect_tri_mesh
from .sim.fields import init_fields
from .cells.agents import init_agents
from .sim.io import make_run_dir, save_config_copy, log_line
from .sim.time_integrator import run_sim
from .sim.viz import make_gif


def pick_device(cfg):
    if cfg['device'] == 'cpu':
        return torch.device('cpu')
    if cfg['device'] == 'cuda' and torch.cuda.is_available():
        return torch.device('cuda')
    return torch.device('cuda' if torch.cuda.is_available() else 'cpu')


def set_seed(seed):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--config', required=True)
    args = ap.parse_args()

    with open(args.config, 'r') as f:
        cfg = yaml.safe_load(f)

    set_seed(cfg['seed'])
    device = pick_device(cfg)

    out_dir = make_run_dir(cfg['output_root'])
    save_config_copy(args.config, out_dir)
    log_line(out_dir, f'device={device}')

    nodes, elems = create_rect_tri_mesh(
        cfg['mesh']['Lx'], cfg['mesh']['Ly'], cfg['mesh']['nx'], cfg['mesh']['ny'], device=device
    )
    fields = init_fields(nodes.shape[0], device=device, seed=cfg['seed'])
    agents = init_agents(cfg['cells']['n_agents'], cfg['mesh']['Lx'], cfg['mesh']['Ly'], device=device, seed=cfg['seed'])

    run_sim(cfg, nodes, elems, fields, agents, out_dir)
    gif_ok = make_gif(os.path.join(out_dir, 'frames'), os.path.join(out_dir, 'animation.gif'), fps=cfg['viz']['fps'])
    log_line(out_dir, f'animation_gif={gif_ok}')
    print(out_dir)


if __name__ == '__main__':
    main()
