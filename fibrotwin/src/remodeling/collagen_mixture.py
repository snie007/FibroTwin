import torch


def update_collagen_cohorts(c_young, c_mature, dep_source, dt, params):
    # constrained-mixture-inspired two-cohort turnover model
    k_mat = params.get('k_maturation', 0.06)  # young -> mature
    k_deg_y = params.get('k_deg_young', 0.02)
    k_deg_m = params.get('k_deg_mature', 0.008)

    c_y2 = c_young + dt * dep_source - dt * k_mat * c_young - dt * k_deg_y * c_young
    c_m2 = c_mature + dt * k_mat * c_young - dt * k_deg_m * c_mature
    c_y2 = torch.clamp(c_y2, 0.0)
    c_m2 = torch.clamp(c_m2, 0.0)
    c_total = c_y2 + c_m2
    return c_y2, c_m2, c_total
