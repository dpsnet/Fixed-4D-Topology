#!/usr/bin/env python3
"""
Figure 6: Spectral Dimension Flow Comparison

Compares dimension flow across different physical systems:
- Rotation systems (centrifugal)
- Black holes (gravity)
- Quantum gravity (CDT, ASG)
"""

import numpy as np
import matplotlib.pyplot as plt

def dimension_flow_generic(eps, d_max, d_min, eps_c, alpha):
    """Generic dimension flow formula"""
    return d_min + (d_max - d_min) / (1 + (eps/eps_c)**alpha)

# Parameters
eps = np.logspace(-2, 2, 500)

# Different systems
systems = [
    {
        'name': 'Rotation (E-6)',
        'd_max': 4, 'd_min': 2.5, 'eps_c': 1.0, 'alpha': 1.0,
        'color': 'blue', 'style': '-'
    },
    {
        'name': 'Schwarzschild BH',
        'd_max': 4, 'd_min': 2.0, 'eps_c': 0.5, 'alpha': 1.2,
        'color': 'red', 'style': '--'
    },
    {
        'name': 'CDT Quantum Gravity',
        'd_max': 4, 'd_min': 2.0, 'eps_c': 0.8, 'alpha': 1.5,
        'color': 'green', 'style': '-.'
    },
    {
        'name': 'ASG (Frankfurt)',
        'd_max': 4, 'd_min': 2.0, 'eps_c': 1.2, 'alpha': 1.1,
        'color': 'purple', 'style': ':'
    },
    {
        'name': 'Hořava-Lifshitz',
        'd_max': 4, 'd_min': 2.0, 'eps_c': 0.6, 'alpha': 2.0,
        'color': 'orange', 'style': '-'
    },
]

fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# Left panel: Linear scale
ax1 = axes[0]
for sys in systems:
    d_s = dimension_flow_generic(eps, sys['d_max'], sys['d_min'], 
                                  sys['eps_c'], sys['alpha'])
    ax1.plot(eps, d_s, sys['style'], color=sys['color'], lw=2.5, 
             label=sys['name'])

ax1.set_xlabel(r'Energy Scale $\varepsilon/\varepsilon_c$', fontsize=14)
ax1.set_ylabel(r'Spectral Dimension $d_s$', fontsize=14)
ax1.set_title(r'Dimension Flow: Linear Scale', fontsize=15)
ax1.set_xlim(0, 3)
ax1.set_ylim(1.5, 4.5)
ax1.legend(loc='upper right', fontsize=10)
ax1.grid(True, alpha=0.3)
ax1.axhline(y=4, color='gray', linestyle='--', alpha=0.5, label='$d_{IR}=4$')
ax1.axhline(y=2, color='gray', linestyle='--', alpha=0.5, label='$d_{UV}=2$')

# Right panel: Log scale
ax2 = axes[1]
for sys in systems:
    d_s = dimension_flow_generic(eps, sys['d_max'], sys['d_min'], 
                                  sys['eps_c'], sys['alpha'])
    ax2.semilogx(eps, d_s, sys['style'], color=sys['color'], lw=2.5, 
                 label=sys['name'])

ax2.set_xlabel(r'Energy Scale $\varepsilon/\varepsilon_c$ (log)', fontsize=14)
ax2.set_ylabel(r'Spectral Dimension $d_s$', fontsize=14)
ax2.set_title(r'Dimension Flow: Log Scale', fontsize=15)
ax2.set_ylim(1.5, 4.5)
ax2.legend(loc='center right', fontsize=10)
ax2.grid(True, alpha=0.3)
ax2.axhline(y=4, color='gray', linestyle='--', alpha=0.5)
ax2.axhline(y=2, color='gray', linestyle='--', alpha=0.5)

# Add transition region annotation
ax2.axvspan(0.5, 2.0, alpha=0.1, color='yellow', label='Transition')
ax2.text(1.0, 3.3, 'Transition\nRegion', ha='center', fontsize=10, 
         bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.3))

plt.tight_layout()
plt.savefig('../fig6_spectral_flow_comparison.pdf', dpi=600, bbox_inches='tight')
plt.savefig('../fig6_spectral_flow_comparison.png', dpi=600, bbox_inches='tight')
print('Figure 6 saved: spectral flow comparison')
