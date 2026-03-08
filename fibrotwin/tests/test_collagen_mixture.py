import torch
from src.remodeling.collagen_mixture import update_collagen_cohorts


def test_collagen_mixture_turnover_and_maturation():
    c_y = torch.zeros(4)
    c_m = torch.zeros(4)
    dep = torch.tensor([1.0, 0.5, 0.0, 0.0])

    for _ in range(30):
        c_y, c_m, c = update_collagen_cohorts(c_y, c_m, dep_source=dep, dt=0.1, params={
            'k_maturation': 0.1,
            'k_deg_young': 0.02,
            'k_deg_mature': 0.005,
        })

    assert torch.all(c >= 0)
    assert c_m[0] > 0  # matured fraction accumulates
    assert c[0] > c[2]
