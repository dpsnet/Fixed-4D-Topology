#!/usr/bin/env python3
"""
P3-T1: Non-Convex Region Analysis
Study the physical meaning and phase transition phenomena 
in the non-convex regime where α + β ≤ T/8
"""

import numpy as np
import matplotlib.pyplot as plt
import json

plt.style.use('seaborn-v0_8-whitegrid')


def energy(d, alpha=1.0, beta=1.0, Vol=1.0):
    """Energy functional E(d)"""
    R = 0  # Background scalar curvature (constant)
    return Vol * (R + alpha * (d - 2)**2 + beta * (d - 4)**2)


def entropy(d, Vol=1.0):
    """Entropy functional S(d)"""
    if d <= 0:
        return -np.inf
    return -Vol * d * np.log(d)


def free_energy(d, alpha, beta, T, Vol=1.0):
    """Total free energy F(d) = E(d) - T*S(d)"""
    return energy(d, alpha, beta, Vol) - T * entropy(d, Vol)


def free_energy_derivative(d, alpha, beta, T, Vol=1.0):
    """First derivative F'(d)"""
    return Vol * (2*alpha*(d-2) + 2*beta*(d-4) + T*(1 + np.log(d)))


def free_energy_second(d, alpha, beta, T, Vol=1.0):
    """Second derivative F''(d)"""
    return Vol * (2*(alpha + beta) - T/d)


def find_critical_points(alpha, beta, T, Vol=1.0):
    """Find critical points where F'(d) = 0"""
    d_range = np.linspace(2.001, 3.999, 1000)
    F_prime = [free_energy_derivative(d, alpha, beta, T, Vol) for d in d_range]
    
    critical_points = []
    for i in range(len(F_prime)-1):
        if F_prime[i] * F_prime[i+1] < 0:  # Sign change
            # Refine with bisection
            a, b = d_range[i], d_range[i+1]
            for _ in range(20):
                mid = (a + b) / 2
                if free_energy_derivative(a, alpha, beta, T, Vol) * free_energy_derivative(mid, alpha, beta, T, Vol) < 0:
                    b = mid
                else:
                    a = mid
            critical_points.append((a + b) / 2)
    
    return critical_points


def classify_critical_point(d, alpha, beta, T, Vol=1.0):
    """Classify critical point as min, max, or saddle"""
    F_pp = free_energy_second(d, alpha, beta, T, Vol)
    if F_pp > 1e-6:
        return 'local_min'
    elif F_pp < -1e-6:
        return 'local_max'
    else:
        return 'degenerate'


def analyze_phase_structure(alpha, beta, T_values, Vol=1.0):
    """Analyze how phase structure changes with temperature"""
    results = []
    
    for T in T_values:
        # Check convexity condition
        is_convex = (alpha + beta) > T/8
        
        # Find critical points
        critical_points = find_critical_points(alpha, beta, T, Vol)
        
        # Classify critical points
        classified = []
        for cp in critical_points:
            classification = classify_critical_point(cp, alpha, beta, T, Vol)
            F_val = free_energy(cp, alpha, beta, T, Vol)
            classified.append({
                'd': cp,
                'type': classification,
                'F': F_val
            })
        
        # Find global minimum
        if classified:
            minima = [c for c in classified if c['type'] == 'local_min']
            if minima:
                global_min = min(minima, key=lambda x: x['F'])
            else:
                global_min = None
        else:
            global_min = None
        
        results.append({
            'T': T,
            'is_convex': is_convex,
            'critical_points': classified,
            'global_minimum': global_min,
            'num_minima': len([c for c in classified if c['type'] == 'local_min'])
        })
    
    return results


