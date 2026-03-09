import torch


def update_receptors(tgf_r, at1r, dt, tgf, ang, params):
    kon_t = params.get('kon_tgfr', 1.2)
    koff_t = params.get('koff_tgfr', 0.5)
    kon_a = params.get('kon_at1r', 1.0)
    koff_a = params.get('koff_at1r', 0.45)

    tgfr2 = tgf_r + dt * (kon_t * tgf * (1 - tgf_r) - koff_t * tgf_r)
    at1r2 = at1r + dt * (kon_a * ang * (1 - at1r) - koff_a * at1r)
    return torch.clamp(tgfr2, 0.0, 1.0), torch.clamp(at1r2, 0.0, 1.0)


def update_signaling_from_receptors(smad, erk, ros, can, dt, tgfr, at1r, mech_cue, params):
    k_tgfr_smad = params.get('k_tgfr_smad', 1.2)
    k_at1r_erk = params.get('k_at1r_erk', 1.0)
    k_mech_ros = params.get('k_mech_ros', 1.0)
    k_mech_can = params.get('k_mech_can', 0.8)
    d_smad = params.get('d_smad', 0.4)
    d_erk = params.get('d_erk', 0.5)
    d_ros = params.get('d_ros', 0.45)
    d_can = params.get('d_can', 0.5)

    drive_smad = k_tgfr_smad * tgfr + 0.25 * ros
    drive_erk = k_at1r_erk * at1r + 0.1 * tgfr
    drive_ros = k_mech_ros * torch.clamp(mech_cue, min=0.0) + 0.12 * erk
    drive_can = k_mech_can * torch.clamp(mech_cue, min=0.0) + 0.08 * tgfr

    sm2 = smad + dt * (drive_smad * (1 - smad) - d_smad * smad)
    er2 = erk + dt * (drive_erk * (1 - erk) - d_erk * erk)
    ro2 = ros + dt * (drive_ros * (1 - ros) - d_ros * ros)
    ca2 = can + dt * (drive_can * (1 - can) - d_can * can)

    sm2 = torch.clamp(sm2, 0.0, 1.0)
    er2 = torch.clamp(er2, 0.0, 1.0)
    ro2 = torch.clamp(ro2, 0.0, 1.0)
    ca2 = torch.clamp(ca2, 0.0, 1.0)

    p = torch.clamp(0.45*sm2 + 0.2*er2 + 0.2*ro2 + 0.15*ca2, 0.0, 1.0)
    return sm2, er2, ro2, ca2, p
