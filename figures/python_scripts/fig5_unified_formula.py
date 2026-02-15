#!/usr/bin/env python3
"""
Figure 5: Unified Dimension Flow Formula

Visual representation of the universal formula:
c₁(d,w) = 1/2^(d-2+w)

Shows how c₁ varies with both spatial (d) and time (w) dimensions.
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

fig = plt.figure(figsize=(14, 6))

# Left panel: 3D surface
ax1 = fig.add_subplot(121, projection='3d')

d = np.linspace(2, 5, 50)
w = np.linspace(0, 2, 50)
D, W = np.meshgrid(d, w)

C1 = 1.0 / (2**(D - 2 + W))

surf = ax1.plot_surface(D, W, C1, cmap='viridis', alpha=0.8, edgecolor='none')
ax1.set_xlabel('Spatial d', fontsize=12)
ax1.set_ylabel('Time w', fontsize=12)
ax1.set_zlabel('$c_1$', fontsize=12)
ax1.set_title(r'Universal Formula: $c_1(d,w) = 2^{2-d-w}$', fontsize=14)
fig.colorbar(surf, ax=ax1, shrink=0.5, aspect=10)

# Right panel: Contour plot
ax2 = fig.add_subplot(122)

contour = ax2.contourf(D, W, C1, levels=20, cmap='viridis')
ax2.contour(D, W, C1, levels=10, colors='white', linewidths=0.5, alpha=0.5)

# Mark specific points
points = [
    (4, 0, 0.25, 'SnapPy\n(4,0)'),
    (3, 0, 0.50, 'Cu₂O\n(3,0)'),
    (2, 0, 1.00, '2D H₂\n(2,0)'),
    (3, 1, 0.25, 'QFT\n(3,1)'),
    (4, 1, 0.125, 'String\n(4,1)'),
]

for d_pt, w_pt, c1_pt, label in points:
    ax2.plot(d_pt, w_pt, 'ro', markersize=12, markeredgecolor='white', markeredgewidth=2)
    ax2.annotate(label, (d_pt, w_pt), xytext=(10, 10), textcoords='offset points',
                 fontsize=9, bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow', alpha=0.7))

ax2.set_xlabel(r'Spatial Dimension $d$', fontsize=14)
ax2.set_ylabel(r'Time Dimension $w$', fontsize=14)
ax2.set_title(r'$c_1(d,w)$ Contour Map', fontsize=14)
ax2.grid(True, alpha=0.3)
plt.colorbar(contour, ax=ax2, label='$c_1$ value')

plt.tight_layout()
plt.savefig('../fig5_unified_formula.pdf', dpi=600, bbox_inches='tight')
plt.savefig('../fig5_unified_formula.png', dpi=600, bbox_inches='tight')
print('Figure 5 saved: unified formula')
