"""
Fixed 4D Topology: Dynamic Spectral Dimension Unified Field Theory

A rigorous mathematical framework unifying fractal geometry, spectral theory,
modular forms, and algebraic topology through the lens of dynamic spectral dimension.

Main Components:
- CantorRepresentation: Approximate real numbers using Cantor class fractal dimensions
- SpectralDimension: Compute and evolve spectral dimensions on fractals
- ModularCorrespondence: Weak correspondence between modular forms and fractals
- FractalArithmetic: Algebraic operations on fractal dimensions

Example:
    >>> from fixed_4d_topology import CantorRepresentation, SpectralDimension
    >>> 
    >>> # T1: Cantor representation approximation
    >>> rep = CantorRepresentation()
    >>> result = rep.approximate(alpha=0.5, epsilon=1e-6)
    >>> print(f"Approximation: {result.approximation}")
    
    >>> # T2: Spectral dimension evolution
    >>> spec = SpectralDimension("sierpinski")
    >>> d_s = spec.compute_spectral_dimension(t=1e-5)
    >>> print(f"Spectral dimension: {d_s}")

References:
- GitHub: https://github.com/dpsnet/Fixed-4D-Topology
- Documentation: https://github.com/dpsnet/Fixed-4D-Topology/tree/main/docs
- Papers: https://github.com/dpsnet/Fixed-4D-Topology/tree/main/papers
"""

__version__ = "1.0.1"
__author__ = "AI Research Engine"
__email__ = "research@fixed4dtopology.org"
__license__ = "MIT"
__url__ = "https://github.com/dpsnet/Fixed-4D-Topology"

# Core modules
from .cantor_representation import CantorRepresentation, CantorApproximation
from .spectral_dimension import SpectralDimension, HeatKernel, SpectralEvolutionResult
from .modular_correspondence import ModularCorrespondence, RamanujanFractal, CorrespondenceResult
from .fractal_arithmetic import FractalArithmetic, GrothendieckGroup, FractalElement

# Version info
def get_version() -> str:
    """Return the version string."""
    return __version__

def get_info() -> dict:
    """Return package information."""
    return {
        "name": "fixed-4d-topology",
        "version": __version__,
        "author": __author__,
        "email": __email__,
        "license": __license__,
        "url": __url__,
    }

__all__ = [
    # Version
    "__version__",
    "get_version",
    "get_info",
    # T1: Cantor Representation
    "CantorRepresentation",
    "CantorApproximation",
    # T2: Spectral Dimension
    "SpectralDimension",
    "HeatKernel",
    "SpectralEvolutionResult",
    # T3: Modular Correspondence
    "ModularCorrespondence",
    "RamanujanFractal",
    "CorrespondenceResult",
    # T4: Fractal Arithmetic
    "FractalArithmetic",
    "GrothendieckGroup",
    "FractalElement",
]
