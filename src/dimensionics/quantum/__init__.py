"""
Quantum Dimension Module (H)

Quantum entanglement and dimension using iTEBD (infinite Time-Evolving Block Decimation).
Validates Bridge C (unitary equivalence).
"""

from .itebd import iTEBD_Simulator, quantum_dimension
from .entanglement import entanglement_entropy, correlation_length

__all__ = [
    "iTEBD_Simulator",
    "quantum_dimension",
    "entanglement_entropy",
    "correlation_length",
]
