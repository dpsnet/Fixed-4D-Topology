"""
Dimensionics: Core Mathematical Theory (Strict Foundation)

This package provides the rigorous mathematical core of Dimensionics theory.

Strict Modules (L1-L2):
    core: Master equation, spectral formulas, convexity (T2-T3)
    number_theory: Cantor approximation (T1)
    topology: Spectral dimension, algebraic topology (T4)

Note: Extended directions (H-K) and Bridge hypotheses have been removed
as they did not meet strict L1/L2 standards.

Version: 3.0.0-core (strict foundation only)
"""

__version__ = "3.0.0-core"
__author__ = "Wang Bin & Research Team"
__license__ = "MIT"

# Core strict modules only
from dimensionics.core import (
    MasterEquation,
    SpectralDimension,
    ConvexityAnalyzer,
    DimensionFlow,
)

from dimensionics.number_theory import (
    CantorApproximation,
    ComplexityAnalyzer,
)

from dimensionics.topology import (
    SpectralTopology,
    IndexTheoremValidator,
)

__all__ = [
    "__version__",
    # Core (T2-T3)
    "MasterEquation",
    "SpectralDimension",
    "ConvexityAnalyzer",
    "DimensionFlow",
    # Number Theory (T1)
    "CantorApproximation",
    "ComplexityAnalyzer",
    # Topology (T4)
    "SpectralTopology",
    "IndexTheoremValidator",
]
