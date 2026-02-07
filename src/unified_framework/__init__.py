"""
Unified Dimensionics Framework
=============================

Fusion of A~G Research Directions and Fixed-4D-Topology

This module provides unified implementations of:
- A: Spectral Zeta Functions
- B: Dimension Flow Equations  
- C: Modular-Fractal Correspondence
- D: PTE Arithmetic
- E: Sobolev Spaces on Fractals
- F: Fractal Complexity
- G: Variational Principles
- T1: Cantor Representation
- T2: Spectral Dimension PDE
- T3: Modular-Fractal Weak Correspondence
- T4: Fractal Arithmetic
"""

__version__ = "1.0.0"
__author__ = "A~G Research Team & Fixed-4D-Topology Team"

# Import core modules
from .core import (
    Dimension,
    SpectralDimension,
    VariationalPrinciple,
)

from .algebraic import (
    GrothendieckGroup,
    FractalElement,
)

from .analytic import (
    SobolevSpace,
    ExtensionOperator,
)

from .evolution import (
    DimensionFlow,
    SpectralPDE,
)

from .number_theory import (
    ModularCorrespondence,
    PTEAnalyzer,
)

from .complexity import (
    FComplexity,
    FNPComplete,
)

__all__ = [
    'Dimension',
    'SpectralDimension', 
    'VariationalPrinciple',
    'GrothendieckGroup',
    'FractalElement',
    'SobolevSpace',
    'ExtensionOperator',
    'DimensionFlow',
    'SpectralPDE',
    'ModularCorrespondence',
    'PTEAnalyzer',
    'FComplexity',
    'FNPComplete',
]
