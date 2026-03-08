from dataclasses import dataclass
import torch


@dataclass
class FieldState:
    c: torch.Tensor
    a: torch.Tensor
    ac: torch.Tensor
    g: torch.Tensor
    p: torch.Tensor
    tgf: torch.Tensor
    chemo: torch.Tensor
    smad: torch.Tensor
    erk: torch.Tensor
    ros: torch.Tensor
    can: torch.Tensor


def init_fields(n_nodes: int, device: torch.device, seed: int = 0) -> FieldState:
    gen = torch.Generator(device='cpu').manual_seed(seed)
    a = torch.randn((n_nodes, 2), generator=gen)
    a = a / (a.norm(dim=1, keepdim=True) + 1e-12)
    z = torch.zeros(n_nodes, device=device)
    return FieldState(
        c=z.clone(),
        a=a.to(device),
        ac=a.clone().to(device),
        g=z.clone(),
        p=z.clone(),
        tgf=z.clone(),
        chemo=z.clone(),
        smad=z.clone(),
        erk=z.clone(),
        ros=z.clone(),
        can=z.clone(),
    )
