import torch


def update_profibrotic_signal(p, mech_cue, dt, tgf_beta=0.2, angII=0.2, mech_gain=1.0, decay=0.3):
    # p in [0,1], mechanochemical drive inspired by fibroblast signaling abstractions
    drive = tgf_beta + angII + mech_gain * torch.clamp(mech_cue, min=0.0)
    dp = drive * (1.0 - p) - decay * p
    p_new = p + dt * dp
    return torch.clamp(p_new, 0.0, 1.0)
