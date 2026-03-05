import torch


def apply_dirichlet(K, f, fixed_dofs, fixed_vals):
    K2 = K.clone()
    f2 = f.clone()
    for dof, val in zip(fixed_dofs.tolist(), fixed_vals.tolist()):
        f2 -= K2[:, dof] * val
    for dof, val in zip(fixed_dofs.tolist(), fixed_vals.tolist()):
        K2[dof, :] = 0
        K2[:, dof] = 0
        K2[dof, dof] = 1.0
        f2[dof] = val
    return K2, f2


def solve_linear_system(K, f):
    return torch.linalg.solve(K, f)
