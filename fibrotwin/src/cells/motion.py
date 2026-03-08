import torch


def sample_gradient_at_positions(nodes, scalar_node, x):
    d = torch.cdist(x, nodes)
    k = min(6, nodes.shape[0])
    idx = torch.topk(d, k=k, largest=False).indices
    grads = torch.zeros_like(x)
    for i in range(x.shape[0]):
        p = x[i]
        nbr = nodes[idx[i]]
        vals = scalar_node[idx[i]]
        A = torch.cat([nbr - p, torch.ones((nbr.shape[0], 1), device=x.device)], dim=1)
        sol = torch.linalg.lstsq(A, vals).solution
        grads[i] = sol[:2]
    return grads


def sample_vector_at_positions(nodes, vec_node, x):
    d = torch.cdist(x, nodes)
    k = min(6, nodes.shape[0])
    idx = torch.topk(d, k=k, largest=False).indices
    out = torch.zeros((x.shape[0], vec_node.shape[1]), device=x.device, dtype=vec_node.dtype)
    for i in range(x.shape[0]):
        di = d[i, idx[i]]
        w = 1.0 / (di + 1e-6)
        w = w / (w.sum() + 1e-12)
        out[i] = (w[:, None] * vec_node[idx[i]]).sum(dim=0)
    return out


def update_agents(agents, nodes, cue, dt, params, bounds, advect_node=None):
    rho = params['persistence']
    noise_std = params['noise_std']
    taxis = params['taxis_weight']
    speed = params['speed']
    advection_gain = params.get('advection_gain', 1.0)

    noise = noise_std * torch.randn_like(agents.v)
    grad = sample_gradient_at_positions(nodes, cue, agents.x)
    agents.v = rho * agents.v + (1 - rho) * noise + taxis * grad
    vn = agents.v.norm(dim=1, keepdim=True) + 1e-12
    agents.v = speed * agents.v / vn

    # motility + kinematic advection by tissue displacement increment
    dx_mot = dt * agents.v
    dx_adv = torch.zeros_like(dx_mot)
    if advect_node is not None:
        dx_adv = advection_gain * sample_vector_at_positions(nodes, advect_node, agents.x)

    agents.x = agents.x + dx_mot + dx_adv

    Lx, Ly = bounds
    for d, L in enumerate([Lx, Ly]):
        lo = agents.x[:, d] < 0
        hi = agents.x[:, d] > L
        agents.x[lo, d] = -agents.x[lo, d]
        agents.v[lo, d] *= -1
        agents.x[hi, d] = 2 * L - agents.x[hi, d]
        agents.v[hi, d] *= -1
    return agents
