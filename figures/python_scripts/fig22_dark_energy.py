#!/usr/bin/env python3
"""
Figure 22: Dark Energy and Dimension Flow

Shows the relationship between dark energy equation of state
and dimension flow parameters.
"""

import numpy as np
import matplotlib.pyplot as plt

def w_dark_energy(z, c1, w0=-1):
    """
    Dark energy equation of state with dimension flow
    w(z) = w0 + c1 * ln(1+z)
    """
    return w0 + c1 * np.log(1 + z)

# Redshift
z = np.linspace(0, 2, 500)

fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# Left: w(z) for different c1
ax1 = axes[0]
c1_values = [0, 0.1, 0.25, 0.5, 1.0]
colors = plt.cm.viridis(np.linspace(0, 1, len(c1_values)))

for c1, color in zip(c1_values, colors):
    w = w_dark_energy(z, c1)
    ax1.plot(z, w, color=color, lw=2.5, label=f'$c_1$ = {c1}')

ax1.axhline(y=-1, color='gray', linestyle='--', alpha=0.5, label='$\Lambda$CDM')
ax1.set_xlabel('Redshift $z$', fontsize=13)
ax1.set_ylabel('Equation of State $w(z)$', fontsize=13)
ax1.set_title('Dark Energy EoS with Dimension Flow', fontsize=14)
ax1.legend(fontsize=10)
ax1.set_ylim(-2, -0.5)
ax1.grid(True, alpha=0.3)

# Right: Contour plot of w vs (z, c1)
ax2 = axes[1]

z_grid = np.linspace(0, 2, 100)
c1_grid = np.linspace(0, 1, 100)
Z, C1 = np.meshgrid(z_grid, c1_grid)
W = w_dark_energy(Z, C1)

contour = ax2.contourf(Z, C1, W, levels=20, cmap='RdBu_r', vmin=-2, vmax=0)
ax2.contour(Z, C1, W, levels=[-1], colors='black', linewidths=2, linestyles='--')

# Mark current universe
ax2.plot(0, 0.5, 'w*', markersize=20, markeredgecolor='black', markeredgewidth=1)
ax2.annotate('Current\n$z=0, c_1=0.5$', (0, 0.5), xytext=(0.5, 0.7),
             fontsize=10, bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

ax2.set_xlabel('Redshift $z$', fontsize=13)
ax2.set_ylabel('Dimension Flow $c_1$', fontsize=13)
ax2.set_title('$w(z, c_1)$ Contour', fontsize=14)
plt.colorbar(contour, ax=ax2, label='$w$')

plt.tight_layout()
plt.savefig('../fig22_dark_energy.pdf', dpi=600, bbox_inches='tight')
plt.savefig('../fig22_dark_energy.png', dpi=600, bbox_inches='tight')
print('Figure 22 saved: dark energy')
