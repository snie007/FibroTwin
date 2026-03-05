import torch
from .materials import constitutive_matrix


def tri_B_matrix(xy: torch.Tensor):
    x1, y1 = xy[0]
    x2, y2 = xy[1]
    x3, y3 = xy[2]
    A = 0.5 * ((x2 - x1) * (y3 - y1) - (x3 - x1) * (y2 - y1))
    b1, b2, b3 = y2 - y3, y3 - y1, y1 - y2
    c1, c2, c3 = x3 - x2, x1 - x3, x2 - x1
    B = torch.tensor([
        [b1, 0, b2, 0, b3, 0],
        [0, c1, 0, c2, 0, c3],
        [c1, b1, c2, b2, c3, b3],
    ], dtype=xy.dtype, device=xy.device) / (2 * A)
    return B, torch.abs(A)


def assemble_stiffness(nodes, elems, E_map, nu=0.3, plane_stress=True, a_elem=None, c_elem=None, kf=0.2):
    n = nodes.shape[0]
    ndof = 2 * n
    K = torch.zeros((ndof, ndof), dtype=nodes.dtype, device=nodes.device)

    for e, conn in enumerate(elems):
        xy = nodes[conn]
        B, A = tri_B_matrix(xy)
        D = constitutive_matrix(float(E_map[e].item()), nu, plane_stress, device=nodes.device).to(nodes.dtype)
        Ke = A * (B.T @ D @ B)

        # Simplified anisotropy: extra stiffness along local fibre direction
        if a_elem is not None and c_elem is not None:
            a = a_elem[e]
            a = a / (torch.norm(a) + 1e-12)
            ax, ay = a[0], a[1]
            w = torch.tensor([ax * ax, ay * ay, 2 * ax * ay], dtype=nodes.dtype, device=nodes.device)
            Ba = w @ B  # (6,)
            Ke = Ke + A * (kf * torch.clamp(c_elem[e], min=0.0)) * torch.outer(Ba, Ba)

        dofs = []
        for nid in conn.tolist():
            dofs += [2 * nid, 2 * nid + 1]
        dofs = torch.tensor(dofs, dtype=torch.long, device=nodes.device)
        K[dofs[:, None], dofs[None, :]] += Ke
    return K


def element_strain(nodes, elems, U):
    strains = []
    for conn in elems:
        xy = nodes[conn]
        B, _ = tri_B_matrix(xy)
        dofs = []
        for nid in conn.tolist():
            dofs += [2 * nid, 2 * nid + 1]
        ue = U[dofs]
        strains.append(B @ ue)
    return torch.stack(strains)
