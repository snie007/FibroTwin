import os
import numpy as np
import matplotlib.pyplot as plt


def render_frame(path, nodes, elems, U, c, a, agents, stride=3):
    xy = nodes.detach().cpu().numpy()
    u = U.detach().cpu().numpy().reshape(-1, 2)
    cnp = c.detach().cpu().numpy()
    anp = a.detach().cpu().numpy()
    xp = agents.x.detach().cpu().numpy()

    deformed = xy + u
    mag = np.linalg.norm(u, axis=1)

    fig, ax = plt.subplots(figsize=(8, 4))
    t = ax.tricontourf(deformed[:,0], deformed[:,1], cnp, levels=20, cmap='magma', alpha=0.85)
    plt.colorbar(t, ax=ax, label='collagen c')
    ax.scatter(xp[:,0], xp[:,1], s=8, c='cyan', alpha=0.8, label='cells')

    qidx = np.arange(0, len(xy), stride)
    ax.quiver(deformed[qidx,0], deformed[qidx,1], anp[qidx,0], anp[qidx,1],
              color='white', alpha=0.6, scale=30)

    ax.set_title(f'FibroTwin MVP | max|u|={mag.max():.3e}')
    ax.set_xlim(deformed[:,0].min()-0.5, deformed[:,0].max()+0.5)
    ax.set_ylim(deformed[:,1].min()-0.5, deformed[:,1].max()+0.5)
    ax.set_aspect('equal')
    ax.legend(loc='upper right')
    fig.tight_layout()
    fig.savefig(path, dpi=120)
    plt.close(fig)


def make_gif(frame_dir, out_path, fps=20):
    try:
        import imageio.v2 as imageio
    except Exception:
        return False
    frames = sorted([f for f in os.listdir(frame_dir) if f.endswith('.png')])
    ims = [imageio.imread(os.path.join(frame_dir, f)) for f in frames]
    imageio.mimsave(out_path, ims, duration=1.0 / fps)
    return True
