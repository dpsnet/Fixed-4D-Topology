"""
Dimensionics: A Unified Mathematical Theory of Dimension

This package provides numerical implementations of the Dimensionics theory,
unifying 16+ research directions across mathematics and physics.

Modules:
    core: Master equation, spectral formulas, convexity
    number_theory: Cantor approximation, p-adic analysis, complexity
    cosmology: Master equation, gravitational waves, simulations
    qft: Convexity analysis, string theory, F-theory
    topology: Spectral dimension, algebraic topology, index theorems
    bridges: Final 5% first-principles unification

Example:
    >>> from dimensionics import MasterEquation
    >>> me = MasterEquation(alpha=0.5, beta=0.3)
    >>> d_s = me.solve(initial_d=4, t_span=10)
"""

__version__ = "3.0.0"
__author__ = "Fixed-4D-Topology Consortium"
__license__ = "MIT"

# Core imports
from dimensionics.core import (
    MasterEquation,
    SpectralDimension,
    ConvexityAnalyzer,
    DimensionFlow,
)

# Number theory
from dimensionics.number_theory import (
    CantorApproximation,
    ComplexityAnalyzer,
)

# Cosmology
from dimensionics.cosmology import (
    CosmologicalSimulator,
    GravitationalWavePredictor,
)

# QFT
from dimensionics.qft import (
    ConvexityQFT,
    StringTheoryConnection,
)

# Topology
from dimensionics.topology import (
    SpectralTopology,
    IndexTheoremValidator,
)

# Bridges
from dimensionics.bridges import (
    BridgeA_FractalLaplacian,
    BridgeB_VariationalWeights,
    BridgeC_NetworkNeuralIsomorphism,
)

__all__ = [
    # Version
    "__version__",
    # Core
    "MasterEquation",
    "SpectralDimension", 
    "ConvexityAnalyzer",
    "DimensionFlow",
    # Number Theory
    "CantorApproximation",
    "ComplexityAnalyzer",
    # Cosmology
    "CosmologicalSimulator",
    "GravitationalWavePredictor",
    # QFT
    "ConvexityQFT",
    "StringTheoryConnection",
    # Topology
    "SpectralTopology",
    "IndexTheoremValidator",
    # Bridges
    "BridgeA_FractalLaplacian",
    "BridgeB_VariationalWeights",
    "BridgeC_NetworkNeuralIsomorphism",
]
