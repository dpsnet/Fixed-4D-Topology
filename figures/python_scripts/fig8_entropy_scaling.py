#!/usr/bin/env python3
"""
Figure 8: Entropy Scaling in Dimension Flow

Shows how Bekenstein-Hawking entropy scaling changes
with effective dimension: S ∝ A^(d_eff/2)
"""

import numpy as np
import matplotlib.pyplot as plt

def entropy_scaling(A, d_eff, G=1):
    """
    Entropy scaling with area A and dimension d_eff
    S ∝ A^(d_eff/2) / (G^(d_eff/2 - 1))
    """
    return A**(d_eff/2) / (G**(d_eff/2 - 1))

# Area range (in Planck units)
A = np.logspace(0, 6, 500)

# Different dimensions
dims = [
    (4, 'black', 'd = 4 (Standard)'),
    (3, 'blue', 'd = 3'),
    (2, 'red', 'd = 2 (Near-horizon)'),
]

fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# Left: Linear comparison
ax1 = axes[0]
for d_eff, color, label in dims:
    S = entropy_scaling(A, d_eff)
    ax1.loglog(A, S, color=color, lw=2.5, label=label)

ax1.set_xlabel(r'Horizon Area $A$ (Planck units)', fontsize=13)
ax1.set_ylabel(r'Entropy $S$', fontsize=13)
ax1.set_title(r'Entropy Scaling: $S \propto A^{d_{eff}/2}$', fontsize=14)
ax1.legend(fontsize=11)
ax1.grid(True, alpha=0.3)

# Add slope annotations
ax1.annotate('Slope = 2', xy=(100, 1e4), fontsize=10, color='black', alpha=0.7)
ax1.annotate('Slope = 1.5', xy=(100, 1e3), fontsize=10, color='blue', alpha=0.7)
ax1.annotate('Slope = 1', xy=(100, 100), fontsize=10, color='red', alpha=0.7)

# Right: Deviation from 4D
ax2 = axes[1]
S_4d = entropy_scaling(A, 4)

for d_eff, color, label in dims:
    if d_eff != 4:
        S = entropy_scaling(A, d_eff)
        ratio = S / S_4d
        ax2.loglog(A, ratio, color=color, lw=2.5, label=f'd = {d_eff}')

ax2.set_xlabel(r'Horizon Area $A$ (Planck units)', fontsize=13)
ax2.set_ylabel(r'$S/S_{d=4}$', fontsize=13)
ax2.set_title(r'Deviation from 4D Scaling', fontsize=14)
ax2.legend(fontsize=11)
ax2.grid(True, alpha=0.3)
ax2.axhline(y=1, color='gray', linestyle='--', alpha=0.5)

# Add physical interpretation
ax2.text(0.05, 0.95, 'For small black holes:\nQuantum effects dominate\n→ Lower effective dimension',
         transform=ax2.transAxes, fontsize=10, verticalalignment='top',
         bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

plt.tight_layout()
plt.savefig('../fig8_entropy_scaling.pdf', dpi=600, bbox_inches='tight')
plt.savefig('../fig8_entropy_scaling.png', dpi=600, bbox_inches='tight')
print('Figure 8 saved: entropy scaling')
