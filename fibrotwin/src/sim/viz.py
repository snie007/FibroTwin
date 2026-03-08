import os
import numpy as np
import matplotlib.pyplot as plt
import torch


def _interp_disp_at_points(nodes, U, x):
    # IDW interpolation of nodal displacement to arbitrary points
    d = torch.cdist(x, nodes)
    k = min(6, nodes.shape[0])
    idx = torch.topk(d, k=k, largest=False).indices
    out = torch.zeros((x.shape[0], 2), device=x.device, dtype=nodes.dtype)
    u_node = U.view(-1, 2)
    for i in range(x.shape[0]):
        di = d[i, idx[i]]
        w = 1.0 / (di + 1e-6)
        w = w / (w.sum() + 1e-12)
        out[i] = (w[:, None] * u_node[idx[i]]).sum(dim=0)
    return out


def render_frame(path, nodes, elems, U, c, a, agents, stride=3, xlim=None, ylim=None, cmax=None):
    xy = nodes.detach().cpu().numpy()
    u = U.detach().cpu().numpy().reshape(-1, 2)
    cnp = c.detach().cpu().numpy()
    anp = a.detach().cpu().numpy()
    # visualize agents in deformed coordinates for geometric consistency
    xa = agents.x
    ua = _interp_disp_at_points(nodes, U, xa)
    xp = (xa + ua).detach().cpu().numpy()

    deformed = xy + u
    mag = np.linalg.norm(u, axis=1)

    fig, ax = plt.subplots(figsize=(8, 4))
    if cmax is None:
        cmax = float(max(1e-8, np.max(cnp)))
    levels = np.linspace(0.0, cmax, 21)
    t = ax.tricontourf(deformed[:, 0], deformed[:, 1], cnp, levels=levels, cmap='magma', alpha=0.85)
    plt.colorbar(t, ax=ax, label='collagen c (fixed scale)')
    ax.scatter(xp[:, 0], xp[:, 1], s=8, c='cyan', alpha=0.8, label='cells')

    qidx = np.arange(0, len(xy), stride)
    ax.quiver(deformed[qidx, 0], deformed[qidx, 1], anp[qidx, 0], anp[qidx, 1],
              color='white', alpha=0.6, scale=30)

    ax.set_title(f'FibroTwin MVP | max|u|={mag.max():.3e}')
    if xlim is None:
        xlim = (deformed[:, 0].min() - 0.5, deformed[:, 0].max() + 0.5)
    if ylim is None:
        ylim = (deformed[:, 1].min() - 0.5, deformed[:, 1].max() + 0.5)
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.set_aspect('equal')
    ax.legend(loc='upper right')
    fig.tight_layout()
    fig.savefig(path, dpi=120)
    plt.close(fig)


def _list_frames(frame_dir):
    return sorted([f for f in os.listdir(frame_dir) if f.endswith('.png')])


def make_gif(frame_dir, out_path, fps=20):
    try:
        import imageio.v2 as imageio
    except Exception:
        return False
    frames = _list_frames(frame_dir)
    ims = [imageio.imread(os.path.join(frame_dir, f)) for f in frames]
    imageio.mimsave(out_path, ims, duration=1.0 / fps)
    return True


def make_mp4(frame_dir, out_path, fps=20):
    try:
        import imageio.v2 as imageio
    except Exception:
        return False
    frames = _list_frames(frame_dir)
    if not frames:
        return False
    try:
        with imageio.get_writer(out_path, fps=fps, codec='libx264') as w:
            for f in frames:
                w.append_data(imageio.imread(os.path.join(frame_dir, f)))
        return True
    except Exception:
        return False
