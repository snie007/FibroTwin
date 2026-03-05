from dataclasses import dataclass
import torch


@dataclass
class FieldState:
    c: torch.Tensor
    a: torch.Tensor
    ac: torch.Tensor
    g: torch.Tensor


def init_fields(n_nodes: int, device: torch.device, seed: int = 0) -> FieldState:
    gen = torch.Generator(device='cpu').manual_seed(seed)
    a = torch.randn((n_nodes, 2), generator=gen)
    a = a / (a.norm(dim=1, keepdim=True) + 1e-12)
    return FieldState(
        c=torch.zeros(n_nodes, device=device),
        a=a.to(device),
        ac=a.clone().to(device),
        g=torch.zeros(n_nodes, device=device),
    )
