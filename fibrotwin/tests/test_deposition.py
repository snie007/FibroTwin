import torch
from src.cells.deposition import deposit_collagen, update_phenotype
from src.cells.agents import Agents


def test_single_cell_radial_like():
    xs = torch.linspace(-1, 1, 21)
    yy, xx = torch.meshgrid(xs, xs, indexing='ij')
    nodes = torch.stack([xx.reshape(-1), yy.reshape(-1)], dim=1)
    c = torch.zeros(nodes.shape[0])
    cell = torch.tensor([[0.0, 0.0]])
    is_myo = torch.tensor([False])
    c2 = deposit_collagen(nodes, c, cell, is_myo, dt=1.0, k_dep=1.0, sigma=0.2, k_deg=0.0)
    center = torch.argmin(torch.sum(nodes**2, dim=1))
    assert c2[center] == torch.max(c2)
    assert torch.all(c2 >= 0)


def test_myofibro_switch_and_boost():
    nodes = torch.tensor([[0.0, 0.0], [1.0, 0.0]], dtype=torch.float32)
    cue = torch.tensor([0.5, 0.01], dtype=torch.float32)
    agents = Agents(
        x=torch.tensor([[0.0, 0.0], [1.0, 0.0]], dtype=torch.float32),
        v=torch.zeros((2, 2), dtype=torch.float32),
        is_myofibro=torch.zeros(2, dtype=torch.bool),
    )
    agents = update_phenotype(agents, nodes, cue, threshold=0.1, k_switch=0.01)
    assert agents.is_myofibro[0]
    c = torch.zeros(2, dtype=torch.float32)
    c2 = deposit_collagen(nodes, c, agents.x, agents.is_myofibro, dt=1.0, k_dep=1.0, sigma=0.3, k_deg=0.0, myo_boost=3.0)
    assert c2[0] > c2[1]


def test_motion_trail_deposition():
    nodes = torch.tensor([[0.0, 0.0], [0.6, 0.0], [1.0, 0.0]], dtype=torch.float32)
    c = torch.zeros(3, dtype=torch.float32)
    x = torch.tensor([[1.0, 0.0]], dtype=torch.float32)
    v = torch.tensor([[1.0, 0.0]], dtype=torch.float32)
    is_myo = torch.tensor([False])
    c2 = deposit_collagen(nodes, c, x, is_myo, dt=1.0, k_dep=1.0, sigma=0.15, k_deg=0.0, agent_v=v, trail_gain=0.8, trail_len=0.4)
    assert c2[1] > c2[0]
