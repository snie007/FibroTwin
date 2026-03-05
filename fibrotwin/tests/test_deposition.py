import torch
from src.cells.deposition import deposit_collagen


def test_single_cell_radial_like():
    xs = torch.linspace(-1, 1, 21)
    yy, xx = torch.meshgrid(xs, xs, indexing='ij')
    nodes = torch.stack([xx.reshape(-1), yy.reshape(-1)], dim=1)
    c = torch.zeros(nodes.shape[0])
    cell = torch.tensor([[0.0, 0.0]])
    c2 = deposit_collagen(nodes, c, cell, dt=1.0, k_dep=1.0, sigma=0.2, k_deg=0.0)
    center = torch.argmin(torch.sum(nodes**2, dim=1))
    assert c2[center] == torch.max(c2)
    assert torch.all(c2 >= 0)
