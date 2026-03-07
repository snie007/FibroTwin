import torch


def build_knn_weights(nodes: torch.Tensor, k: int = 8, sigma: float = 0.6):
    d = torch.cdist(nodes, nodes)
    idx = torch.topk(d, k=min(k + 1, nodes.shape[0]), largest=False).indices
    nbr = idx[:, 1:]  # drop self
    dn = torch.gather(d, 1, nbr)
    w = torch.exp(-0.5 * (dn / max(sigma, 1e-6)) ** 2)
    w = w / (w.sum(dim=1, keepdim=True) + 1e-12)
    return nbr, w


def graph_diffuse(field: torch.Tensor, nbr: torch.Tensor, w: torch.Tensor):
    fn = field[nbr]  # (n,k)
    smooth = (w * fn).sum(dim=1)
    return smooth - field


def update_cytokine_fields(
    tgf: torch.Tensor,
    chemo: torch.Tensor,
    dt: float,
    nbr: torch.Tensor,
    w: torch.Tensor,
    src_tgf_node: torch.Tensor,
    src_chemo_node: torch.Tensor,
    D_tgf: float = 0.15,
    D_chemo: float = 0.25,
    decay_tgf: float = 0.08,
    decay_chemo: float = 0.12,
):
    lap_tgf = graph_diffuse(tgf, nbr, w)
    lap_chemo = graph_diffuse(chemo, nbr, w)

    tgf2 = tgf + dt * (D_tgf * lap_tgf + src_tgf_node - decay_tgf * tgf)
    chemo2 = chemo + dt * (D_chemo * lap_chemo + src_chemo_node - decay_chemo * chemo)

    return torch.clamp(tgf2, 0.0, 1.0), torch.clamp(chemo2, 0.0, 1.0)