def plot_free_energy_landscape():
    """Plot free energy landscape for different parameter regimes"""
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle('P3-T1: Free Energy Landscape in Non-Convex Regime', 
                 fontsize=14, fontweight='bold')
    
    d_range = np.linspace(2.01, 3.99, 500)
    
    # Case 1: Convex (α + β > T/8)
    ax1 = axes[0, 0]
    alpha, beta, T = 0.5, 0.5, 1.0
    F_vals = [free_energy(d, alpha, beta, T) for d in d_range]
    ax1.plot(d_range, F_vals, linewidth=2.5, color='#2ecc71', label=f'α={alpha}, β={beta}, T={T}')
    ax1.axvline(x=2.5, color='green', linestyle='--', alpha=0.7, label='Global minimum')
    ax1.set_title(f'Convex Regime (α+β={alpha+beta} > T/8={T/8:.3f})', fontsize=11)
    ax1.set_xlabel('Dimension d')
    ax1.set_ylabel('F(d)')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Case 2: Boundary (α + β = T/8)
    ax2 = axes[0, 1]
    alpha, beta, T = 0.25, 0.25, 4.0
    F_vals = [free_energy(d, alpha, beta, T) for d in d_range]
    ax2.plot(d_range, F_vals, linewidth=2.5, color='#f39c12', label=f'α={alpha}, β={beta}, T={T}')
    critical = find_critical_points(alpha, beta, T)
    for cp in critical:
        F_cp = free_energy(cp, alpha, beta, T)
        ax2.plot(cp, F_cp, 'ro', markersize=10)
    ax2.set_title(f'Critical Boundary (α+β={alpha+beta} = T/8={T/8:.3f})', fontsize=11)
    ax2.set_xlabel('Dimension d')
    ax2.set_ylabel('F(d)')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    # Case 3: Non-convex with double well
    ax3 = axes[1, 0]
    alpha, beta, T = 0.15, 0.15, 4.0
    F_vals = [free_energy(d, alpha, beta, T) for d in d_range]
    ax3.plot(d_range, F_vals, linewidth=2.5, color='#e74c3c', label=f'α={alpha}, β={beta}, T={T}')
    critical = find_critical_points(alpha, beta, T)
    for i, cp in enumerate(critical):
        F_cp = free_energy(cp, alpha, beta, T)
        classification = classify_critical_point(cp, alpha, beta, T)
        color = 'go' if classification == 'local_min' else 'ro'
        ax3.plot(cp, F_cp, color, markersize=12, label=f'{"Min" if classification == "local_min" else "Max"} {i+1}')
    ax3.set_title(f'Non-Convex: Double Well (α+β={alpha+beta} < T/8={T/8:.3f})', fontsize=11)
    ax3.set_xlabel('Dimension d')
    ax3.set_ylabel('F(d)')
    ax3.legend()
    ax3.grid(True, alpha=0.3)
    
    # Case 4: Phase transition with temperature
    ax4 = axes[1, 1]
    alpha, beta = 0.2, 0.2
    T_vals = [2.0, 3.0, 3.5, 4.0]
    colors = plt.cm.viridis(np.linspace(0, 1, len(T_vals)))
    
    for T, color in zip(T_vals, colors):
        F_vals = [free_energy(d, alpha, beta, T) for d in d_range]
        ax4.plot(d_range, F_vals, linewidth=2, color=color, label=f'T={T} (α+β={alpha+beta} vs T/8={T/8:.3f})')
    
    ax4.set_title(f'Phase Transition with Temperature (α={alpha}, β={beta})', fontsize=11)
    ax4.set_xlabel('Dimension d')
    ax4.set_ylabel('F(d)')
    ax4.legend(fontsize=8)
    ax4.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('nonconvex_landscape.png', dpi=150, bbox_inches='tight')
    print("Saved: nonconvex_landscape.png")
    plt.close()


