#!/usr/bin/env python3
"""
Figure 13: Renormalization Group Flow in Dimension Space

Shows the RG flow trajectories in the space of dimension operators.
"""

import numpy as np
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(10, 8))

# Create grid
g1 = np.linspace(-2, 2, 20)
g2 = np.linspace(-2, 2, 20)
G1, G2 = np.meshgrid(g1, g2)

# RG flow equations (simplified)
dg1 = -G1 + 0.5 * G2
dg2 = 0.3 * G1 - 0.8 * G2

# Normalize arrows
M = np.sqrt(dg1**2 + dg2**2)
dg1_norm = dg1 / M
dg2_norm = dg2 / M

# Plot flow
ax.quiver(G1, G2, dg1_norm, dg2_norm, M, scale=30, cmap='viridis', alpha=0.7)

# Plot some trajectories
t = np.linspace(0, 10, 100)
for x0, y0 in [(-1.5, 1.5), (1.5, 1.5), (-1.5, -1.5), (1.5, -1.5), (0, 1.8)]:
    # Simple integration
    x, y = [x0], [y0]
    dt = 0.1
    for _ in range(100):
        dx = (-x[-1] + 0.5*y[-1]) * dt
        dy = (0.3*x[-1] - 0.8*y[-1]) * dt
        x.append(x[-1] + dx)
        y.append(y[-1] + dy)
    ax.plot(x, y, 'w-', lw=2, alpha=0.8)

# Fixed points
ax.plot(0, 0, 'r*', markersize=20, label='Gaussian Fixed Point', zorder=10)
ax.plot(-1.2, -0.8, 'go', markersize=15, label='Non-Gaussian FP', zorder=10)

# Labels
ax.set_xlabel(r'Coupling $g_1$ (Dimension Operator)', fontsize=13)
ax.set_ylabel(r'Coupling $g_2$ (Curvature)', fontsize=13)
ax.set_title('RG Flow in Theory Space', fontsize=15)
ax.legend(loc='upper right', fontsize=11)
ax.set_xlim(-2.2, 2.2)
ax.set_ylim(-2.2, 2.2)
ax.grid(True, alpha=0.3)

# Add annotation
ax.text(0.05, 0.95, 'Arrows point toward IR', transform=ax.transAxes,
        fontsize=10, verticalalignment='top',
        bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

plt.tight_layout()
plt.savefig('../fig13_renormalization_flow.pdf', dpi=600, bbox_inches='tight')
plt.savefig('../fig13_renormalization_flow.png', dpi=600, bbox_inches='tight')
print('Figure 13 saved: RG flow')
