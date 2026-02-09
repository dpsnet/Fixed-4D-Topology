#!/usr/bin/env python3
"""
P3-T1: Convexity Analysis of Energy Functional
Variational Methods in Dimensionics

Author: Fixed-4D-Topology Research Team
Date: 2026-02-09
"""

import numpy as np
import matplotlib.pyplot as plt
from typing import Callable, Tuple
import json
from datetime import datetime


def energy_density(d: float, R: float = 0.0, alpha: float = 1.0, beta: float = 1.0) -> float:
    """
    Energy density: e(d) = R + α(d-2)² + β(d-4)²
    
    Args:
        d: Dimension value
        R: Scalar curvature
        alpha, beta: Coupling constants
    
    Returns:
        Energy density
    """
    return R + alpha * (d - 2)**2 + beta * (d - 4)**2


def energy_density_first_derivative(d: float, alpha: float = 1.0, beta: float = 1.0) -> float:
    """First derivative: e'(d) = 2α(d-2) + 2β(d-4)"""
    return 2 * alpha * (d - 2) + 2 * beta * (d - 4)


def energy_density_second_derivative(alpha: float = 1.0, beta: float = 1.0) -> float:
    """Second derivative: e''(d) = 2(α + β)"""
    return 2 * (alpha + beta)


def entropy_density(d: float) -> float:
    """
    Entropy density: s(d) = -d ln(d)
    """
    if d <= 0:
        return 0
    return -d * np.log(d)


def entropy_density_first_derivative(d: float) -> float:
    """First derivative: s'(d) = -ln(d) - 1"""
    return -np.log(d) - 1


def entropy_density_second_derivative(d: float) -> float:
    """Second derivative: s''(d) = -1/d"""
    return -1 / d


def total_functional(
    d: float,
    R: float = 0.0,
    alpha: float = 1.0,
    beta: float = 1.0,
    T: float = 1.0
) -> float:
    """
    Total functional: F(d) = E(d) - T·S(d)
    """
    return energy_density(d, R, alpha, beta) - T * entropy_density(d)


def analyze_convexity(
    alpha: float = 1.0,
    beta: float = 1.0,
    T: float = 1.0,
    d_range: Tuple[float, float] = (2.0, 4.0)
) -> dict:
    """
    Analyze convexity properties of functionals.
    
    Returns:
        Dictionary with analysis results
    """
    results = {
        "parameters": {"alpha": alpha, "beta": beta, "T": T},
        "timestamp": datetime.now().isoformat(),
        "convexity": {}
    }
    
    print("=" * 60)
    print("Convexity Analysis of Energy Functional")
    print("=" * 60)
    print(f"\nParameters: α={alpha}, β={beta}, T={T}")
    
    # Energy convexity
    e_hessian = energy_density_second_derivative(alpha, beta)
    print(f"\n1. Energy Functional E(d):")
    print(f"   e''(d) = 2(α+β) = {e_hessian:.4f}")
    print(f"   Status: {'✓ Strictly convex' if e_hessian > 0 else '✗ Not convex'}")
    results["convexity"]["energy"] = {"hessian": e_hessian, "convex": e_hessian > 0}
    
    # Entropy concavity
    d_test = np.linspace(d_range[0], d_range[1], 100)
    s_hessian_min = min(entropy_density_second_derivative(d) for d in d_test)
    print(f"\n2. Entropy Functional S(d):")
    print(f"   s''(d) = -1/d ∈ [{s_hessian_min:.4f}, {entropy_density_second_derivative(d_range[0]):.4f}]")
    print(f"   Status: {'✓ Strictly concave' if s_hessian_min < 0 else '✗ Not concave'}")
    results["convexity"]["entropy"] = {"hessian_range": (s_hessian_min, -0.25), "concave": s_hessian_min < 0}
    
    # Total functional
    f_hessian_min = e_hessian + T * s_hessian_min
    print(f"\n3. Total Functional F(d) = E(d) - T·S(d):")
    print(f"   F''(d) = e''(d) - T·s''(d)")
    print(f"   Minimum Hessian: {f_hessian_min:.4f}")
    print(f"   Status: {'✓ Strictly convex' if f_hessian_min > 0 else '✗ Not convex'}")
    results["convexity"]["total"] = {"hessian_min": f_hessian_min, "convex": f_hessian_min > 0}
    
    return results


