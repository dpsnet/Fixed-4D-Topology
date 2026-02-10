"""
Network Geometry Module (I)

Spectral dimension analysis in complex networks.
Validates Bridge B (network weight formula).
"""

from .spectral import network_spectral_dimension, laplacian_eigenvalues
from .analysis import analyze_network, effective_network_dimension

__all__ = [
    "network_spectral_dimension",
    "laplacian_eigenvalues",
    "analyze_network",
    "effective_network_dimension",
]
