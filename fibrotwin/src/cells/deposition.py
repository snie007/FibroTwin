import torch


def deposit_collagen(nodes, c, agent_x, dt, k_dep, sigma, k_deg):
    d2 = torch.cdist(nodes, agent_x) ** 2
    kern = torch.exp(-0.5 * d2 / (sigma ** 2))
    dep = k_dep * kern.sum(dim=1)
    c_new = c + dt * dep - dt * k_deg * c
    return torch.clamp(c_new, min=0.0)
