#!/usr/bin/env python3
"""
Figure 12: Holographic Duality in Dimension Flow

Visualizes the AdS/CFT correspondence in the context of dimension flow.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Rectangle
import matplotlib.patches as mpatches

fig, ax = plt.subplots(figsize=(12, 10))

# Draw AdS space (bulk)
ads = plt.Polygon([[2, 1], [8, 1], [9, 9], [1, 9]], 
                  closed=True, fill=True, facecolor='lightblue', 
                  edgecolor='blue', linewidth=2, alpha=0.3)
ax.add_patch(ads)
ax.text(5, 8, 'AdS$_{d+1}$ Bulk\n(Quantum Gravity)', 
        ha='center', va='center', fontsize=14, fontweight='bold')

# Draw CFT boundary
cft = plt.Polygon([[1.5, 9], [8.5, 9], [8.3, 9.5], [1.7, 9.5]], 
                  closed=True, fill=True, facecolor='lightyellow', 
                  edgecolor='orange', linewidth=2)
ax.add_patch(cft)
ax.text(5, 9.25, 'CFT$_d$ Boundary\n(Quantum Field Theory)', 
        ha='center', va='center', fontsize=12, fontweight='bold')

# Draw dimension flow arrows
arrow1 = FancyArrowPatch((3, 7), (3, 9), 
                        arrowstyle='->', mutation_scale=30, 
                        color='red', lw=3)
ax.add_patch(arrow1)
ax.text(2.3, 8, 'IR\n$d_{eff}=d$', fontsize=10, color='red', ha='center')

arrow2 = FancyArrowPatch((7, 3), (7, 9), 
                        arrowstyle='->', mutation_scale=30, 
                        color='purple', lw=3)
ax.add_patch(arrow2)
ax.text(7.7, 6, 'UV\n$d_{eff}=2$', fontsize=10, color='purple', ha='center')

# Add radial coordinate label
ax.text(9.3, 5, r'Radial direction $z$', fontsize=12, rotation=90, va='center')
ax.annotate('', xy=(9.2, 8.5), xytext=(9.2, 1.5),
            arrowprops=dict(arrowstyle='->', color='black', lw=2))

# Add energy scale
ax.text(0.5, 5, r'Energy $\varepsilon$', fontsize=12, rotation=90, va='center')
ax.annotate('', xy=(0.3, 8.5), xytext=(0.3, 1.5),
            arrowprops=dict(arrowstyle='->', color='black', lw=2))
ax.text(-0.2, 1.5, 'Low', fontsize=9)
ax.text(-0.2, 8.5, 'High', fontsize=9)

# Key equations
ax.text(5, 0.3, r'$d_s^{CFT}(\varepsilon) = d_s^{Bulk}(z)$ where $z \sim 1/\varepsilon$', 
        ha='center', fontsize=11, 
        bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

ax.set_xlim(-1, 11)
ax.set_ylim(0, 10.5)
ax.set_aspect('equal')
ax.axis('off')
ax.set_title('Holographic Duality and Dimension Flow', fontsize=16, pad=20)

plt.tight_layout()
plt.savefig('../fig12_holographic_duality.pdf', dpi=600, bbox_inches='tight')
plt.savefig('../fig12_holographic_duality.png', dpi=600, bbox_inches='tight')
print('Figure 12 saved: holographic duality')
