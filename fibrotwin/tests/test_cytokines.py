import torch
from src.remodeling.cytokines import build_knn_weights, update_cytokine_fields


def test_cytokine_diffusion_nonnegative_and_spreads():
    nodes = torch.tensor([[0.0, 0.0], [0.5, 0.0], [1.0, 0.0], [1.5, 0.0]], dtype=torch.float32)
    nbr, w = build_knn_weights(nodes, k=2, sigma=0.5)
    tgf = torch.zeros(4)
    chemo = torch.zeros(4)
    src_tgf = torch.tensor([1.0, 0.0, 0.0, 0.0])
    src_chemo = torch.zeros(4)

    for _ in range(20):
        tgf, chemo = update_cytokine_fields(tgf, chemo, dt=0.1, nbr=nbr, w=w, src_tgf_node=src_tgf, src_chemo_node=src_chemo)

    assert torch.all(tgf >= 0)
    assert tgf[1] > 0  # spread beyond source node
