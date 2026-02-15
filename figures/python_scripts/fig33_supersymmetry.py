#!/usr/bin/env python3
"""
Figure 33: Supersymmetry and Dimension Flow

Explores the relationship between SUSY breaking and dimension flow.
"""

import numpy as np
import matplotlib.pyplot as plt

# Energy scale
E = np.logspace(2, 16, 500)

# SUSY breaking scale
M_susy = 1e3  # TeV (example)

# Dimension flow
d_eff = 2 + 2 / (1 + (E/1e16)**0.3)

# SUSY breaking parameter (simplified)
def susy_breaking(E, M_susy):
    """SUSY breaking strength"""
    return 1 / (1 + (M_susy/E)**2)

fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# Left: SUSY breaking vs dimension
ax1 = axes[0]
F = [susy_breaking(e, M_susy) for e in E]

ax1.semilogx(E, F, 'b-', lw=2.5, label='$F$-term breaking')
ax1_twin = ax1.twinx()
ax1_twin.semilogx(E, d_eff, 'r--', lw=2.5, label='Effective dimension')

ax1.axvline(x=M_susy, color='gray', linestyle=':', alpha=0.7)
ax1.set_xlabel('Energy $E$ (GeV)', fontsize=13)
ax1.set_ylabel('SUSY Breaking $F$', fontsize=13, color='blue')
ax1_twin.set_ylabel('Effective Dimension $d_{eff}$', fontsize=13, color='red')
ax1.set_title('SUSY Breaking and Dimension Flow', fontsize=14)
ax1.grid(True, alpha=0.3)

# Right: Superpartner spectrum
ax2 = axes[1]

# Masses in different dimensions
particles = ['$\\tilde{g}$', '$\\tilde{q}$', '$\\tilde{l}$', '$\\tilde{\\chi}^0$', '$\\tilde{\\chi}^\\pm$']
masses_4d = [2000, 1500, 300, 200, 250]  # GeV
masses_3d = [m * 0.8 for m in masses_4d]  # Modified in d=3

x = np.arange(len(particles))
width = 0.35

bars1 = ax2.bar(x - width/2, masses_4d, width, label='d = 4', color='blue', alpha=0.7)
bars2 = ax2.bar(x + width/2, masses_3d, width, label='d = 3', color='red', alpha=0.7)

ax2.set_ylabel('Mass (GeV)', fontsize=13)
ax2.set_title('Superpartner Spectrum', fontsize=14)
ax2.set_xticks(x)
ax2.set_xticklabels(particles, fontsize=11)
ax2.legend(fontsize=11)
ax2.grid(True, alpha=0.3, axis='y')

plt.tight_layout()
plt.savefig('../fig33_supersymmetry.pdf', dpi=600, bbox_inches='tight')
plt.savefig('../fig33_supersymmetry.png', dpi=600, bbox_inches='tight')
print('Figure 33 saved: supersymmetry')