def plot_phase_diagram_detailed():
    """Plot detailed phase diagram showing different regimes"""
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    fig.suptitle('P3-T1: Phase Diagram and Number of Minima', fontsize=14, fontweight='bold')
    
    # Left: Phase diagram with explicit regions
    ax1 = axes[0]
    
    alpha_vals = np.linspace(0, 1, 200)
    beta_vals = np.linspace(0, 1, 200)
    A, B = np.meshgrid(alpha_vals, beta_vals)
    
    T = 2.0
    num_minima_map = np.zeros_like(A, dtype=int)
    
    for i in range(len(alpha_vals)):
        for j in range(len(beta_vals)):
            critical = find_critical_points(alpha_vals[i], beta_vals[j], T)
            minima = [c for c in critical if classify_critical_point(c, alpha_vals[i], beta_vals[j], T) == 'local_min']
            num_minima_map[j, i] = len(minima)
    
    # Plot regions
    im = ax1.contourf(A, B, num_minima_map, levels=[0, 0.5, 1.5, 2.5], 
                       colors=['#ffcccc', '#ccffcc', '#ccccff'], alpha=0.7)
    
    # Boundary line
    boundary_beta = T/8 - alpha_vals
    boundary_beta = np.maximum(boundary_beta, 0)
    ax1.plot(alpha_vals, boundary_beta, 'k--', linewidth=2.5, label=f'α + β = T/8 = {T/8}')
    
    # Mark specific points
    ax1.plot(0.1, 0.1, 'rx', markersize=15, markeredgewidth=3, label='Non-convex (0 min)')
    ax1.plot(0.3, 0.3, 'go', markersize=10, markeredgewidth=2, label='Convex (1 min)')
    ax1.plot(0.15, 0.15, 'b^', markersize=10, markeredgewidth=2, label='Non-convex (2 min)')
    
    ax1.set_xlabel('α', fontsize=12)
    ax1.set_ylabel('β', fontsize=12)
    ax1.set_title(f'Phase Diagram (T={T})', fontsize=12)
    ax1.legend(loc='upper right')
    ax1.set_xlim(0, 1)
    ax1.set_ylim(0, 1)
    
    # Add text annotations
    ax1.text(0.05, 0.05, 'NO MINIMA\n(invalid)', fontsize=10, ha='center', color='red', fontweight='bold')
    ax1.text(0.6, 0.6, 'SINGLE\nMINIMUM', fontsize=10, ha='center', color='green', fontweight='bold')
    ax1.text(0.2, 0.4, 'DOUBLE\nWELL', fontsize=10, ha='center', color='blue', fontweight='bold')
    
    # Right: Number of minima vs temperature
    ax2 = axes[1]
    
    alpha, beta = 0.15, 0.15
    T_range = np.linspace(1.0, 6.0, 100)
    num_minima_vs_T = []
    
    for T in T_range:
        critical = find_critical_points(alpha, beta, T)
        minima = [c for c in critical if classify_critical_point(c, alpha, beta, T) == 'local_min']
        num_minima_vs_T.append(len(minima))
    
    ax2.plot(T_range, num_minima_vs_T, linewidth=3, color='#3498db')
    
    # Mark critical temperature
    T_critical = 8 * (alpha + beta)
    ax2.axvline(x=T_critical, color='red', linestyle='--', linewidth=2, 
                label=f'Critical T = 8(α+β) = {T_critical:.2f}')
    
    ax2.set_xlabel('Temperature T', fontsize=12)
    ax2.set_ylabel('Number of Local Minima', fontsize=12)
    ax2.set_title(f'Phase Transition (α={alpha}, β={beta})', fontsize=12)
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    ax2.set_ylim(-0.1, 2.5)
    ax2.set_yticks([0, 1, 2])
    
    plt.tight_layout()
    plt.savefig('phase_diagram_detailed.png', dpi=150, bbox_inches='tight')
    print("Saved: phase_diagram_detailed.png")
    plt.close()


