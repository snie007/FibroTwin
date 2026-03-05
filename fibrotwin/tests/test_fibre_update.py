import torch
from src.remodeling.fibre_reorientation import update_fibres


def test_fibre_converges_to_target():
    a = torch.tensor([[1.0, 0.0]])
    target = torch.tensor([[0.0, 1.0]])
    for _ in range(200):
        a = update_fibres(a, target, dt=0.1, tau=5.0)
    assert a[0, 1] > 0.95
    assert torch.isclose(torch.norm(a, dim=1), torch.tensor([1.0]), atol=1e-5).all()
