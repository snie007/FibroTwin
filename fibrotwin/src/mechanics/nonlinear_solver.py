import torch


def _tri_rest_data(nodes, elems):
    dm_inv = []
    area0 = []
    for conn in elems:
        X = nodes[conn]
        dX = torch.stack([X[1] - X[0], X[2] - X[0]], dim=1)  # 2x2
        dm_inv.append(torch.linalg.inv(dX))
        area0.append(0.5 * torch.abs(torch.linalg.det(dX)))
    return torch.stack(dm_inv), torch.stack(area0)


def ogden_element_energy(F, mu=20.0, alpha=8.0, kappa=200.0):
    C = F.T @ F
    evals = torch.linalg.eigvalsh(C)
    evals = torch.clamp(evals, min=1e-9)
    lam1 = torch.sqrt(evals[0])
    lam2 = torch.sqrt(evals[1])
    J = torch.det(F)
    J = torch.clamp(J, min=1e-8)
    lam3 = torch.tensor(1.0, device=F.device, dtype=F.dtype)
    w_iso = (mu / alpha) * (lam1 ** alpha + lam2 ** alpha + lam3 ** alpha - 3.0)
    w_vol = 0.5 * kappa * (J - 1.0) ** 2
    return w_iso + w_vol


def solve_quasistatic_ogden(nodes, elems, fixed_dofs, fixed_vals, U0=None, material=None, max_iter=80):
    device = nodes.device
    dtype = nodes.dtype
    n = nodes.shape[0]
    ndof = 2 * n

    dm_inv, area0 = _tri_rest_data(nodes, elems)

    if U0 is None:
        U = torch.zeros(ndof, device=device, dtype=dtype)
    else:
        U = U0.detach().clone().to(device=device, dtype=dtype)

    fixed = torch.zeros(ndof, dtype=torch.bool, device=device)
    fixed[fixed_dofs] = True
    free_dofs = torch.where(~fixed)[0]

    U[fixed_dofs] = fixed_vals
    u_free = U[free_dofs].clone().detach().requires_grad_(True)

    mu = float(material.get('mu', 20.0)) if material else 20.0
    alpha = float(material.get('alpha', 8.0)) if material else 8.0
    kappa = float(material.get('kappa', 200.0)) if material else 200.0

    optimizer = torch.optim.LBFGS([u_free], lr=0.8, max_iter=max_iter, tolerance_grad=1e-8, tolerance_change=1e-10)

    def closure():
        optimizer.zero_grad()
        Ufull = torch.zeros(ndof, device=device, dtype=dtype)
        Ufull[fixed_dofs] = fixed_vals
        Ufull[free_dofs] = u_free
        xdef = nodes + Ufull.view(-1, 2)

        total = torch.tensor(0.0, device=device, dtype=dtype)
        for e, conn in enumerate(elems):
            x = xdef[conn]
            ds = torch.stack([x[1] - x[0], x[2] - x[0]], dim=1)
            F = ds @ dm_inv[e]
            total = total + area0[e] * ogden_element_energy(F, mu=mu, alpha=alpha, kappa=kappa)

        total.backward()
        return total

    optimizer.step(closure)

    Ufinal = torch.zeros(ndof, device=device, dtype=dtype)
    Ufinal[fixed_dofs] = fixed_vals
    Ufinal[free_dofs] = u_free.detach()
    return Ufinal
