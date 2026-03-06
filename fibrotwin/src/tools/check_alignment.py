import copy
import yaml
import torch

from src.mechanics.mesh import create_rect_tri_mesh
from src.sim.fields import init_fields
from src.cells.agents import init_agents
from src.sim.io import make_run_dir, log_line
from src.sim.time_integrator import run_sim


def main(config_path='configs/mvp_2d_stretch.yaml', threshold=0.85):
    with open(config_path, 'r') as f:
        cfg = yaml.safe_load(f)

    cfg = copy.deepcopy(cfg)
    cfg['viz']['enable'] = False
    cfg['viz']['frame_every'] = 10**9
    cfg['time']['n_steps'] = 220
    cfg['mesh']['nx'] = min(cfg['mesh']['nx'], 12)
    cfg['mesh']['ny'] = min(cfg['mesh']['ny'], 6)

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    torch.manual_seed(cfg['seed'])

    out_dir = make_run_dir(cfg['output_root'])
    log_line(out_dir, 'alignment_check_run=true')

    nodes, elems = create_rect_tri_mesh(cfg['mesh']['Lx'], cfg['mesh']['Ly'], cfg['mesh']['nx'], cfg['mesh']['ny'], device=device)
    fields = init_fields(nodes.shape[0], device=device, seed=cfg['seed'])
    agents = init_agents(cfg['cells']['n_agents'], cfg['mesh']['Lx'], cfg['mesh']['Ly'], device=device, seed=cfg['seed'])

    a0 = torch.abs(fields.a[:, 0]).mean().item()
    ac0 = torch.abs(fields.ac[:, 0]).mean().item()

    fields, agents = run_sim(cfg, nodes, elems, fields, agents, out_dir)

    a1 = torch.abs(fields.a[:, 0]).mean().item()
    ac1 = torch.abs(fields.ac[:, 0]).mean().item()

    passed = (ac1 >= threshold) and (ac1 > ac0)
    print({
        'run_dir': out_dir,
        'a_align_x_init': round(a0, 4),
        'a_align_x_final': round(a1, 4),
        'ac_align_x_init': round(ac0, 4),
        'ac_align_x_final': round(ac1, 4),
        'threshold': threshold,
        'pass': passed,
    })


if __name__ == '__main__':
    main()
