import torch


def init_infarct_states(mask: torch.Tensor):
    # Start with inflammatory phase in infarct region
    infl = mask.clone()
    prov = torch.zeros_like(mask)
    scar = torch.zeros_like(mask)
    return infl, prov, scar


def update_infarct_states(infl, prov, scar, dt: float, mask: torch.Tensor, params: dict):
    k_ip = params.get('k_infl_to_prov', 0.12)
    k_ps = params.get('k_prov_to_scar', 0.06)
    k_ir = params.get('k_infl_resolve', 0.05)
    k_pr = params.get('k_prov_resolve', 0.03)

    # simple maturation chain: inflammation -> provisional matrix -> scar
    d_infl = -k_ip * infl - k_ir * infl
    d_prov = k_ip * infl - k_ps * prov - k_pr * prov
    d_scar = k_ps * prov

    infl2 = infl + dt * d_infl
    prov2 = prov + dt * d_prov
    scar2 = scar + dt * d_scar

    infl2 = torch.clamp(infl2, 0.0, 1.0) * mask
    prov2 = torch.clamp(prov2, 0.0, 1.0) * mask
    scar2 = torch.clamp(scar2, 0.0, 1.0) * mask
    return infl2, prov2, scar2


def infarct_softening_factor(infl, prov, scar, base_softening=0.6):
    # Softer early infarct; partial stiffening as scar matures
    eff = base_softening * torch.clamp(0.8 * infl + 0.5 * prov + 0.2 * scar, 0.0, 1.0)
    return eff


def infarct_signal_source(infl, prov, scar, base_signal=0.2):
    # Strongest biochemical drive early; decays with maturation
    return base_signal * torch.clamp(1.2 * infl + 0.6 * prov + 0.2 * scar, 0.0, 2.0)
