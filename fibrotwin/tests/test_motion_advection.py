import torch
from src.cells.agents import Agents
from src.cells.motion import update_agents


def test_agent_advection_moves_with_tissue_increment():
    nodes = torch.tensor([[0.0, 0.0], [1.0, 0.0], [0.0, 1.0], [1.0, 1.0]], dtype=torch.float32)
    cue = torch.zeros(4)
    agents = Agents(
        x=torch.tensor([[0.5, 0.5]], dtype=torch.float32),
        v=torch.zeros((1, 2), dtype=torch.float32),
        is_myofibro=torch.zeros(1, dtype=torch.bool),
    )
    params = {
        'persistence': 1.0,
        'noise_std': 0.0,
        'taxis_weight': 0.0,
        'speed': 0.0,
        'advection_gain': 1.0,
    }
    adv = torch.tensor([[0.2, 0.0], [0.2, 0.0], [0.2, 0.0], [0.2, 0.0]], dtype=torch.float32)
    agents2 = update_agents(agents, nodes, cue, dt=1.0, params=params, bounds=(2.0, 2.0), advect_node=adv)
    assert agents2.x[0, 0] > 0.65
