#!/usr/bin/env python3
"""
Figure 10: Experimental Landscape

Overview of all experiments and observations relevant to
dimension flow validation across different energy scales.
"""

import numpy as np
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(14, 10))

# Experiment categories
experiments = [
    # (name, energy_scale_GeV, precision_c1, field, color)
    ('Cu₂O Excitons', 1e-9, 0.05, 'Condensed Matter', 'green'),
    ('2D Hydrogen', 1e-9, 0.06, 'AMO Physics', 'green'),
    ('Cold Atoms', 1e-12, 0.10, 'AMO Physics', 'lightgreen'),
    ('Superfluid He', 1e-12, 0.15, 'Condensed Matter', 'lightgreen'),
    ('LIGO (GW)', 1e-24, 0.20, 'Gravitational Waves', 'blue'),
    ('LISA (proj.)', 1e-27, 0.15, 'Gravitational Waves', 'lightblue'),
    ('CMB (Planck)', 1e-4, 0.05, 'Cosmology', 'red'),
    ('CMB-S4 (proj.)', 1e-4, 0.02, 'Cosmology', 'pink'),
    ('LHC', 1e4, 0.30, 'Particle Physics', 'purple'),
    ('FCC (proj.)', 1e5, 0.25, 'Particle Physics', 'plum'),
    ('Cosmic Rays', 1e11, 0.50, 'Astroparticle', 'orange'),
    ('SnapPy (Math)', 0, 0.014, 'Mathematics', 'gray'),
    ('Knot Theory', 0, 0.02, 'Mathematics', 'lightgray'),
]

# Plot
for name, E, prec, field, color in experiments:
    if E > 0:
        ax.scatter(E, prec, s=300, c=color, alpha=0.7, edgecolors='black', linewidths=1.5)
        ax.annotate(name, (E, prec), xytext=(10, 5), textcoords='offset points',
                   fontsize=9, bbox=dict(boxstyle='round,pad=0.3', 
                   facecolor=color, alpha=0.3, edgecolor='black'))

# Theory point
ax.scatter([1e16], [0.001], s=500, c='gold', marker='*', 
           edgecolors='black', linewidths=2, label='Theory (Planck)', zorder=10)
ax.annotate('Theory\n(Planck Scale)', (1e16, 0.001), xytext=(-50, 20), 
            textcoords='offset points', fontsize=10, ha='center',
            arrowprops=dict(arrowstyle='->', color='gold', lw=2),
            bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.5))

# Formatting
ax.set_xscale('log')
ax.set_yscale('log')
ax.set_xlabel(r'Energy Scale $E$ (GeV)', fontsize=14)
ax.set_ylabel(r'Precision on $c_1$ ($\sigma_{c_1}$)', fontsize=14)
ax.set_title(r'Experimental Landscape for Dimension Flow', fontsize=16, pad=20)

# Add vertical bands for different regimes
ax.axvspan(1e-28, 1e-10, alpha=0.1, color='blue', label='GW/Cosmology')
ax.axvspan(1e-10, 1e-3, alpha=0.1, color='green', label='Condensed Matter')
ax.axvspan(1e-3, 1e8, alpha=0.1, color='red', label='CMB/Particle')

ax.set_xlim(1e-28, 1e20)
ax.set_ylim(5e-4, 1)
ax.grid(True, alpha=0.3, which='both')
ax.legend(loc='upper left', fontsize=10)

# Add annotation
ax.text(0.02, 0.98, 'Lower = Better Precision', transform=ax.transAxes,
        fontsize=10, verticalalignment='top',
        bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

plt.tight_layout()
plt.savefig('../fig10_experimental_landscape.pdf', dpi=600, bbox_inches='tight')
plt.savefig('../fig10_experimental_landscape.png', dpi=600, bbox_inches='tight')
print('Figure 10 saved: experimental landscape')
