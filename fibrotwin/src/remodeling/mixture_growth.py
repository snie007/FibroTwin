import torch


def update_growth(g, c, dt, k_g=0.01, k_r=0.005):
    g2 = g + dt * (k_g * c - k_r * g)
    return torch.clamp(g2, min=0.0)


def element_E_from_fields(base_E, c_elem, g_elem, alpha_c=2.0, beta_g=0.5):
    return base_E * (1.0 + alpha_c * c_elem) * (1.0 + beta_g * g_elem)
