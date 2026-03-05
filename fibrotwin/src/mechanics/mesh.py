import torch


def create_rect_tri_mesh(Lx: float, Ly: float, nx: int, ny: int, device=None):
    xs = torch.linspace(0.0, Lx, nx)
    ys = torch.linspace(0.0, Ly, ny)
    xx, yy = torch.meshgrid(xs, ys, indexing='xy')
    nodes = torch.stack([xx.reshape(-1), yy.reshape(-1)], dim=1)

    def idx(i, j):
        return j * nx + i

    elems = []
    for j in range(ny - 1):
        for i in range(nx - 1):
            n0 = idx(i, j)
            n1 = idx(i + 1, j)
            n2 = idx(i, j + 1)
            n3 = idx(i + 1, j + 1)
            elems.append([n0, n1, n3])
            elems.append([n0, n3, n2])
    elems = torch.tensor(elems, dtype=torch.long)
    if device is not None:
        nodes = nodes.to(device)
        elems = elems.to(device)
    return nodes, elems
