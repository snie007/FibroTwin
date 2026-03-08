import torch


def update_signaling_network(
    smad: torch.Tensor,
    erk: torch.Tensor,
    ros: torch.Tensor,
    can: torch.Tensor,
    dt: float,
    tgf: torch.Tensor,
    ang_eff: torch.Tensor,
    mech_cue: torch.Tensor,
    params: dict,
):
    # compact multi-node phenomenological network
    k_tgf_smad = params.get('k_tgf_smad', 1.2)
    k_ros_smad = params.get('k_ros_smad', 0.3)
    k_ang_erk = params.get('k_ang_erk', 1.0)
    k_mech_ros = params.get('k_mech_ros', 1.0)
    k_mech_can = params.get('k_mech_can', 0.8)
    k_smad_autocrine = params.get('k_smad_autocrine', 0.2)

    d_smad = params.get('d_smad', 0.4)
    d_erk = params.get('d_erk', 0.5)
    d_ros = params.get('d_ros', 0.45)
    d_can = params.get('d_can', 0.5)

    drive_smad = k_tgf_smad * tgf + k_ros_smad * ros + k_smad_autocrine * smad
    drive_erk = k_ang_erk * ang_eff + 0.2 * tgf
    drive_ros = k_mech_ros * torch.clamp(mech_cue, min=0.0) + 0.15 * erk
    drive_can = k_mech_can * torch.clamp(mech_cue, min=0.0) + 0.1 * tgf

    smad2 = smad + dt * (drive_smad * (1.0 - smad) - d_smad * smad)
    erk2 = erk + dt * (drive_erk * (1.0 - erk) - d_erk * erk)
    ros2 = ros + dt * (drive_ros * (1.0 - ros) - d_ros * ros)
    can2 = can + dt * (drive_can * (1.0 - can) - d_can * can)

    smad2 = torch.clamp(smad2, 0.0, 1.0)
    erk2 = torch.clamp(erk2, 0.0, 1.0)
    ros2 = torch.clamp(ros2, 0.0, 1.0)
    can2 = torch.clamp(can2, 0.0, 1.0)

    p = torch.clamp(
        0.45 * smad2 + 0.20 * erk2 + 0.20 * ros2 + 0.15 * can2,
        0.0,
        1.0,
    )
    return smad2, erk2, ros2, can2, p
