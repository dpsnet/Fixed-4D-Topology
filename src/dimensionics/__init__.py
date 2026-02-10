"""
Dimensionics: A Unified Mathematical Theory of Dimension

This package provides numerical implementations of the Dimensionics theory,
unifying 16+ research directions across mathematics and physics.

Modules:
    core: Master equation, spectral formulas, convexity (T1-T4)
    number_theory: Cantor approximation, p-adic analysis, complexity
    topology: Spectral dimension, algebraic topology, index theorems
    qft: Convexity analysis, string theory, F-theory
    cosmology: Master equation, gravitational waves, simulations
    bridges: Final 5% first-principles unification (A, B, C)
    quantum: Quantum dimension, iTEBD (H)
    network: Network geometry, spectral analysis (I)
    fractal: Random fractals, percolation (J)
    neural_network: Effective dimension, Fisher information (K)

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

# Extended directions
from dimensionics.quantum import (
    iTEBD_Simulator,
    quantum_dimension,
)

from dimensionics.network import (
    network_spectral_dimension,
    analyze_network,
)

from dimensionics.fractal import (
    percolation_3d,
    critical_exponent,
)

from dimensionics.neural_network import (
    effective_dimension,
    fisher_information_matrix,
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
    # Topology
    "SpectralTopology",
    "IndexTheoremValidator",
    # QFT
    "ConvexityQFT",
    "StringTheoryConnection",
    # Cosmology
    "CosmologicalSimulator",
    "GravitationalWavePredictor",
    # Bridges
    "BridgeA_FractalLaplacian",
    "BridgeB_VariationalWeights",
    "BridgeC_NetworkNeuralIsomorphism",
    # Extended Directions
    "iTEBD_Simulator",
    "quantum_dimension",
    "network_spectral_dimension",
    "analyze_network",
    "percolation_3d",
    "critical_exponent",
    "effective_dimension",
    "fisher_information_matrix",
]
