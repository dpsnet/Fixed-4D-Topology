"""
Neural Network Effective Dimension Module (K)

Effective dimension of neural networks using Fisher information approach.
Applies Bridge B (weight formulas).
"""

from .fisher_information import effective_dimension, fisher_information_matrix
from .analysis import analyze_network_architecture, dimension_dynamics

__all__ = [
    "effective_dimension",
    "fisher_information_matrix",
    "analyze_network_architecture",
    "dimension_dynamics",
]
