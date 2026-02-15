#!/usr/bin/env python3
"""
Multifractal Spectrum Analysis for Mode Constraint Systems

This script computes the multifractal spectrum f(α) from the n_dof(E_c) curve.

Task: 2.1.2 - Multifractal Spectrum Analysis
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.interpolate import interp1d


class MultifractalAnalyzer:
    """
    Analyzer for multifractal properties of constraint-determined mode systems.
    """
    
    def __init__(self, d_topo, w=0, d_low=2):
        """
        Initialize analyzer.
        
        Parameters:
        -----------
        d_topo : int
            Topological dimension
        w : int
            Quantum correction (0 or 1)
        d_low : int
            Minimal accessible dimensions
        """
        self.d_topo = d_topo
        self.w = w
        self.d_low = d_low
        self.L = d_topo - 2 + w  # Number of constraint levels
        self.c1 = 2**(-self.L)
        
    def ndof_curve(self, E_c, E_ref=1.0):
        """
        Calculate n_dof as function of constraint energy.
        
        Uses the standard transition formula:
        n_dof(E_c) = d_low + (d_topo - d_low) / (1 + (E_c/E_ref)^c1)
        """
        x = E_c / E_ref
        return self.d_low + (self.d_topo - self.d_low) / (1.0 + x**self.c1)
    
    def local_dimension(self, E_c, E_ref=1.0):
        """
        Calculate local (pointwise) dimension at given E_c.
        
        α(E_c) = -d ln(n_dof) / d ln(E_c)
        """
        # Numerical derivative
        dE = E_c * 0.001
        
        n1 = self.ndof_curve(E_c - dE, E_ref)
        n2 = self.ndof_curve(E_c + dE, E_ref)
        
        # Handle edge cases
        if n1 <= 0 or n2 <= 0:
            return np.nan
            
        alpha = -np.log(n2/n1) / np.log((E_c + dE)/(E_c - dE))
        return alpha
    
    def partition_function(self, q, E_c_range, E_ref=1.0):
        """
        Calculate partition function Z(q) for multifractal analysis.
        
        Z(q) = ∫ dE_c [n_dof(E_c)]^q
        
        This is related to the moment of the measure.
        """
        ndof = np.array([self.ndof_curve(E_c, E_ref) for E_c in E_c_range])
        
        # Normalize to create probability measure
        measure = ndof / np.trapz(ndof, E_c_range)
        
        # Calculate moment
        Z_q = np.trapz(measure**q, E_c_range)
        
        return Z_q
    
    def tau_q(self, q_values, E_c_range, E_ref=1.0):
        """
        Calculate mass exponent τ(q).
        
        τ(q) = lim_{ε→0} ln(Z(q)) / ln(ε)
        
        where ε is the "box size" in energy space.
        """
        tau = []
        
        for q in q_values:
            Z_q = self.partition_function(q, E_c_range, E_ref)
            if Z_q > 0:
                # Effective scaling exponent
                tau_q_val = np.log(Z_q) / np.log(len(E_c_range))
                tau.append(tau_q_val)
            else:
                tau.append(np.nan)
                
        return np.array(tau)
    
    def singularity_spectrum(self, alpha_range, E_c_range, E_ref=1.0):
        """
        Calculate singularity spectrum f(α).
        
        f(α) = q·α - τ(q)
        
        where α = dτ/dq
        """
        # Calculate τ(q) for range of q
        q_values = np.linspace(-10, 10, 200)
        tau = self.tau_q(q_values, E_c_range, E_ref)
        
        # Remove NaN values
        valid_idx = ~np.isnan(tau)
        q_valid = q_values[valid_idx]
        tau_valid = tau[valid_idx]
        
        if len(q_valid) < 2:
            return None, None
        
        # Calculate α = dτ/dq
        alpha = np.gradient(tau_valid, q_valid)
        
        # Calculate f(α) = q·α - τ(q)
        f_alpha = q_valid * alpha - tau_valid
        
        return alpha, f_alpha
    
    def box_counting_dimension(self, E_c_range, n_boxes_list, E_ref=1.0):
        """
        Calculate dimension using box-counting method.
        
        N(ε) ∝ ε^(-D)
        where ε is box size.
        """
        ndof = np.array([self.ndof_curve(E_c, E_ref) for E_c in E_c_range])
        
        dimensions = []
        
        for n_boxes in n_boxes_list:
            # Divide energy range into boxes
            box_size = len(E_c_range) / n_boxes
            
            # Count non-empty boxes
            occupied = 0
            for i in range(n_boxes):
                start_idx = int(i * box_size)
                end_idx = int((i + 1) * box_size)
                if end_idx > len(ndof):
                    end_idx = len(ndof)
                
                if np.any(ndof[start_idx:end_idx] > 0):
                    occupied += 1
            
            dimensions.append((n_boxes, occupied))
            
        return dimensions
    
    def analyze(self, E_c_range, E_ref=1.0, save_plots=True):
        """
        Perform complete multifractal analysis.
        """
        results = {
            'd_topo': self.d_topo,
            'w': self.w,
            'c1': self.c1,
            'L': self.L,
            'E_c': E_c_range,
            'E_ref': E_ref
        }
        
        # 1. n_dof curve
        results['n_dof'] = np.array([self.ndof_curve(E_c, E_ref) for E_c in E_c_range])
        
        # 2. Local dimension α(E_c)
        results['alpha_local'] = np.array([self.local_dimension(E_c, E_ref) 
                                           for E_c in E_c_range[10:-10]])
        results['E_c_alpha'] = E_c_range[10:-10]
        
        # 3. Singularity spectrum f(α)
        alpha_range = np.linspace(0.5, 3.0, 100)
        alpha, f_alpha = self.singularity_spectrum(alpha_range, E_c_range, E_ref)
        results['alpha_spectrum'] = alpha
        results['f_alpha'] = f_alpha
        
        # 4. Box counting
        n_boxes_list = [10, 20, 40, 80, 160, 320]
        box_results = self.box_counting_dimension(E_c_range, n_boxes_list, E_ref)
        results['box_counting'] = box_results
        
        return results


def plot_multifractal_results(results, save_prefix="multifractal"):
    """Plot multifractal analysis results."""
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    
    d = results['d_topo']
    w = results['w']
    c1 = results['c1']
    
    # 1. n_dof vs E_c
    ax = axes[0, 0]
    ax.semilogx(results['E_c'], results['n_dof'], 'b-', linewidth=2)
    ax.set_xlabel('Constraint Energy $E_c / E_{ref}$')
    ax.set_ylabel('$n_{dof}$')
    ax.set_title(f'$n_{{dof}}$ vs $E_c$ (d={d}, w={w})')
    ax.grid(True, alpha=0.3)
    
    # 2. Local dimension α(E_c)
    ax = axes[0, 1]
    alpha_local = results['alpha_local']
    E_c_alpha = results['E_c_alpha']
    valid_idx = ~np.isnan(alpha_local)
    ax.semilogx(E_c_alpha[valid_idx], alpha_local[valid_idx], 'r-', linewidth=2)
    ax.set_xlabel('$E_c / E_{ref}$')
    ax.set_ylabel('Local Dimension $\\alpha$')
    ax.set_title(f'Local Dimension (c₁={c1:.4f})')
    ax.grid(True, alpha=0.3)
    
    # 3. Singularity spectrum f(α)
    ax = axes[0, 2]
    alpha = results['alpha_spectrum']
    f_alpha = results['f_alpha']
    if alpha is not None and f_alpha is not None:
        valid = (~np.isnan(alpha)) & (~np.isnan(f_alpha))
        ax.plot(alpha[valid], f_alpha[valid], 'g-', linewidth=2)
        ax.set_xlabel('Singularity Strength $\\alpha$')
        ax.set_ylabel('$f(\\alpha)$')
        ax.set_title('Singularity Spectrum')
        ax.grid(True, alpha=0.3)
    
    # 4. Phase space visualization
    ax = axes[1, 0]
    # Show how n_dof fills the available space
    ndof_norm = results['n_dof'] / results['d_topo']
    ax.fill_between(results['E_c'], 0, ndof_norm, alpha=0.5)
    ax.set_xscale('log')
    ax.set_xlabel('$E_c / E_{ref}$')
    ax.set_ylabel('Normalized $n_{dof}$')
    ax.set_title('Phase Space Occupation')
    ax.grid(True, alpha=0.3)
    
    # 5. Box counting
    ax = axes[1, 1]
    box_results = results['box_counting']
    if box_results:
        n_boxes = [r[0] for r in box_results]
        occupied = [r[1] for r in box_results]
        ax.loglog(1/np.array(n_boxes), occupied, 'mo-', markersize=8)
        
        # Fit power law
        log_eps = np.log(1/np.array(n_boxes))
        log_N = np.log(occupied)
        coeffs = np.polyfit(log_eps, log_N, 1)
        D_box = coeffs[0]
        
        ax.set_xlabel('Box Size $\\epsilon$')
        ax.set_ylabel('Occupied Boxes N($\\epsilon$)')
        ax.set_title(f'Box Counting (D={D_box:.3f})')
        ax.grid(True, alpha=0.3)
        
        results['D_box'] = D_box
    
    # 6. Summary statistics
    ax = axes[1, 2]
    ax.axis('off')
    
    summary_text = f"""
    Multifractal Analysis Summary
    =============================
    
    System Parameters:
    - Topological dimension: {d}
    - Quantum correction: {w}
    - Constraint levels: {results['L']}
    - c₁ value: {c1:.6f}
    
    Key Results:
    - n_dof range: [{np.min(results['n_dof']):.3f}, {np.max(results['n_dof']):.3f}]
    - α range: [{np.nanmin(alpha_local):.3f}, {np.nanmax(alpha_local):.3f}]
    
    Interpretation:
    The system exhibits multifractal structure
    with c₁ controlling the transition sharpness.
    """
    
    ax.text(0.1, 0.5, summary_text, fontsize=10, family='monospace',
            verticalalignment='center')
    
    plt.suptitle(f'Multifractal Analysis: d={d}, w={w}, c₁={c1:.4f}', 
                 fontsize=14, fontweight='bold')
    plt.tight_layout()
    
    if save_prefix:
        filename = f"{save_prefix}_d{d}_w{w}.png"
        fig.savefig(filename, dpi=150, bbox_inches='tight')
        print(f"Saved: {filename}")
    
    return fig


def main():
    """Main analysis routine."""
    print("=" * 60)
    print("Multifractal Spectrum Analysis")
    print("=" * 60)
    
    # Systems to analyze
    systems = [
        {'d': 3, 'w': 0, 'name': 'Classical 3D'},
        {'d': 4, 'w': 0, 'name': 'Classical 4D'},
        {'d': 4, 'w': 1, 'name': 'Quantum 4D'},
    ]
    
    # Energy range
    E_c_range = np.logspace(-3, 3, 1000)
    E_ref = 1.0
    
    all_results = []
    
    for sys in systems:
        print(f"\n{sys['name']}:")
        print(f"  d={sys['d']}, w={sys['w']}")
        
        analyzer = MultifractalAnalyzer(sys['d'], sys['w'])
        results = analyzer.analyze(E_c_range, E_ref)
        all_results.append(results)
        
        print(f"  c₁ = {results['c1']:.6f}")
        print(f"  n_dof range: [{np.min(results['n_dof']):.3f}, {np.max(results['n_dof']):.3f}]")
        
        if 'D_box' in results:
            print(f"  Box-counting dim: {results['D_box']:.3f}")
        
        # Generate plots
        fig = plot_multifractal_results(results, "multifractal")
        plt.close(fig)
    
    print("\n" + "=" * 60)
    print("Analysis complete!")
    print("=" * 60)
    
    return all_results


if __name__ == '__main__':
    results = main()
