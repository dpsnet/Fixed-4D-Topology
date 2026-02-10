"""
Core Dimensionics Module

Implements the fundamental equations and concepts of Dimensionics theory.
"""

from .master_equation import MasterEquation
from .spectral_dimension import SpectralDimension
from .convexity import ConvexityAnalyzer
from .dimension_flow import DimensionFlow

__all__ = [
    "MasterEquation",
    "SpectralDimension",
    "ConvexityAnalyzer",
    "DimensionFlow",
]
