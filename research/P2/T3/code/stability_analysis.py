#!/usr/bin/env python3
"""
P2-T3: Stability Analysis of Master Equation
Lyapunov Theory and Numerical Verification

Author: Fixed-4D-Topology Research Team
Date: 2026-02-09
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
from typing import Callable, Tuple
import json
from datetime import datetime


def beta_standard(d: float, alpha: float = 1.0) -> float:
    """
    Standard model beta function.
    
    Args:
        d: Spectral dimension
        alpha: Coupling constant
    
    Returns:
        Beta function value
    """
    return -alpha * (d - 2) * (4 - d)


def beta_derivative(d: float, alpha: float = 1.0) -> float:
    """Derivative of beta function."""
    return -alpha * ((4 - d) - (d - 2))


def master_equation(y: float, ln_mu: float, alpha: float = 1.0) -> float:
    """
    Master equation: d(d_s)/d(ln mu) = beta(d_s)
    
    Args:
        y: Current value of d_s
        ln_mu: Logarithm of energy scale
        alpha: Coupling constant
    
    Returns:
        Derivative dd_s/d(ln mu)
    """
    return beta_standard(y, alpha)


def lyapunov_function(d: float) -> float:
    """
    Lyapunov function V(d) = 0.5 * (d-2)^2 * (4-d)^2
    """
    return 0.5 * (d - 2)**2 * (4 - d)**2


def solve_master_eq(
    d0: float,
    ln_mu_range: Tuple[float, float],
    alpha: float = 1.0,
    n_points: int = 1000
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Solve Master equation numerically.
    
    Args:
        d0: Initial spectral dimension
        ln_mu_range: (ln_mu_min, ln_mu_max)
        alpha: Coupling constant
        n_points: Number of integration points
    
    Returns:
        (ln_mu_values, d_s_values)
    """
    ln_mu = np.linspace(ln_mu_range[0], ln_mu_range[1], n_points)
    
    def ode(y, t):
        return master_equation(y, t, alpha)
    
    d_solution = odeint(ode, d0, ln_mu)
    return ln_mu, d_solution.flatten()


def analyze_stability(
    d0_values: np.ndarray,
    alpha: float = 1.0,
    ln_mu_max: float = 10.0
) -> dict:
    """
    Analyze stability for various initial conditions.
    
    Returns:
        Dictionary with analysis results
    """
    results = {
        "alpha": alpha,
        "timestamp": datetime.now().isoformat(),
        "runs": []
    }
    
    print("=" * 60)
    print("Master Equation Stability Analysis")
    print("=" * 60)
    print(f"\nParameters: α = {alpha}")
    print(f"Fixed points: d_UV = 2, d_IR = 4")
    print(f"β'(2) = {beta_derivative(2, alpha):.4f} (UV stability)")
    print(f"β'(4) = {beta_derivative(4, alpha):.4f} (IR stability)")
    print("=" * 60)
    
    for d0 in d0_values:
        ln_mu, d_sol = solve_master_eq(d0, (0, ln_mu_max), alpha)
        
        d_final = d_sol[-1]
        convergence = abs(d_final - 4) if d0 > 3 else abs(d_final - 2)
        
        # Fit exponential decay
        if d0 < 3:
            # UV convergence
            decay_rate = -2 * alpha
            theory_decay = np.exp(decay_rate * ln_mu)
            actual_residual = np.abs(d_sol - 2)
        else:
            # IR convergence
            decay_rate = 2 * alpha
            theory_decay = 4 - np.exp(-decay_rate * ln_mu) * (4 - d0)
            actual_residual = np.abs(d_sol - 4)
        
        run_result = {
            "d0": float(d0),
            "d_final": float(d_final),
            "convergence": float(convergence),
            "converged_to": "UV" if d_final < 3 else "IR"
        }
        results["runs"].append(run_result)
        
        print(f"\nd_0 = {d0:.4f}:")
        print(f"  Final d_s = {d_final:.6f}")
        print(f"  Converged to: {run_result['converged_to']}")
        print(f"  Convergence error: {convergence:.2e}")
    
    return results