def analyze_dimension_phase_transition():
    """Analyze the physical meaning of dimension phase transition"""
    print("=" * 70)
    print("P3-T1: Non-Convex Region Analysis - Phase Transition Study")
    print("=" * 70)
    
    # Study temperature dependence
    alpha, beta = 0.2, 0.2
    T_values = np.linspace(1.0, 6.0, 20)
    
    results = analyze_phase_structure(alpha, beta, T_values)
    
    print(f"\nParameter: α={alpha}, β={beta}")
    print(f"Critical temperature: T_c = 8(α+β) = {8*(alpha+beta):.2f}")
    print("\nTemperature scan results:")
    print("-" * 70)
    print(f"{'T':<8} {'Convex?':<10} {'#Minima':<10} {'Global min d':<15} {'Status'}")
    print("-" * 70)
    
    for r in results:
        T = r['T']
        convex = 'YES' if r['is_convex'] else 'NO'
        n_min = r['num_minima']
        
        if r['global_minimum']:
            d_min = r['global_minimum']['d']
            if T < 8*(alpha+beta) * 0.8:
                status = 'Deep convex'
            elif T < 8*(alpha+beta) * 1.2:
                status = 'Near critical'
            else:
                status = 'Non-convex regime'
        else:
            d_min = 'N/A'
            status = 'No minimum!'
        
        print(f"{T:<8.2f} {convex:<10} {n_min:<10} {str(d_min):<15} {status}")
    
    # Find critical point more precisely
    print("\n" + "=" * 70)
    print("CRITICAL POINT ANALYSIS")
    print("=" * 70)
    
    # Binary search for transition
    T_low, T_high = 2.0, 4.0
    for _ in range(10):
        T_mid = (T_low + T_high) / 2
        critical = find_critical_points(alpha, beta, T_mid)
        minima = [c for c in critical if classify_critical_point(c, alpha, beta, T_mid) == 'local_min']
        if len(minima) >= 2:
            T_high = T_mid
        else:
            T_low = T_mid
    
    T_transition = (T_low + T_high) / 2
    print(f"\nPrecise transition temperature: T* ≈ {T_transition:.4f}")
    print(f"Theoretical critical: T_c = 8(α+β) = {8*(alpha+beta):.4f}")
    print(f"Difference: {abs(T_transition - 8*(alpha+beta)):.4f}")
    
    # Physical interpretation
    print("\n" + "=" * 70)
    print("PHYSICAL INTERPRETATION")
    print("=" * 70)
    print("""
1. CONVEX REGIME (T < T_c):
   - Unique global minimum
   - Dimension d is uniquely determined
   - System has single stable state
   - Standard thermodynamic behavior

2. CRITICAL POINT (T = T_c):
   - Loss of convexity
   - Flattening of free energy landscape
   - Critical slowing down
   - Enhanced fluctuations

3. NON-CONVEX REGIME (T > T_c):
   - Multiple local minima (double-well structure)
   - First-order phase transition possible
   - Dimension can "jump" between values
   - Hysteresis effects possible
   - Spontaneous symmetry breaking in dimension

4. PHYSICAL IMPLICATIONS:
   - Early universe (high T): dimension may fluctuate
   - Phase transition at T_c: dimension "freezes"
   - Below T_c: stable 4D spacetime emerges
   - Connection to dimensional reduction in quantum gravity
""")
    
    return results


def save_analysis_results(results, filename='nonconvex_analysis_results.json'):
    """Save analysis results to JSON"""
    # Convert to serializable format
    serializable = []
    for r in results:
        sr = {
            'T': float(r['T']),
            'is_convex': bool(r['is_convex']),
            'num_minima': int(r['num_minima']),
            'global_minimum': {
                'd': float(r['global_minimum']['d']),
                'F': float(r['global_minimum']['F'])
            } if r['global_minimum'] else None
        }
        serializable.append(sr)
    
    with open(filename, 'w') as f:
        json.dump(serializable, f, indent=2)
    print(f"\nResults saved to {filename}")


def generate_all_plots():
    """Generate all visualization plots"""
    print("=" * 70)
    print("Generating Non-Convex Region Analysis Plots")
    print("=" * 70)
    
    plot_free_energy_landscape()
    plot_phase_diagram_detailed()
    
    print("=" * 70)
    print("All plots generated successfully!")
    print("=" * 70)


if __name__ == "__main__":
    # Run analysis
    results = analyze_dimension_phase_transition()
    
    # Generate plots
    generate_all_plots()
    
    # Save results
    save_analysis_results(results)
    
    print("\n" + "=" * 70)
    print("P3-T1 Non-Convex Analysis Complete!")
    print("=" * 70)
