"""Standard neural network architectures for dimension analysis."""

from .standard_architectures import (
    TwoLayerMLP,
    DeepMLP,
    SimpleConvNet,
    ResNet18,
    VGG19,
)
from .lottery_ticket import LotteryTicketNetwork

__all__ = [
    "TwoLayerMLP",
    "DeepMLP", 
    "SimpleConvNet",
    "ResNet18",
    "VGG19",
    "LotteryTicketNetwork",
]
