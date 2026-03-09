import math
import torch
from src.remodeling.signaling_network import update_signaling_network


def test_smad_linear_closed_form_in_decoupled_case():
    n = 5
    smad = torch.ones(n) * 0.2
    z = torch.zeros(n)
    tgf = torch.ones(n) * 0.7
    params = {
        'k_tgf_smad': 1.3,
        'k_ros_smad': 0.0,
        'k_smad_autocrine': 0.0,
        'k_ang_erk': 0.0,
        'k_mech_ros': 0.0,
        'k_mech_can': 0.0,
        'd_smad': 0.4,
        'd_erk': 1.0,
        'd_ros': 1.0,
        'd_can': 1.0,
    }

    dt = 0.001
    steps = 2000
    for _ in range(steps):
        smad, _, _, _, _ = update_signaling_network(smad, z, z, z, dt, tgf, z, z, params)

    a = params['k_tgf_smad'] * 0.7
    b = params['d_smad']
    s0 = 0.2
    T = dt * steps
    # ds/dt = a - (a+b)s
    s_exact = (s0 - a/(a+b))*math.exp(-(a+b)*T) + a/(a+b)
    assert torch.allclose(smad, torch.ones_like(smad)*s_exact, atol=2e-2)
