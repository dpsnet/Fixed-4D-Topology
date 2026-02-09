"""
Dimension Visualization
=======================

Plotting utilities for effective dimension analysis.
"""

import numpy as np
import matplotlib.pyplot as plt
from typing import Optional, List, Dict
import seaborn as sns


def plot_eigenvalue_spectrum(eigenvalues: np.ndarray, 
                             title: str = "Fisher Eigenvalue Spectrum",
                             figsize: tuple = (10, 6),
                             save_path: Optional[str] = None):
    """
    Plot eigenvalue spectrum of Fisher Information Matrix.
    
    Args:
        eigenvalues: Array of eigenvalues (sorted descending)
        title: Plot title
        figsize: Figure size
        save_path: Path to save figure
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=figsize)
    
    # Linear scale
    ax1.plot(eigenvalues, 'b-', linewidth=2)
    ax1.set_xlabel('Index', fontsize=12)
    ax1.set_ylabel('Eigenvalue', fontsize=12)
    ax1.set_title('Linear Scale', fontsize=14)
    ax1.grid(True, alpha=0.3)
    
    # Log scale
    ax2.semilogy(eigenvalues, 'r-', linewidth=2)
    ax2.set_xlabel('Index', fontsize=12)
    ax2.set_ylabel('Eigenvalue (log)', fontsize=12)
    ax2.set_title('Log Scale', fontsize=14)
    ax2.grid(True, alpha=0.3)
    
    plt.suptitle(title, fontsize=16, fontweight='bold')
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    
    return fig


def plot_effective_dimension_comparison(
    results: Dict[str, Dict],
    figsize: tuple = (12, 6),
    save_path: Optional[str] = None
):
    """
    Compare effective dimensions across different models.
    
    Args:
        results: Dict of {model_name: {d_eff: float, total_params: int, ...}}
        figsize: Figure size
        save_path: Path to save figure
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=figsize)
    
    model_names = list(results.keys())
    d_effs = [r['fisher_effective_dimension'] for r in results.values()]
    total_params = [r['total_parameters'] for r in results.values()]
    reduction_ratios = [d/t for d, t in zip(d_effs, total_params)]
    
    # Effective dimension
    colors = sns.color_palette("husl", len(model_names))
    ax1.bar(model_names, d_effs, color=colors)
    ax1.set_ylabel('Effective Dimension', fontsize=12)
    ax1.set_title('Effective Dimension by Model', fontsize=14)
    ax1.tick_params(axis='x', rotation=45)
    
    # Reduction ratio
    ax2.bar(model_names, reduction_ratios, color=colors)
    ax2.set_ylabel('Reduction Ratio ($d_{eff} / D$)', fontsize=12)
    ax2.set_title('Dimension Reduction', fontsize=14)
    ax2.tick_params(axis='x', rotation=45)
    ax2.axhline(y=1.0, color='r', linestyle='--', alpha=0.5, label='No reduction')
    ax2.legend()
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    
    return fig


def plot_dimension_evolution(
    epochs: List[int],
    dimensions: Dict[str, List[float]],
    train_loss: Optional[List[float]] = None,
    test_loss: Optional[List[float]] = None,
    figsize: tuple = (14, 8),
    save_path: Optional[str] = None
):
    """
    Plot evolution of dimensions during training.
    
    Args:
        epochs: List of epoch numbers
        dimensions: Dict of {metric_name: [values]}
        train_loss: Training loss curve
        test_loss: Test loss curve
        figsize: Figure size
        save_path: Path to save figure
    """
    n_plots = 1 + (train_loss is not None)
    fig, axes = plt.subplots(1, n_plots, figsize=figsize, 
                            squeeze=False)
    
    # Dimension evolution
    ax = axes[0, 0]
    for metric_name, values in dimensions.items():
        ax.plot(epochs, values, label=metric_name, linewidth=2, marker='o')
    ax.set_xlabel('Epoch', fontsize=12)
    ax.set_ylabel('Dimension', fontsize=12)
    ax.set_title('Effective Dimension Evolution', fontsize=14)
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3)
    
    # Loss curves
    if train_loss is not None:
        ax = axes[0, 1]
        ax.plot(epochs, train_loss, 'b-', label='Train Loss', linewidth=2)
        if test_loss is not None:
            ax.plot(epochs, test_loss, 'r-', label='Test Loss', linewidth=2)
        ax.set_xlabel('Epoch', fontsize=12)
        ax.set_ylabel('Loss', fontsize=12)
        ax.set_title('Training Dynamics', fontsize=14)
        ax.legend(fontsize=10)
        ax.grid(True, alpha=0.3)
        ax.set_yscale('log')
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    
    return fig


