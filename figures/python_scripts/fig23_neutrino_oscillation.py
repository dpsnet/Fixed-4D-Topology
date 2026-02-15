#!/usr/bin/env python3
"""
Figure 23: Neutrino Oscillations in Varying Dimensions

Shows how neutrino oscillation probabilities are modified
dimension flow at different energy scales.
"""

import numpy as np
import matplotlib.pyplot as plt

def oscillation_prob(E, L, d_eff, theta=np.pi/4, dm2=2.5e-3):
    """
    Neutrino oscillation probability with dimension flow
    P ~ sin²(2θ) sin²(1.27 Δm² L / E^(d_eff/2))
    """
    argument = 1.27 * dm2 * L / (E**(d_eff/2))
    return np.sin(2*theta)**2 * np.sin(argument)**2

# Energy range (GeV)
E = np.logspace(-1, 2, 500)
L = 1000  # km (atmospheric neutrinos)

fig, ax = plt.subplots(figsize=(10, 6))

dims = [(4, 'black', 'd=4 (Standard)'),
        (3.5, 'blue', 'd=3.5'),
        (3, 'green', 'd=3.0'),
        (2.5, 'red', 'd=2.5')]

for d_eff, color, label in dims:
    P = oscillation_prob(E, L, d_eff)
    ax.semilogx(E, P, color=color, lw=2.5, label=label)

ax.set_xlabel('Neutrino Energy $E$ (GeV)', fontsize=13)
ax.set_ylabel(r'Oscillation Probability $P_{\mu e}$', fontsize=13)
ax.set_title(f'Neutrino Oscillations at L={L} km', fontsize=14)
ax.legend(fontsize=11)
ax.set_ylim(0, 1.1)
ax.grid(True, alpha=0.3)

# Add annotation
ax.text(0.02, 0.95, 'Dimension flow modifies\noscillation wavelength', 
        transform=ax.transAxes, fontsize=10, verticalalignment='top',
        bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

plt.tight_layout()
plt.savefig('../fig23_neutrino_oscillation.pdf', dpi=600, bbox_inches='tight')
plt.savefig('../fig23_neutrino_oscillation.png', dpi=600, bbox_inches='tight')
print('Figure 23 saved: neutrino oscillations')
