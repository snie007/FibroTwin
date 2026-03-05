import torch


def principal_direction_from_strain(eps):
    # eps shape (...,3) with [exx, eyy, exy]
    out = []
    for e in eps:
        E = torch.tensor([[e[0], e[2]], [e[2], e[1]]], dtype=e.dtype, device=e.device)
        vals, vecs = torch.linalg.eigh(E)
        out.append(vecs[:, -1])
    return torch.stack(out)


def update_fibres(a_node, target_node, dt, tau):
    a_new = a_node + (dt / tau) * (target_node - a_node)
    return a_new / (a_new.norm(dim=1, keepdim=True) + 1e-12)
