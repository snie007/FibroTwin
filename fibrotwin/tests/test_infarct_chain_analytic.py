import torch
from src.remodeling.infarct_maturation import init_infarct_states, update_infarct_states


def test_infarct_chain_matches_matrix_exponential_reference():
    mask = torch.tensor([1.0])
    infl, prov, scar = init_infarct_states(mask)
    params = {'k_infl_to_prov': 0.12, 'k_prov_to_scar': 0.06, 'k_infl_resolve': 0.05, 'k_prov_resolve': 0.03}

    dt = 0.001
    steps = 3000
    for _ in range(steps):
        infl, prov, scar = update_infarct_states(infl, prov, scar, dt, mask, params)

    # linear system reference: xdot = A x
    kip, kps, kir, kpr = params['k_infl_to_prov'], params['k_prov_to_scar'], params['k_infl_resolve'], params['k_prov_resolve']
    A = torch.tensor([
        [-(kip+kir), 0.0, 0.0],
        [kip, -(kps+kpr), 0.0],
        [0.0, kps, 0.0],
    ], dtype=torch.float64)
    x0 = torch.tensor([1.0, 0.0, 0.0], dtype=torch.float64)
    T = dt * steps
    x_ref = torch.matrix_exp(A*T) @ x0

    x_num = torch.tensor([infl.item(), prov.item(), scar.item()], dtype=torch.float64)
    assert torch.allclose(x_num, x_ref, atol=2e-2)
