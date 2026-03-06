import torch


def update_phenotype(agents, nodes, cue_node, profibrotic_node=None, threshold=0.45, k_switch=0.08, deact_threshold=0.20):
    d = torch.cdist(agents.x, nodes)
    idx = torch.argmin(d, dim=1)
    local_cue = cue_node[idx]
    local_p = profibrotic_node[idx] if profibrotic_node is not None else torch.zeros_like(local_cue)
    z = (0.6 * local_cue + 1.0 * local_p - threshold) / max(k_switch, 1e-6)
    p_on = torch.sigmoid(z)
    rand = torch.rand_like(p_on)
    switched_on = rand < p_on

    # reversible deactivation under weak pro-fibrotic conditions
    z_off = (deact_threshold - (0.6 * local_cue + local_p)) / max(k_switch, 1e-6)
    p_off = 0.2 * torch.sigmoid(z_off)
    switched_off = rand < p_off

    agents.is_myofibro = torch.logical_or(agents.is_myofibro, switched_on)
    agents.is_myofibro = torch.logical_and(agents.is_myofibro, ~switched_off)
    return agents


def deposit_collagen(nodes, c, agent_x, agent_is_myo, dt, k_dep, sigma, k_deg, myo_boost=2.0, agent_p=None, agent_cue=None, p_gain=1.0, mech_gain=0.5, synergy_gain=0.6):
    d2 = torch.cdist(nodes, agent_x) ** 2
    kern = torch.exp(-0.5 * d2 / (sigma ** 2))

    w = torch.ones(agent_x.shape[0], device=nodes.device)
    w = w + torch.where(agent_is_myo, torch.tensor(myo_boost, device=nodes.device), torch.tensor(0.0, device=nodes.device))
    if agent_p is not None:
        w = w + p_gain * torch.clamp(agent_p, min=0.0)
    if agent_cue is not None:
        w = w + mech_gain * torch.clamp(agent_cue, min=0.0)
    if (agent_p is not None) and (agent_cue is not None):
        w = w + synergy_gain * torch.clamp(agent_p, min=0.0) * torch.clamp(agent_cue, min=0.0)

    dep = k_dep * (kern * w[None, :]).sum(dim=1)
    c_new = c + dt * dep - dt * k_deg * c
    return torch.clamp(c_new, min=0.0)
