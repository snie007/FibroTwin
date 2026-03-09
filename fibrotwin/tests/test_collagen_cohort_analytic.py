import torch
from src.remodeling.collagen_mixture import update_collagen_cohorts


def test_collagen_cohort_matches_linear_system_reference():
    cy = torch.tensor([0.0])
    cm = torch.tensor([0.0])
    dep = torch.tensor([1.0])
    params = {'k_maturation': 0.08, 'k_deg_young': 0.02, 'k_deg_mature': 0.01}

    dt = 0.002
    steps = 3000
    for _ in range(steps):
        cy, cm, c = update_collagen_cohorts(cy, cm, dep, dt, params)

    # high-resolution reference using same equations with finer dt
    cy_r = torch.tensor([0.0])
    cm_r = torch.tensor([0.0])
    dt_r = 0.0002
    ref_steps = int(steps * dt / dt_r)
    for _ in range(ref_steps):
        cy_r, cm_r, _ = update_collagen_cohorts(cy_r, cm_r, dep, dt_r, params)

    assert torch.allclose(cy, cy_r, atol=1e-2)
    assert torch.allclose(cm, cm_r, atol=1e-2)
