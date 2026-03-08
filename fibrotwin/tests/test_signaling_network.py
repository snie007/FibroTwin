import torch
from src.remodeling.signaling_network import update_signaling_network


def test_tgf_increases_smad():
    z = torch.zeros(5)
    smad, erk, ros, can, p = update_signaling_network(
        z.clone(), z.clone(), z.clone(), z.clone(),
        dt=0.2,
        tgf=torch.ones(5) * 0.8,
        ang_eff=torch.zeros(5),
        mech_cue=torch.zeros(5),
        params={},
    )
    assert smad.mean() > 0.05
    assert torch.all((p >= 0) & (p <= 1))


def test_mech_increases_ros_and_can():
    z = torch.zeros(6)
    smad, erk, ros, can, p = update_signaling_network(
        z.clone(), z.clone(), z.clone(), z.clone(),
        dt=0.2,
        tgf=torch.zeros(6),
        ang_eff=torch.zeros(6),
        mech_cue=torch.ones(6) * 0.9,
        params={},
    )
    assert ros.mean() > 0.05
    assert can.mean() > 0.05
