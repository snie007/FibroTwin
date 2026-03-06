import torch
from src.mechanics.mesh import create_rect_tri_mesh
from src.mechanics.nonlinear_solver import solve_quasistatic_ogden


def test_ogden_solver_respects_dirichlet():
    Lx, Ly = 1.0, 0.5
    nodes, elems = create_rect_tri_mesh(Lx, Ly, 6, 3)
    n = nodes.shape[0]
    left = torch.where(torch.isclose(nodes[:, 0], torch.tensor(0.0)))[0]
    right = torch.where(torch.isclose(nodes[:, 0], torch.tensor(Lx)))[0]

    fixed_dofs = []
    fixed_vals = []
    for i in left.tolist():
        fixed_dofs += [2 * i, 2 * i + 1]
        fixed_vals += [0.0, 0.0]
    for i in right.tolist():
        fixed_dofs += [2 * i]
        fixed_vals += [0.1 * Lx]

    fixed_dofs = torch.tensor(fixed_dofs, dtype=torch.long)
    fixed_vals = torch.tensor(fixed_vals, dtype=torch.float32)

    U = solve_quasistatic_ogden(nodes, elems, fixed_dofs, fixed_vals, material={"mu": 10.0, "alpha": 8.0, "kappa": 100.0}, max_iter=20)
    assert torch.isfinite(U).all()
    assert torch.allclose(U[fixed_dofs], fixed_vals, atol=1e-5)
