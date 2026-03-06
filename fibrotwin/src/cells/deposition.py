import torch


def update_phenotype(agents, nodes, cue_node, threshold=0.15, k_switch=0.05):
    d = torch.cdist(agents.x, nodes)
    idx = torch.argmin(d, dim=1)
    local_cue = cue_node[idx]
    p = torch.sigmoid((local_cue - threshold) / max(k_switch, 1e-6))
    rand = torch.rand_like(p)
    switched = rand < p
    agents.is_myofibro = torch.logical_or(agents.is_myofibro, switched)
    return agents


def deposit_collagen(nodes, c, agent_x, agent_is_myo, dt, k_dep, sigma, k_deg, myo_boost=2.0):
    d2 = torch.cdist(nodes, agent_x) ** 2
    kern = torch.exp(-0.5 * d2 / (sigma ** 2))
    w = torch.where(agent_is_myo, torch.tensor(myo_boost, device=nodes.device), torch.tensor(1.0, device=nodes.device))
    dep = k_dep * (kern * w[None, :]).sum(dim=1)
    c_new = c + dt * dep - dt * k_deg * c
    return torch.clamp(c_new, min=0.0)
