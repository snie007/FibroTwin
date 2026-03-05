from dataclasses import dataclass
import torch


@dataclass
class Agents:
    x: torch.Tensor
    v: torch.Tensor


def init_agents(n_agents, Lx, Ly, device, seed=0):
    g = torch.Generator(device='cpu').manual_seed(seed + 1)
    x = torch.stack([
        torch.rand(n_agents, generator=g) * Lx,
        torch.rand(n_agents, generator=g) * Ly,
    ], dim=1).to(device)
    v = torch.zeros((n_agents, 2), device=device)
    return Agents(x=x, v=v)
