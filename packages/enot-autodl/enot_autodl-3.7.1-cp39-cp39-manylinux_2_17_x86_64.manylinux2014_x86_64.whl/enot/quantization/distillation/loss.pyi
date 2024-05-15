import torch
from _typeshed import Incomplete
from torch import nn

class RMSELoss(nn.Module):
    """RMSE loss."""
    mse: Incomplete
    eps: Incomplete
    def __init__(self, eps: float = 1e-06) -> None: ...
    def forward(self, inputs: torch.Tensor, target: torch.Tensor) -> torch.Tensor: ...
