#!/usr/bin/env python3
"""
Figure 34: String Compactification and Dimension Flow

Visualizes how compactification affects dimension flow.
"""

import numpy as np
import matplotlib.pyplot as plt

# Compactification radius
R = np.logspace(-2, 2, 500)

# Effective dimension from compactification
def compactified_dimension(R, d_bulk=10, d_compact=6):
    """
    Effective dimension as function of compactification radius
    """
    # At small R, compactified dimensions are invisible
    visibility = R**2 / (1 + R**2)
    return d_bulk - d_compact * (1 - visibility)

fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# Left: Dimension vs compactification radius
ax1 = axes[0]
d_eff = [compactified_dimension(r) for r in R]

ax1.semilogx(R, d_eff, 'b-', lw=3)
ax1.axhline(y=10, color='gray', linestyle='--', alpha=0.5, label='Bulk d=10')
ax1.axhline(y=4, color='red', linestyle='--', alpha=0.5, label='Observable d=4')
ax1.axvline(x=1, color='green', linestyle=':', alpha=0.7, label='String Scale')

ax1.set_xlabel(r'Compactification Radius $R/R_s$', fontsize=13)
ax1.set_ylabel('Effective Dimension $d_{eff}$', fontsize=13)
ax1.set_title('String Compactification', fontsize=14)
ax1.legend(fontsize=11)
ax1.set_ylim(3, 11)
ax1.grid(True, alpha=0.3)

# Right: Calabi-Yau manifold schematic
ax2 = axes[1]

# Create a schematic representation
theta = np.linspace(0, 2*np.pi, 100)

# Torus-like structure (simplified Calabi-Yau representation)
for i in range(5):
    r = 1 + 0.3 * np.sin(5*theta + i*np.pi/3)
    x = r * np.cos(theta) * (1 + 0.1*i)
    y = r * np.sin(theta) * (1 + 0.1*i)
    ax2.plot(x, y, lw=1.5, alpha=0.7)

# Add fiber structure
for angle in np.linspace(0, 2*np.pi, 8, endpoint=False):
    x_fiber = [0, 1.5*np.cos(angle)]
    y_fiber = [0, 1.5*np.sin(angle)]
    ax2.plot(x_fiber, y_fiber, 'b--', alpha=0.3)

ax2.set_aspect('equal')
ax2.axis('off')
ax2.set_title('Calabi-Yau Manifold (Schematic)', fontsize=14)

# Add text annotation
ax2.text(0, -2, 'Compactified 6 dimensions\n→ 4D effective theory', 
         ha='center', fontsize=11, 
         bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

plt.tight_layout()
plt.savefig('../fig34_string_compactification.pdf', dpi=600, bbox_inches='tight')
plt.savefig('../fig34_string_compactification.png', dpi=600, bbox_inches='tight')
print('Figure 34 saved: string compactification')
