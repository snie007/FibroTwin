import torch
from src.mechanics.mesh import create_rect_tri_mesh
from src.mechanics.fem_assembly import assemble_stiffness
from src.mechanics.solver import apply_dirichlet, solve_linear_system


def test_fem_uniaxial_patch_like():
    Lx, Ly = 2.0, 1.0
    nodes, elems = create_rect_tri_mesh(Lx, Ly, 8, 4)
    n = nodes.shape[0]
    K = assemble_stiffness(nodes, elems, E_map=torch.ones(elems.shape[0]) * 10.0, nu=0.3)
    f = torch.zeros(2 * n)
    left = torch.where(torch.isclose(nodes[:, 0], torch.tensor(0.0)))[0]
    right = torch.where(torch.isclose(nodes[:, 0], torch.tensor(Lx)))[0]
    fixed_dofs = []
    fixed_vals = []
    for i in left.tolist():
        fixed_dofs += [2*i, 2*i+1]
        fixed_vals += [0.0, 0.0]
    for i in right.tolist():
        fixed_dofs += [2*i]
        fixed_vals += [0.2 * Lx]
    fixed_dofs = torch.tensor(fixed_dofs, dtype=torch.long)
    fixed_vals = torch.tensor(fixed_vals)
    Kb, fb = apply_dirichlet(K, f, fixed_dofs, fixed_vals)
    U = solve_linear_system(Kb, fb)
    ux = U[0::2]
    assert torch.isfinite(U).all()
    assert ux.max() > 0.35
