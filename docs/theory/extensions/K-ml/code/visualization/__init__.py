"""Visualization tools for neural dimension analysis."""

from .dimension_plots import (
    plot_eigenvalue_spectrum,
    plot_effective_dimension_comparison,
    plot_dimension_evolution,
    plot_generalization_vs_dimension,
)
from .training_dynamics import plot_training_dynamics

__all__ = [
    "plot_eigenvalue_spectrum",
    "plot_effective_dimension_comparison",
    "plot_dimension_evolution",
    "plot_generalization_vs_dimension",
    "plot_training_dynamics",
]
