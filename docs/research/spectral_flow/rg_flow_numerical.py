#!/usr/bin/env python3
"""
Numerical RG Flow Analysis for Mode Constraint Systems

Task 2.1.3: RG Fixed Point Analysis
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint, solve_ivp
from scipy.optimize import fsolve


class RGFlowAnalyzer:
    """
    Analyzer for renormalization group flow of mode constraint systems.
    """
    
    def __init__(self, d_topo, w=0):
        """
        Initialize RG analyzer.
        
        Parameters:
        -----------
        d_topo : int
            Topological dimension
        w : int
            Quantum correction (0 or 1)
        """
        self.d_topo = d_topo
        self.w = w
        self.L = d_topo - 2 + w
        self.c1_star = 2**(-self.L)  # Theoretical fixed point
        
    def beta_function_c1(self, c1, form='polynomial', **params):
        """
        Beta function for c1 flow.
        
        Parameters:
        -----------
        c1 : float
            Constraint sharpness parameter
        form : str
            'polynomial', 'logarithmic', or 'constrained'
        params : dict
            Parameters for specific form
            
        Returns:
        --------
        beta : float
            Flow velocity
        """
        if c1 <= 0:
            return 0  # Boundary
            
        if form == 'polynomial':
            # beta = a1*c1 + a2*c1^2
            a1 = params.get('a1', -0.5)
            a2 = params.get('a2', 1.0)
            return a1 * c1 + a2 * c1**2
            
        elif form == 'logarithmic':
            # beta = -c1 * ln(c1/c0)
            c0 = params.get('c0', 1.0)
            return -c1 * np.log(c1 / c0)
            
        elif form == 'constrained':
            # beta = c1 * (1 - c1/c1_star)
            c1_target = params.get('c1_star', self.c1_star)
            gamma = params.get('gamma', 1.0)
            return gamma * c1 * (1 - c1 / c1_target)
            
        elif form == 'physical':
            # Physical ansatz based on entropy
            # beta ~ -c1 * ln(2^L * c1)
            return -c1 * np.log((2**self.L) * c1)
            
        else:
            raise ValueError(f"Unknown form: {form}")
    
    def beta_function_L(self, L, gamma=1.0, L_star=None):
        """
        Beta function for number of constraint levels L.
        
        This may be more physical than c1 flow.
        """
        if L_star is None:
            L_star = self.L
        return -gamma * (L - L_star)
    
    def solve_flow_c1(self, c1_0, t_range, form='constrained', **params):
        """
        Solve RG flow for c1.
        
        Parameters:
        -----------
        c1_0 : float
            Initial value
        t_range : array
            Flow parameter (log scale)
        form : str
            Beta function form
        params : dict
            Parameters for beta function
            
        Returns:
        --------
        c1_t : array
            Solution c1(t)
        """
        def dcdt(c1, t):
            return self.beta_function_c1(c1, form, **params)
        
        c1_t = odeint(dcdt, c1_0, t_range, rtol=1e-10, atol=1e-12)
        return c1_t.flatten()
    
    def solve_flow_L(self, L_0, t_range, gamma=1.0):
        """Solve RG flow for L."""
        def dLdt(L, t):
            return self.beta_function_L(L, gamma)
        
        L_t = odeint(dLdt, L_0, t_range)
        return L_t.flatten()
    
    def find_fixed_points(self, form='constrained', **params):
        """
        Find fixed points by solving beta(c*) = 0.
        
        Returns:
        --------
        fixed_points : list
            List of fixed point values
        stability : list
            Stability of each (+1 for unstable, -1 for stable)
        """
        # Search range
        c1_range = np.logspace(-5, 0, 1000)
        
        fixed_points = []
        stability = []
        
        for c1 in c1_range:
            try:
                c1_fp = fsolve(lambda x: self.beta_function_c1(x, form, **params), 
                              c1, full_output=False)[0]
                
                # Check if it's actually a solution
                if abs(self.beta_function_c1(c1_fp, form, **params)) < 1e-6:
                    # Check uniqueness
                    is_new = True
                    for fp in fixed_points:
                        if abs(c1_fp - fp) < 1e-4:
                            is_new = False
                            break
                    
                    if is_new and c1_fp > 0:
                        fixed_points.append(c1_fp)
                        
                        # Determine stability (derivative of beta)
                        dc = c1_fp * 1e-6
                        beta_prime = (self.beta_function_c1(c1_fp + dc, form, **params) - 
                                     self.beta_function_c1(c1_fp - dc, form, **params)) / (2*dc)
                        
                        stability.append(np.sign(beta_prime))
            except:
                continue
        
        return fixed_points, stability
    
    def critical_exponent(self, c1_fp, form='constrained', **params):
        """
        Calculate critical exponent at fixed point.
        
        theta = d(beta)/dc1 at c1 = c1_fp
        """
        dc = c1_fp * 1e-8
        beta_plus = self.beta_function_c1(c1_fp + dc, form, **params)
        beta_minus = self.beta_function_c1(c1_fp - dc, form, **params)
        
        theta = (beta_plus - beta_minus) / (2*dc)
        return theta
    
    def analyze_phase_space(self, c1_range, form='constrained', **params):
        """
        Analyze phase space (beta vs c1).
        """
        beta_vals = [self.beta_function_c1(c1, form, **params) for c1 in c1_range]
        
        # Find zeros
        zeros = []
        for i in range(len(beta_vals) - 1):
            if beta_vals[i] * beta_vals[i+1] < 0:  # Sign change
                zeros.append(c1_range[i])
        
        return np.array(beta_vals), zeros


def plot_rg_flow_comparison(analyzer, t_range, forms=['polynomial', 'logarithmic', 'constrained']):
    """Compare different beta function forms."""
    
    fig, axes = plt.subplots(2, len(forms), figsize=(15, 8))
    
    colors = ['blue', 'red', 'green', 'purple']
    
    for idx, form in enumerate(forms):
        ax1 = axes[0, idx]
        ax2 = axes[1, idx]
        
        # Plot 1: Phase space (beta vs c1)
        c1_range = np.logspace(-4, 0, 500)
        beta_vals, zeros = analyzer.analyze_phase_space(c1_range, form)
        
        ax1.semilogx(c1_range, beta_vals, color=colors[idx], linewidth=2)
        ax1.axhline(y=0, color='k', linestyle='--', alpha=0.5)
        
        # Mark fixed points
        for z in zeros:
            ax1.axvline(x=z, color='r', linestyle=':', alpha=0.7)
            ax1.plot(z, 0, 'ro', markersize=10)
        
        ax1.set_xlabel('$c_1$')
        ax1.set_ylabel(r'$\beta(c_1)$')
        ax1.set_title(f'Phase Space: {form}')
        ax1.grid(True, alpha=0.3)
        
        # Plot 2: Flow trajectories
        initial_conditions = [0.001, 0.01, 0.1, 0.5, 1.0]
        
        for c1_0 in initial_conditions:
            if c1_0 > 0:
                c1_t = analyzer.solve_flow_c1(c1_0, t_range, form)
                ax2.semilogy(t_range, c1_t, linewidth=2, alpha=0.7)
        
        # Mark theoretical fixed point
        ax2.axhline(y=analyzer.c1_star, color='r', linestyle='--', 
                   label=f'$c_1^* = {analyzer.c1_star:.4f}$')
        
        ax2.set_xlabel('RG time $t$')
        ax2.set_ylabel('$c_1(t)$')
        ax2.set_title(f'Flow Trajectories: {form}')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
    
    plt.suptitle(f'RG Flow Analysis: d={analyzer.d_topo}, w={analyzer.w}, L={analyzer.L}', 
                fontsize=14, fontweight='bold')
    plt.tight_layout()
    
    return fig


def analyze_all_forms(analyzer):
    """Comprehensive analysis of all beta function forms."""
    
    print("=" * 70)
    print(f"RG Fixed Point Analysis")
    print(f"System: d={analyzer.d_topo}, w={analyzer.w}, L={analyzer.L}")
    print(f"Theoretical c₁* = {analyzer.c1_star:.6f}")
    print("=" * 70)
    
    forms = ['polynomial', 'logarithmic', 'constrained', 'physical']
    
    for form in forms:
        print(f"\n{'='*70}")
        print(f"Form: {form}")
        print('='*70)
        
        # Find fixed points
        fp_list, stability = analyzer.find_fixed_points(form)
        
        print(f"\nFixed Points Found: {len(fp_list)}")
        for i, (fp, stab) in enumerate(zip(fp_list, stability)):
            theta = analyzer.critical_exponent(fp, form)
            stab_str = "Stable" if stab < 0 else "Unstable"
            print(f"  FP {i+1}: c₁ = {fp:.6f}")
            print(f"    Stability: {stab_str}")
            print(f"    Critical exponent θ = {theta:.4f}")
        
        # Compare with theoretical value
        if analyzer.c1_star in fp_list or any(abs(fp - analyzer.c1_star) < 1e-4 for fp in fp_list):
            print(f"\n  ✓ Theoretical c₁* = {analyzer.c1_star:.6f} IS a fixed point!")
        else:
            print(f"\n  ✗ Theoretical c₁* = {analyzer.c1_star:.6f} is NOT a fixed point for this form.")
    
    print("\n" + "=" * 70)


def main():
    """Main RG analysis."""
    
    print("=" * 70)
    print("RG Fixed Point Analysis - Task 2.1.3")
    print("=" * 70)
    
    # Analyze multiple systems
    systems = [
        {'d': 3, 'w': 0, 'name': 'Classical 3D'},
        {'d': 4, 'w': 0, 'name': 'Classical 4D'},
        {'d': 4, 'w': 1, 'name': 'Quantum 4D'},
    ]
    
    t_range = np.linspace(0, 10, 1000)
    
    for sys in systems:
        print(f"\n{'='*70}")
        print(f"System: {sys['name']}")
        print('='*70)
        
        analyzer = RGFlowAnalyzer(sys['d'], sys['w'])
        analyze_all_forms(analyzer)
        
        # Generate plots
        fig = plot_rg_flow_comparison(analyzer, t_range)
        filename = f"rg_flow_d{sys['d']}_w{sys['w']}.png"
        fig.savefig(filename, dpi=150, bbox_inches='tight')
        print(f"\nPlot saved: {filename}")
        plt.close(fig)
    
    print("\n" + "=" * 70)
    print("RG Analysis Complete!")
    print("=" * 70)


if __name__ == '__main__':
    main()
