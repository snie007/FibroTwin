import torch
from src.remodeling.signaling_network import update_signaling_network


def test_mech_signal_synergy_increases_profibrotic_output():
    n = 8
    z = torch.zeros(n)
    params = {}
    dt = 0.05

    # signal only
    sm, er, ro, ca, p_sig = update_signaling_network(z.clone(), z.clone(), z.clone(), z.clone(), dt,
                                                     tgf=torch.ones(n)*0.8,
                                                     ang_eff=torch.ones(n)*0.7,
                                                     mech_cue=torch.zeros(n),
                                                     params=params)
    # mech + signal
    sm2, er2, ro2, ca2, p_both = update_signaling_network(z.clone(), z.clone(), z.clone(), z.clone(), dt,
                                                          tgf=torch.ones(n)*0.8,
                                                          ang_eff=torch.ones(n)*0.7,
                                                          mech_cue=torch.ones(n)*0.9,
                                                          params=params)
    assert p_both.mean() > p_sig.mean()
