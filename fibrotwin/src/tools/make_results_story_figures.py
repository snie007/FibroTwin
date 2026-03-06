import re
from pathlib import Path

import matplotlib.pyplot as plt
import torch
import yaml

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'outputs'
SITE_IMG = ROOT / 'site' / 'assets' / 'img'


def parse_log(run_dir: Path):
    steps = []
    a_align = []
    ac_align = []
    c_mean = []
    for line in (run_dir / 'run.log').read_text().splitlines() if (run_dir / 'run.log').exists() else []:
        m = re.search(r"step=(\d+).*c_mean=([0-9eE+\-.]+).*a_align_x=([0-9eE+\-.]+).*ac_align_x=([0-9eE+\-.]+)", line)
        if m:
            steps.append(int(m.group(1)))
            c_mean.append(float(m.group(2)))
            a_align.append(float(m.group(3)))
            ac_align.append(float(m.group(4)))
    return steps, c_mean, a_align, ac_align


def latest_runs(n=5):
    ds = sorted([d for d in OUT.iterdir() if d.is_dir()], key=lambda p: p.name, reverse=True)
    return ds[:n]


def make_agent_paths(run_dir: Path, run_id: str):
    snaps = sorted(run_dir.glob('step_*.pt'))
    if len(snaps) < 2:
        return
    take = snaps[::max(1, len(snaps)//80)]
    traj = []
    for s in take:
        d = torch.load(s, map_location='cpu')
        traj.append(d['agents_x'])
    # sample up to 20 agents
    n_agents = traj[0].shape[0]
    idx = torch.linspace(0, n_agents - 1, steps=min(20, n_agents)).long()

    fig, ax = plt.subplots(figsize=(6, 3.8))
    for i in idx:
        xy = torch.stack([t[i] for t in traj], dim=0).numpy()
        ax.plot(xy[:, 0], xy[:, 1], alpha=0.6, lw=1)
        ax.scatter(xy[-1, 0], xy[-1, 1], s=12)
    ax.set_title('Fibroblast paths (sampled agents)')
    ax.set_xlabel('x'); ax.set_ylabel('y')
    ax.set_aspect('equal')
    fig.tight_layout()
    fig.savefig(SITE_IMG / f'{run_id}_agent_paths.png', dpi=200)
    plt.close(fig)


def make_alignment_plot(run_dir: Path, run_id: str):
    steps, c_mean, a_align, ac_align = parse_log(run_dir)
    if not steps:
        return
    fig, ax = plt.subplots(figsize=(6.5, 3.8))
    ax.plot(steps, a_align, '-o', ms=3, label='myofibre align x')
    ax.plot(steps, ac_align, '-o', ms=3, label='collagen align x')
    ax.set_ylim(0, 1)
    ax.set_xlabel('Step')
    ax.set_ylabel('Alignment metric |a·ex|')
    ax.set_title('Fibre reorientation toward loading direction')
    ax.legend()
    fig.tight_layout()
    fig.savefig(SITE_IMG / f'{run_id}_alignment.png', dpi=200)
    plt.close(fig)


def make_montage(run_dir: Path, run_id: str):
    fr = sorted((run_dir / 'frames').glob('frame_*.png')) if (run_dir / 'frames').exists() else []
    if len(fr) < 2:
        return
    sel_idx = [0, len(fr)//5, 2*len(fr)//5, 3*len(fr)//5, 4*len(fr)//5, len(fr)-1]
    sel = [fr[i] for i in sel_idx]
    imgs = [plt.imread(str(p)) for p in sel]

    fig, axs = plt.subplots(2, 3, figsize=(12, 6))
    for ax, im, p in zip(axs.ravel(), imgs, sel):
        ax.imshow(im)
        ax.set_title(p.stem)
        ax.axis('off')
    fig.suptitle('Time-sequence: collagen + cells + fibre orientation')
    fig.tight_layout()
    fig.savefig(SITE_IMG / f'{run_id}_montage6.png', dpi=180)
    plt.close(fig)


def main():
    SITE_IMG.mkdir(parents=True, exist_ok=True)
    for d in latest_runs(6):
        run_id = d.name
        make_agent_paths(d, run_id)
        make_alignment_plot(d, run_id)
        make_montage(d, run_id)
    print('Generated results story figures')


if __name__ == '__main__':
    main()
