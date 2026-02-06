"""
Fixed 4D Topology: Dynamic Spectral Dimension Unified Field Theory

A rigorous mathematical framework unifying fractal geometry, spectral theory,
modular forms, and algebraic topology.

Main Components:
- CantorRepresentation: Approximate real numbers using Cantor class fractals
- SpectralDimension: Compute and evolve spectral dimensions on fractals
- ModularCorrespondence: Weak correspondence between modular forms and fractals
- FractalArithmetic: Algebraic operations on fractal dimensions
"""

__version__ = "1.0.0"
__author__ = "AI Research Engine"
__license__ = "MIT"

from .cantor_representation import CantorRepresentation
from .spectral_dimension import SpectralDimension, HeatKernel
from .modular_correspondence import ModularCorrespondence, RamanujanFractal
from .fractal_arithmetic import FractalArithmetic, GrothendieckGroup

__all__ = [
    "CantorRepresentation",
    "SpectralDimension",
    "HeatKernel",
    "ModularCorrespondence",
    "RamanujanFractal",
    "FractalArithmetic",
    "GrothendieckGroup",
]
