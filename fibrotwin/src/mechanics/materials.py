import torch


def constitutive_matrix(E: float, nu: float, plane_stress: bool = True, device=None):
    if plane_stress:
        c = E / (1 - nu ** 2)
        D = torch.tensor([
            [1, nu, 0],
            [nu, 1, 0],
            [0, 0, (1 - nu) / 2],
        ], dtype=torch.float32, device=device) * c
    else:
        c = E / ((1 + nu) * (1 - 2 * nu))
        D = torch.tensor([
            [1 - nu, nu, 0],
            [nu, 1 - nu, 0],
            [0, 0, (1 - 2 * nu) / 2],
        ], dtype=torch.float32, device=device) * c
    return D
