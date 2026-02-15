#!/usr/bin/env python3
"""
n_dof Calculation for Fractal Constraint Hierarchy

This script calculates the effective degrees of freedom for a system
with fractal constraint structure.

Task: 2.1.1 - Subtask 2: Calculate n_dof for fractal hierarchy
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.special import gamma, zeta


class FractalConstraintModel:
    """
    Model for constraint-determined effective degrees of freedom
    with fractal hierarchical structure.
    """
    
    def __init__(self, d_topo, w=0):
        """
        Initialize model.
        
        Parameters:
        -----------
        d_topo : int
            Topological dimension
        w : int
            Quantum correction (0 for classical, 1 for quantum)
        """
        self.d_topo = d_topo
        self.w = w
        self.N_levels = d_topo - 2 + w  # Number of constraint levels
        self.c1 = 2**(-self.N_levels)  # Theoretical c1
        
    def constraint_probability(self, E_c, E_ref, level):
        """
        Probability that a mode at given level is accessible.
        
        P_acc = 1 / (1 + (E_c/E_ref)^(c1 * 2^level))
        
        The factor 2^level accounts for hierarchical constraint strength.
        """
        effective_c = self.c1 * (2**level)
        x = E_c / E_ref
        return 1.0 / (1.0 + x**effective_c)
    
    def calculate_ndof(self, E_c, E_ref, d_low=2):
        """
        Calculate effective degrees of freedom.
        
        n_dof = d_low + (d_topo - d_low) / (1 + (E_c/E_ref)^c1)
        
        This is the standard dimension flow formula.
        """
        x = E_c / E_ref
        return d_low + (self.d_topo - d_low) / (1.0 + x**self.c1)
    
    def calculate_ndof_hierarchical(self, E_c, E_ref, d_low=2):
        """
        Calculate n_dof using explicit hierarchical model.
        
        Sum over all constraint levels with level-dependent accessibility.
        """
        n_accessible = 0
        
        # Level 0: Always accessible (2 dimensions - time + 1 space)
        n_accessible += d_low
        
        # Higher levels: Each contributes based on constraint probability
        for level in range(1, self.N_levels + 1):
            p_acc = self.constraint_probability(E_c, E_ref, level)
            n_accessible += p_acc
            
        return n_accessible
    
    def fractal_dimension(self, E_c, E_ref):
        """
        Calculate effective fractal dimension at given constraint energy.
        
        D_f = -d log(n_dof) / d log(E_c)
        """
        # Numerical derivative
        dE = E_c * 0.01
        n1 = self.calculate_ndof(E_c - dE, E_ref)
        n2 = self.calculate_ndof(E_c + dE, E_ref)
        
        return -np.log(n2/n1) / np.log((E_c + dE)/(E_c - dE))


def analyze_system(d_topo, w, E_c_range, E_ref=1.0):
    """
    Analyze a system with given topological dimension.
    
    Parameters:
    -----------
    d_topo : int
        Topological dimension
    w : int
        Quantum correction
    E_c_range : array
        Range of constraint energies to analyze
    E_ref : float
        Reference energy scale
        
    Returns:
    --------
    results : dict
        Analysis results
    """
    model = FractalConstraintModel(d_topo, w)
    
    # Calculate n_dof for each E_c
    n_dof_standard = [model.calculate_ndof(E_c, E_ref) for E_c in E_c_range]
    n_dof_hierarchical = [model.calculate_ndof_hierarchical(E_c, E_ref) for E_c in E_c_range]
    
    # Calculate fractal dimension
    D_f = [model.fractal_dimension(E_c, E_ref) for E_c in E_c_range[1:-1]]
    
    return {
        'model': model,
        'E_c': E_c_range,
        'n_dof_standard': n_dof_standard,
        'n_dof_hierarchical': n_dof_hierarchical,
        'D_f': D_f,
        'c1': model.c1,
        'N_levels': model.N_levels
    }


def plot_results(results, title_suffix=""):
    """Plot analysis results."""
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    
    model = results['model']
    E_c = results['E_c']
    
    # Plot 1: n_dof vs E_c
    ax = axes[0, 0]
    ax.semilogx(E_c, results['n_dof_standard'], 'b-', label='Standard formula', linewidth=2)
    ax.semilogx(E_c, results['n_dof_hierarchical'], 'r--', label='Hierarchical model', linewidth=2)
    ax.set_xlabel('Constraint Energy $E_c$ / $E_{ref}$')
    ax.set_ylabel('Effective Degrees of Freedom $n_{dof}$')
    ax.set_title(f'$n_{{dof}}$ vs $E_c$ (d={model.d_topo}, w={model.w})')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # Plot 2: Transition function
    ax = axes[0, 1]
    x = E_c / E_c[len(E_c)//2]  # Normalized
    f = 1 / (1 + x**model.c1)
    ax.semilogx(x, f, 'g-', linewidth=2)
    ax.axhline(y=0.5, color='r', linestyle='--', alpha=0.5, label='Half-point')
    ax.set_xlabel('$E_c / E_{ref}$ (normalized)')
    ax.set_ylabel('Transition Function $f(E_c)$')
    ax.set_title(f'Transition Function ($c_1 = {model.c1:.4f}$)')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # Plot 3: Fractal dimension
    ax = axes[1, 0]
    D_f = results['D_f']
    E_c_mid = E_c[1:-1]
    ax.semilogx(E_c_mid, D_f, 'm-', linewidth=2)
    ax.set_xlabel('Constraint Energy $E_c$ / $E_{ref}$')
    ax.set_ylabel('Effective Fractal Dimension $D_f$')
    ax.set_title('Fractal Dimension vs Constraint Energy')
    ax.grid(True, alpha=0.3)
    
    # Plot 4: Constraint hierarchy visualization
    ax = axes[1, 1]
    levels = range(model.N_levels + 1)
    probs = [model.constraint_probability(1.0, 1.0, level) for level in levels]
    ax.bar(levels, probs, color='steelblue', alpha=0.7)
    ax.set_xlabel('Constraint Level')
    ax.set_ylabel('Accessibility Probability')
    ax.set_title(f'Constraint Hierarchy (N={model.N_levels} levels)')
    ax.grid(True, alpha=0.3, axis='y')
    
    plt.suptitle(f'Fractal Constraint Model Analysis {title_suffix}', fontsize=14, fontweight='bold')
    plt.tight_layout()
    return fig


def main():
    """Main analysis routine."""
    print("=" * 60)
    print("Fractal Constraint Model - n_dof Calculation")
    print("=" * 60)
    
    # System parameters
    systems = [
        {'d': 3, 'w': 0, 'name': 'Classical 3D (Rotating Fluid)'},
        {'d': 4, 'w': 0, 'name': 'Classical 4D (Black Hole)'},
        {'d': 4, 'w': 1, 'name': 'Quantum 4D (Quantum Gravity)'},
    ]
    
    # Energy range
    E_c_range = np.logspace(-3, 3, 1000)
    E_ref = 1.0
    
    results_all = []
    
    for sys in systems:
        print(f"\n{sys['name']}:")
        print(f"  d_topo = {sys['d']}, w = {sys['w']}")
        
        results = analyze_system(sys['d'], sys['w'], E_c_range, E_ref)
        results_all.append(results)
        
        print(f"  N_levels = {results['N_levels']}")
        print(f"  c_1 = {results['c1']:.6f}")
        print(f"  c_1 (exact) = 1/2^{results['N_levels']} = {1/2**results['N_levels']:.6f}")
        print(f"  n_dof at E_c = E_ref: {results['n_dof_standard'][len(E_c_range)//2]:.3f}")
        
        # Save plot
        fig = plot_results(results, f"- {sys['name']}")
        filename = f"fractal_model_d{sys['d']}_w{sys['w']}.png"
        fig.savefig(filename, dpi=150, bbox_inches='tight')
        print(f"  Plot saved: {filename}")
        plt.close(fig)
    
    print("\n" + "=" * 60)
    print("Analysis complete!")
    print("=" * 60)
    
    return results_all


if __name__ == '__main__':
    results = main()
