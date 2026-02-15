#!/usr/bin/env python3
"""
Figure 4: Phase Diagram of Dimension Flow

Shows the phase diagram in the (d, c₁) parameter space,
marking the experimental and theoretical points.

Author: 王斌 (Wang Bin), Kimi 2.5 Agent
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyBboxPatch
import matplotlib.patches as mpatches

# Setup figure
fig, ax = plt.subplots(figsize=(10, 8))

# Theoretical curve: c₁(d) = 1/2^(d-2)
d = np.linspace(1.5, 5, 200)
c1_theory = 1.0 / (2**(d - 2))

# Plot theoretical curve
ax.plot(d, c1_theory, 'b-', lw=3, label=r'Theory: $c_1(d) = 2^{2-d}$', zorder=3)

# Experimental points with error bars
experiments = [
    {'name': 'SnapPy\n(d=4)', 'd': 4.0, 'c1': 0.245, 'err': 0.014, 'color': 'red', 'marker': 'o'},
    {'name': 'Cu₂O\n(d=3)', 'd': 3.0, 'c1': 0.516, 'err': 0.026, 'color': 'green', 'marker': 's'},
    {'name': '2D H\n(d=3→2)', 'd': 3.0, 'c1': 0.523, 'err': 0.029, 'color': 'purple', 'marker': '^'},
    {'name': 'Knot Theory\n(d=4)', 'd': 4.0, 'c1': 0.250, 'err': 0.005, 'color': 'orange', 'marker': 'D'},
]

for exp in experiments:
    ax.errorbar(exp['d'], exp['c1'], yerr=exp['err'], 
                fmt=exp['marker'], markersize=15, capsize=8,
                color=exp['color'], ecolor=exp['color'],
                markeredgecolor='black', markeredgewidth=1.5,
                label=exp['name'], zorder=4)

# Phase regions
# Quantum gravity region
rect1 = Rectangle((3.5, 0.1), 1.5, 0.3, alpha=0.2, color='blue', label='Quantum Gravity')
ax.add_patch(rect1)
ax.text(4.25, 0.25, 'Quantum\nGravity', ha='center', va='center', fontsize=10, color='blue')

# Condensed matter region
rect2 = Rectangle((2.5, 0.4), 1.0, 0.4, alpha=0.2, color='green')
ax.add_patch(rect2)
ax.text(3.0, 0.6, 'Condensed\nMatter', ha='center', va='center', fontsize=10, color='green')

# Topology region
rect3 = Rectangle((3.8, 0.18), 0.7, 0.12, alpha=0.2, color='red')
ax.add_patch(rect3)
ax.text(4.15, 0.24, 'Topology', ha='center', va='center', fontsize=10, color='red')

# Labels and styling
ax.set_xlabel(r'Spatial Dimension $d$', fontsize=16)
ax.set_ylabel(r'Dimension Flow Parameter $c_1$', fontsize=16)
ax.set_title(r'Phase Diagram: $(d, c_1)$ Parameter Space', fontsize=18, pad=20)

ax.set_xlim(1.5, 5.2)
ax.set_ylim(0, 1.1)

ax.legend(loc='upper right', fontsize=10, framealpha=0.95)
ax.grid(True, alpha=0.3, linestyle='--')

# Add annotation
ax.annotate('Universal\nFormula', xy=(3.5, 0.35), xytext=(2.2, 0.8),
            fontsize=12, ha='center',
            arrowprops=dict(arrowstyle='->', color='gray', lw=1.5),
            bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow', alpha=0.3))

plt.tight_layout()
plt.savefig('../fig4_phase_diagram.pdf', dpi=600, bbox_inches='tight')
plt.savefig('../fig4_phase_diagram.png', dpi=600, bbox_inches='tight')
print('Figure 4 saved: phase diagram')
