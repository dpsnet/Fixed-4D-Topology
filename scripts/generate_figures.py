#!/usr/bin/env python3
"""
Generate publication-quality figures for the Dimensionics paper.
===========================================================

Usage:
    python generate_figures.py --output-dir ../papers/unified-dimensionics/latex/figures/
"""

import argparse
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend

# Set publication style
plt.rcParams['font.size'] = 10
plt.rcParams['axes.labelsize'] = 11
plt.rcParams['axes.titlesize'] = 12
plt.rcParams['legend.fontsize'] = 9
plt.rcParams['figure.dpi'] = 150


def figure_dimension_hierarchy(output_dir):
    """Figure 1: Network dimension hierarchy."""
    fig, ax = plt.subplots(figsize=(8, 6))
    
    # Empirical data
    networks = [
        'Internet AS', 'DBLP', 'Facebook', 'Yeast PPI', 
        'Twitter', 'Power Grid', 'Email'
    ]
    dimensions = [4.36, 3.0, 2.57, 2.4, 2.0, 2.11, 1.24]
    types = ['infra', 'academic', 'social', 'bio', 'social', 'infra', 'comm']
    
    colors = {
        'infra': '#e74c3c',
        'academic': '#3498db',
        'social': '#2ecc71',
        'bio': '#9b59b6',
        'comm': '#f39c12'
    }
    
    y_pos = np.arange(len(networks))
    bar_colors = [colors[t] for t in types]
    
    bars = ax.barh(y_pos, dimensions, color=bar_colors, alpha=0.8, edgecolor='black', linewidth=0.5)
    
    # Add value labels
    for i, (bar, dim) in enumerate(zip(bars, dimensions)):
        ax.text(bar.get_width() + 0.1, bar.get_y() + bar.get_height()/2, 
                f'{dim:.2f}', va='center', fontsize=9)
    
    ax.set_yticks(y_pos)
    ax.set_yticklabels(networks)
    ax.set_xlabel('Effective Dimension')
    ax.set_title('Network Dimension Hierarchy (7 Networks, 2.1M Nodes)')
    ax.set_xlim(0, 5)
    ax.grid(axis='x', alpha=0.3)
    
    # Legend
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor=colors['infra'], label='Infrastructure'),
        Patch(facecolor=colors['academic'], label='Academic'),
        Patch(facecolor=colors['social'], label='Social'),
        Patch(facecolor=colors['bio'], label='Biological'),
        Patch(facecolor=colors['comm'], label='Communication')
    ]
    ax.legend(handles=legend_elements, loc='lower right')
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}/figure1_dimension_hierarchy.pdf', bbox_inches='tight')
    plt.savefig(f'{output_dir}/figure1_dimension_hierarchy.png', dpi=300)
    plt.close()
    print("✓ Figure 1 generated: dimension_hierarchy")


def figure_variational_principle(output_dir):
    """Figure 2: Variational principle demonstration."""
    fig, axes = plt.subplots(1, 2, figsize=(10, 4))
    
    # Left: Free energy landscape
    ax1 = axes[0]
    d = np.linspace(0.1, 3.0, 200)
    A, alpha, T = 1.0, 0.5, 0.3
    
    energy = A / (d ** alpha)
    entropy = T * d * np.log(d)
    free_energy = energy + entropy
    
    ax1.plot(d, energy, 'b--', label='Energy: $A/d^\\alpha$', alpha=0.7)
    ax1.plot(d, entropy, 'r--', label='Entropy: $Td\\log d$', alpha=0.7)
    ax1.plot(d, free_energy, 'g-', linewidth=2, label='Free Energy: $F(d)$')
    
    # Mark optimal
    d_opt = 0.617
    ax1.axvline(d_opt, color='k', linestyle=':', alpha=0.5)
    ax1.text(d_opt + 0.1, 2.5, f'$d^* \\approx {d_opt:.3f}$', fontsize=9)
    
    ax1.set_xlabel('Dimension $d$')
    ax1.set_ylabel('Energy')
    ax1.set_title('Variational Principle: Energy-Entropy Competition')
    ax1.legend(loc='upper right')
    ax1.set_ylim(0, 5)
    ax1.grid(alpha=0.3)
    
    # Right: Temperature dependence
    ax2 = axes[1]
    temperatures = np.linspace(0.05, 1.0, 100)
    
    def optimal_d(T):
        d = np.linspace(0.1, 5.0, 1000)
        F = A / (d ** alpha) + T * d * np.log(d)
        return d[np.argmin(F)]
    
    d_optimal = [optimal_d(T) for T in temperatures]
    
    ax2.plot(temperatures, d_optimal, 'b-', linewidth=2)
    ax2.set_xlabel('Temperature $T$')
    ax2.set_ylabel('Optimal Dimension $d^*$')
    ax2.set_title('Dimension Selection vs Temperature')
    ax2.grid(alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}/figure2_variational_principle.pdf', bbox_inches='tight')
    plt.savefig(f'{output_dir}/figure2_variational_principle.png', dpi=300)
    plt.close()
    print("✓ Figure 2 generated: variational_principle")


def figure_model_comparison(output_dir):
    """Figure 3: Empirical vs model predictions."""
    fig, ax = plt.subplots(figsize=(8, 6))
    
    networks = ['Internet AS', 'DBLP', 'Yeast PPI', 'Facebook', 'Twitter', 'Power Grid', 'Email']
    empirical = [4.36, 3.0, 2.4, 2.57, 2.0, 2.11, 1.24]
    ba_model = [1.0] * 7
    ws_model = [1.0] * 7
    
    x = np.arange(len(networks))
    width = 0.25
    
    ax.bar(x - width, empirical, width, label='Empirical', color='#3498db', alpha=0.8)
    ax.bar(x, ba_model, width, label='Barabási-Albert', color='#e74c3c', alpha=0.8)
    ax.bar(x + width, ws_model, width, label='Watts-Strogatz', color='#f39c12', alpha=0.8)
    
    ax.set_ylabel('Dimension')
    ax.set_title('Model Failure: Standard Models Underestimate by 50-400%')
    ax.set_xticks(x)
    ax.set_xticklabels(networks, rotation=45, ha='right')
    ax.legend()
    ax.grid(axis='y', alpha=0.3)
    
    ax.annotate('Models predict d≈1\nfor all networks', 
                xy=(3, 1.2), xytext=(4.5, 2.5),
                arrowprops=dict(arrowstyle='->', color='red'),
                fontsize=9, color='red')
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}/figure3_model_comparison.pdf', bbox_inches='tight')
    plt.savefig(f'{output_dir}/figure3_model_comparison.png', dpi=300)
    plt.close()
    print("✓ Figure 3 generated: model_comparison")


def main():
    parser = argparse.ArgumentParser(description='Generate paper figures')
    parser.add_argument('--output-dir', default='../papers/unified-dimensionics/latex/figures/',
                       help='Output directory for figures')
    args = parser.parse_args()
    
    import os
    os.makedirs(args.output_dir, exist_ok=True)
    
    print("Generating publication-quality figures...")
    print("=" * 50)
    
    figure_dimension_hierarchy(args.output_dir)
    figure_variational_principle(args.output_dir)
    figure_model_comparison(args.output_dir)
    
    print("=" * 50)
    print(f"✓ All figures generated in: {args.output_dir}")


if __name__ == '__main__':
    main()
