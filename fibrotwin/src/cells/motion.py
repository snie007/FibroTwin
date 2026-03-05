import torch


def sample_gradient_at_positions(nodes, scalar_node, x):
    # simple nearest-neighbor finite-difference proxy on unstructured nodes
    # for MVP, use weighted differences to k nearest points
    d = torch.cdist(x, nodes)
    idx = torch.topk(d, k=6, largest=False).indices
    grads = torch.zeros_like(x)
    for i in range(x.shape[0]):
        p = x[i]
        nbr = nodes[idx[i]]
        vals = scalar_node[idx[i]]
        A = torch.cat([nbr - p, torch.ones((nbr.shape[0], 1), device=x.device)], dim=1)
        sol = torch.linalg.lstsq(A, vals).solution
        grads[i] = sol[:2]
    return grads


def update_agents(agents, nodes, cue, dt, params, bounds):
    rho = params['persistence']
    noise_std = params['noise_std']
    taxis = params['taxis_weight']
    speed = params['speed']

    noise = noise_std * torch.randn_like(agents.v)
    grad = sample_gradient_at_positions(nodes, cue, agents.x)
    agents.v = rho * agents.v + (1 - rho) * noise + taxis * grad
    vn = agents.v.norm(dim=1, keepdim=True) + 1e-12
    agents.v = speed * agents.v / vn
    agents.x = agents.x + dt * agents.v

    Lx, Ly = bounds
    for d, L in enumerate([Lx, Ly]):
        lo = agents.x[:, d] < 0
        hi = agents.x[:, d] > L
        agents.x[lo, d] = -agents.x[lo, d]
        agents.v[lo, d] *= -1
        agents.x[hi, d] = 2 * L - agents.x[hi, d]
        agents.v[hi, d] *= -1
    return agents
