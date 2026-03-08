import torch
from src.remodeling.infarct_maturation import init_infarct_states, update_infarct_states


def test_infarct_state_progression():
    mask = torch.tensor([1.0, 1.0, 0.0])
    infl, prov, scar = init_infarct_states(mask)
    assert infl[0] > 0 and prov[0] == 0 and scar[0] == 0

    for _ in range(40):
        infl, prov, scar = update_infarct_states(infl, prov, scar, dt=0.2, mask=mask, params={})

    # inflammation decays, scar grows
    assert infl[:2].mean() < 0.8
    assert scar[:2].mean() > 0.0
    # outside infarct stays zero
    assert infl[2] == 0 and prov[2] == 0 and scar[2] == 0
