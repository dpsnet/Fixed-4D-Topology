"""
Random Fractals Module (J)

Percolation theory and random fractal structures.
Validates Bridge A (critical exponent C*).
"""

from .percolation import percolation_3d, critical_exponent
from .random_cantor import random_cantor_set, fractal_dimension

__all__ = [
    "percolation_3d",
    "critical_exponent",
    "random_cantor_set",
    "fractal_dimension",
]
