"""
Final 5% Bridges Module

First-principles derivations eliminating phenomenological parameters.
"""

from .bridge_a_fractal_laplacian import BridgeA_FractalLaplacian
from .bridge_b_variational_weights import BridgeB_VariationalWeights
from .bridge_c_network_neural import BridgeC_NetworkNeuralIsomorphism

__all__ = [
    "BridgeA_FractalLaplacian",
    "BridgeB_VariationalWeights",
    "BridgeC_NetworkNeuralIsomorphism",
]