def plot_phase_portrait(alpha: float = 1.0, save_path: str = "phase_portrait.png"):
    """Generate phase portrait of Master equation."""
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    # Plot 1: Trajectories
    ax1 = axes[0]
    d0_values = np.linspace(2.1, 3.9, 10)
    
    for d0 in d0_values:
        ln_mu, d_sol = solve_master_eq(d0, (0, 5), alpha)
        mu = np.exp(ln_mu)
        ax1.plot(mu, d_sol, 'b-', alpha=0.6, linewidth=1.5)
    
    ax1.axhline(y=2, color='r', linestyle='--', label='UV fixed point (d=2)')
    ax1.axhline(y=4, color='g', linestyle='--', label='IR fixed point (d=4)')
    ax1.set_xlabel('$\mu$ (energy scale)', fontsize=12)
    ax1.set_ylabel('$d_s(\mu)$', fontsize=12)
    ax1.set_title('Spectral Dimension Flow', fontsize=14)
    ax1.legend()
    ax1.set_xscale('log')
    ax1.grid(True, alpha=0.3)
    ax1.set_ylim([1.5, 4.5])
    
    # Plot 2: Lyapunov function
    ax2 = axes[1]
    d_range = np.linspace(2, 4, 100)
    V_values = [lyapunov_function(d) for d in d_range]
    
    ax2.plot(d_range, V_values, 'b-', linewidth=2)
    ax2.axvline(x=2, color='r', linestyle='--', alpha=0.5)
    ax2.axvline(x=4, color='g', linestyle='--', alpha=0.5)
    ax2.set_xlabel('$d_s$', fontsize=12)
    ax2.set_ylabel('$V(d_s)$', fontsize=12)
    ax2.set_title('Lyapunov Function', fontsize=14)
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=150, bbox_inches='tight')
    print(f"\nPhase portrait saved to: {save_path}")
    plt.close()


def verify_exponential_convergence(
    d0: float,
    target: float,
    alpha: float = 1.0,
    save_path: str = "convergence.png"
):
    """Verify exponential convergence to fixed point."""
    ln_mu, d_sol = solve_master_eq(d0, (0, 5), alpha)
    
    residual = np.abs(d_sol - target)
    
    # Theoretical decay
    if target == 2:
        rate = 2 * alpha
        theory_residual = np.abs(d0 - target) * np.exp(-rate * ln_mu)
    else:
        rate = -2 * alpha
        theory_residual = np.abs(d0 - target) * np.exp(rate * ln_mu)
    
    plt.figure(figsize=(10, 6))
    plt.semilogy(ln_mu, residual, 'b-', linewidth=2, label='Numerical')
    plt.semilogy(ln_mu, theory_residual, 'r--', linewidth=2, label='Theoretical')
    plt.xlabel('$\ln \mu$', fontsize=12)
    plt.ylabel('$|d_s - d^*|$', fontsize=12)
    plt.title(f'Exponential Convergence to d={target}', fontsize=14)
    plt.legend(fontsize=11)
    plt.grid(True, alpha=0.3)
    plt.savefig(save_path, dpi=150, bbox_inches='tight')
    print(f"Convergence plot saved to: {save_path}")
    plt.close()


if __name__ == "__main__":
    print("=" * 60)
    print("P2-T3: Master Equation Stability Analysis")
    print("=" * 60)
    
    # Run stability analysis
    d0_values = np.array([2.1, 2.5, 2.9, 3.1, 3.5, 3.9])
    results = analyze_stability(d0_values, alpha=1.0)
    
    # Save results
    with open("stability_results.json", 'w') as f:
        json.dump(results, f, indent=2)
    print("\nResults saved to: stability_results.json")
    
    # Generate plots
    plot_phase_portrait(alpha=1.0)
    
    # Verify exponential convergence
    verify_exponential_convergence(2.5, 2, alpha=1.0, save_path="uv_convergence.png")
    verify_exponential_convergence(3.5, 4, alpha=1.0, save_path="ir_convergence.png")
    
    print("\n" + "=" * 60)
    print("Analysis Complete!")
    print("=" * 60)