def plot_generalization_vs_dimension(
    n_samples: List[int],
    d_effs: List[float],
    gen_errors: List[float],
    theoretical_curve: Optional[bool] = True,
    figsize: tuple = (10, 6),
    save_path: Optional[str] = None
):
    """
    Plot generalization error vs dimension for different sample sizes.
    
    Args:
        n_samples: List of training sample sizes
        d_effs: List of effective dimensions
        gen_errors: List of generalization errors
        theoretical_curve: Whether to plot theoretical bound
        figsize: Figure size
        save_path: Path to save figure
    """
    fig, ax = plt.subplots(figsize=figsize)
    
    # Scatter plot
    ax.scatter(d_effs, gen_errors, s=100, c=n_samples, 
              cmap='viridis', alpha=0.7, edgecolors='black')
    cbar = plt.colorbar(ax.collections[0], ax=ax)
    cbar.set_label('Training Samples (N)', fontsize=12)
    
    # Theoretical curve
    if theoretical_curve:
        d_range = np.linspace(min(d_effs), max(d_effs), 100)
        n_avg = np.mean(n_samples)
        theoretical = np.sqrt(d_range / n_avg)
        ax.plot(d_range, theoretical, 'r--', linewidth=2, 
               label=f'Theory: $\sqrt{{d_{{eff}}/N}}$, N={n_avg:.0f}')
    
    ax.set_xlabel('Effective Dimension ($d_{eff}$)', fontsize=12)
    ax.set_ylabel('Generalization Error', fontsize=12)
    ax.set_title('Generalization vs Effective Dimension', fontsize=14)
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    
    return fig


def plot_double_descent(
    model_complexities: List[float],
    train_errors: List[float],
    test_errors: List[float],
    d_effs: List[float],
    figsize: tuple = (12, 5),
    save_path: Optional[str] = None
):
    """
    Plot double descent phenomenon with dimension overlay.
    
    Args:
        model_complexities: List of model complexity (e.g., number of parameters)
        train_errors: Training errors
        test_errors: Test errors
        d_effs: Effective dimensions
        figsize: Figure size
        save_path: Path to save figure
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=figsize)
    
    # Double descent curves
    ax1.plot(model_complexities, train_errors, 'b-o', 
            label='Train Error', linewidth=2, markersize=6)
    ax1.plot(model_complexities, test_errors, 'r-s', 
            label='Test Error', linewidth=2, markersize=6)
    ax1.set_xlabel('Model Complexity (Number of Parameters)', fontsize=12)
    ax1.set_ylabel('Error', fontsize=12)
    ax1.set_title('Double Descent', fontsize=14)
    ax1.legend(fontsize=10)
    ax1.grid(True, alpha=0.3)
    
    # Dimension overlay
    ax2_twin = ax2.twinx()
    ax2.plot(model_complexities, test_errors, 'r-s', 
            label='Test Error', linewidth=2, markersize=6)
    ax2_twin.plot(model_complexities, d_effs, 'g-^', 
                 label='Effective Dim', linewidth=2, markersize=6)
    ax2.set_xlabel('Model Complexity', fontsize=12)
    ax2.set_ylabel('Test Error', fontsize=12, color='r')
    ax2_twin.set_ylabel('Effective Dimension', fontsize=12, color='g')
    ax2.set_title('Test Error vs Effective Dimension', fontsize=14)
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    
    return fig
