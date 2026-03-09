import torch
from src.remodeling.receptor_signaling import update_receptors, update_signaling_from_receptors


def test_receptor_activation_under_ligand():
    z = torch.zeros(5)
    tgfr, at1r = z.clone(), z.clone()
    for _ in range(50):
        tgfr, at1r = update_receptors(tgfr, at1r, dt=0.05, tgf=torch.ones(5)*0.8, ang=torch.ones(5)*0.7, params={})
    assert tgfr.mean() > 0.3
    assert at1r.mean() > 0.3


def test_signaling_from_receptors_increases_p():
    z = torch.zeros(4)
    sm, er, ro, ca, p = update_signaling_from_receptors(z, z, z, z, dt=0.1, tgfr=torch.ones(4)*0.9, at1r=torch.ones(4)*0.8, mech_cue=torch.ones(4)*0.2, params={})
    assert p.mean() > 0.05
