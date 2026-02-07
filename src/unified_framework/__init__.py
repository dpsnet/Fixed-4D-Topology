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
- H: Quantum Dimensions
- I: Network Geometry (NEW - 2.1M nodes empirical study)
- J: Random Fractals
- T1: Cantor Representation
- T2: Spectral Dimension PDE
- T3: Modular-Fractal Weak Correspondence
- T4: Fractal Arithmetic
"""

__version__ = "2.0.0"
__author__ = "A~G Research Team & Fixed-4D-Topology Team"

# Import core modules
from .core import (
    Dimension,
    VariationalPrinciple,
    DimensionicsFramework,
    master_equation,
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

# NEW: I Direction - Network Geometry
from .network import (
    NetworkDimension,
    NetworkMasterEquation,
    EMPIRICAL_NETWORK_DATA,
    get_empirical_data,
    compare_to_empirical,
)

__all__ = [
    # Core
    'Dimension',
    'VariationalPrinciple',
    'DimensionicsFramework',
    'master_equation',
    # Algebraic
    'GrothendieckGroup',
    'FractalElement',
    # Analytic
    'SobolevSpace',
    'ExtensionOperator',
    # Evolution
    'DimensionFlow',
    'SpectralPDE',
    # Number Theory
    'ModularCorrespondence',
    'PTEAnalyzer',
    # Complexity
    'FComplexity',
    'FNPComplete',
    # Network Geometry (I Direction)
    'NetworkDimension',
    'NetworkMasterEquation',
    'EMPIRICAL_NETWORK_DATA',
    'get_empirical_data',
    'compare_to_empirical',
]