def plot_functionals(
    alpha: float = 1.0,
    beta: float = 1.0,
    T: float = 1.0,
    save_path: str = "convexity_plots.png"
):
    """Plot energy, entropy, and total functionals."""
    d = np.linspace(2.0, 4.0, 500)
    
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    
    # Plot 1: Energy
    ax1 = axes[0, 0]
    e_vals = [energy_density(di, 0, alpha, beta) for di in d]
    ax1.plot(d, e_vals, 'b-', linewidth=2)
    ax1.set_xlabel('d', fontsize=11)
    ax1.set_ylabel('E(d)', fontsize=11)
    ax1.set_title(f'Energy (α={alpha}, β={beta})', fontsize=12)
    ax1.grid(True, alpha=0.3)
    ax1.axvline(x=2, color='r', linestyle='--', alpha=0.3)
    ax1.axvline(x=4, color='g', linestyle='--', alpha=0.3)
    
    # Plot 2: Entropy
    ax2 = axes[0, 1]
    s_vals = [entropy_density(di) for di in d]
    ax2.plot(d, s_vals, 'r-', linewidth=2)
    ax2.set_xlabel('d', fontsize=11)
    ax2.set_ylabel('S(d)', fontsize=11)
    ax2.set_title('Entropy', fontsize=12)
    ax2.grid(True, alpha=0.3)
    ax2.axvline(x=2, color='r', linestyle='--', alpha=0.3)
    ax2.axvline(x=4, color='g', linestyle='--', alpha=0.3)
    
    # Plot 3: Total functional
    ax3 = axes[1, 0]
    f_vals = [total_functional(di, 0, alpha, beta, T) for di in d]
    ax3.plot(d, f_vals, 'g-', linewidth=2)
    ax3.set_xlabel('d', fontsize=11)
    ax3.set_ylabel('F(d) = E(d) - T·S(d)', fontsize=11)
    ax3.set_title(f'Total Functional (T={T})', fontsize=12)
    ax3.grid(True, alpha=0.3)
    ax3.axvline(x=2, color='r', linestyle='--', alpha=0.3)
    ax3.axvline(x=4, color='g', linestyle='--', alpha=0.3)
    
    # Find and mark minimum
    min_idx = np.argmin(f_vals)
    ax3.plot(d[min_idx], f_vals[min_idx], 'ko', markersize=10)
    ax3.annotate(f'Min: d={d[min_idx]:.3f}', 
                 xy=(d[min_idx], f_vals[min_idx]),
                 xytext=(d[min_idx]+0.3, f_vals[min_idx]+0.5),
                 fontsize=10)
    
    # Plot 4: Second derivatives (Hessian)
    ax4 = axes[1, 1]
    e_hess = [energy_density_second_derivative(alpha, beta) for _ in d]
    s_hess = [entropy_density_second_derivative(di) for di in d]
    f_hess = [e + T * s for e, s in zip(e_hess, s_hess)]
    
    ax4.plot(d, e_hess, 'b-', linewidth=2, label="E''(d)")
    ax4.plot(d, s_hess, 'r-', linewidth=2, label="S''(d)")
    ax4.plot(d, f_hess, 'g-', linewidth=2, label="F''(d)")
    ax4.axhline(y=0, color='k', linestyle='-', alpha=0.3)
    ax4.set_xlabel('d', fontsize=11)
    ax4.set_ylabel("Second derivative", fontsize=11)
    ax4.set_title('Hessian Analysis', fontsize=12)
    ax4.legend(fontsize=10)
    ax4.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=150, bbox_inches='tight')
    print(f"\nPlots saved to: {save_path}")
    plt.close()


def parameter_sweep(save_path: str = "parameter_sweep.json"):
    """Test convexity for various parameter combinations."""
    alphas = [0.5, 1.0, 2.0]
    betas = [0.5, 1.0, 2.0]
    Ts = [0.5, 1.0, 2.0]
    
    results = []
    
    print("\n" + "=" * 60)
    print("Parameter Sweep: Convexity Testing")
    print("=" * 60)
    
    for alpha in alphas:
        for beta in betas:
            for T in Ts:
                result = analyze_convexity(alpha, beta, T)
                results.append(result)
                print(f"\nα={alpha}, β={beta}, T={T}: F convex = {result['convexity']['total']['convex']}")
    
    with open(save_path, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\n\nSweep results saved to: {save_path}")


if __name__ == "__main__":
    print("=" * 60)
    print("P3-T1: Convexity Analysis of Energy Functional")
    print("=" * 60)
    
    # Main analysis
    results = analyze_convexity(alpha=1.0, beta=1.0, T=1.0)
    
    # Save results
    with open("convexity_results.json", 'w') as f:
        json.dump(results, f, indent=2)
    print("\nResults saved to: convexity_results.json")
    
    # Generate plots
    plot_functionals(alpha=1.0, beta=1.0, T=1.0)
    
    # Parameter sweep
    parameter_sweep()
    
    print("\n" + "=" * 60)
    print("Analysis Complete!")
    print("=" * 60)
