import math
import torch
from src.remodeling.cytokines import build_knn_weights, update_cytokine_fields


def test_cytokine_zero_diffusion_matches_closed_form():
    nodes = torch.tensor([[0.0,0.0],[1.0,0.0],[2.0,0.0]], dtype=torch.float32)
    nbr, w = build_knn_weights(nodes, k=2, sigma=1.0)

    tgf = torch.ones(3) * 0.3
    chemo = torch.ones(3) * 0.4
    src_tgf = torch.ones(3) * 0.2
    src_chemo = torch.ones(3) * 0.1
    dt = 0.01
    n = 200
    decay_tgf = 0.08
    decay_chemo = 0.12

    for _ in range(n):
        tgf, chemo = update_cytokine_fields(
            tgf, chemo, dt=dt, nbr=nbr, w=w,
            src_tgf_node=src_tgf, src_chemo_node=src_chemo,
            D_tgf=0.0, D_chemo=0.0,
            decay_tgf=decay_tgf, decay_chemo=decay_chemo,
        )

    T = n * dt
    tgf_exact = (0.3 - 0.2/decay_tgf) * math.exp(-decay_tgf*T) + 0.2/decay_tgf
    chemo_exact = (0.4 - 0.1/decay_chemo) * math.exp(-decay_chemo*T) + 0.1/decay_chemo

    assert torch.allclose(tgf, torch.ones_like(tgf)*tgf_exact, atol=2e-2)
    assert torch.allclose(chemo, torch.ones_like(chemo)*chemo_exact, atol=2e-2)
