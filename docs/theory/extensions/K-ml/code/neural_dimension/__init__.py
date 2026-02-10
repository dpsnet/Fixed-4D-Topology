"""
Neural Dimension Toolkit
========================

A Python package for analyzing the effective dimension of neural networks
and connecting to the Dimensionics framework.

Main Components:
- core: Fisher information and effective dimension computation
- models: Standard neural network architectures
- visualization: Plotting tools for dimension analysis
- experiments: Reproducible experiments for theory validation

Author: Kimi 2.5 Agent (AI Research Assistant)
Human Supervision: Research Direction and Quality Control
"""

__version__ = "0.1.0"
__author__ = "K Machine Learning Dimension Research Team"

from .core.fisher_information import FisherInformationMatrix
from .core.effective_dimension import EffectiveDimensionCalculator
from .core.dimension_dynamics import DimensionTracker

__all__ = [
    "FisherInformationMatrix",
    "EffectiveDimensionCalculator", 
    "DimensionTracker",
]
