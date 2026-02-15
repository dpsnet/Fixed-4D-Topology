#!/usr/bin/env python3
"""
Figure 3: Three-system correspondence
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc

rc('font', family='serif')
rc('text', usetex=True)

fig, axes = plt.subplots(1, 3, figsize=(15, 5))

epsilon = np.linspace(0, 2, 200)
d_min = 2.5
d_max = 4.0
alpha = 1.7

def d_eff(eps, d_min, d_max, alpha, eps_c):
    return d_min + (d_max - d_min) / (1 + (eps/eps_c)**alpha)

# Panel A: Rotation
ax = axes[0]
eps_c_rot = 0.9
d_rot = d_eff(epsilon, d_min, d_max, alpha, eps_c_rot)
ax.plot(epsilon, d_rot, 'b-', lw=3)
ax.set_xlabel(r'Constraint $\epsilon = \omega^2 r^2/c^2$', fontsize=12)
ax.set_ylabel(r'Effective dimension $d_{\rm eff}$', fontsize=12)
ax.set_title(r'(a) Rotation System', fontsize=14)
ax.set_ylim([2, 4.5])
ax.grid(True, alpha=0.3)
ax.text(0.5, 3.8, 'E-6 Experiment', fontsize=12, bbox=dict(boxstyle='round', facecolor='wheat'))

# Panel B: Black Hole
ax = axes[1]
eps_c_bh = 1.0
d_bh = d_eff(epsilon, 2.0, 4.0, 0.5, eps_c_bh)
ax.plot(epsilon, d_bh, 'r-', lw=3)
ax.set_xlabel(r'Constraint $\epsilon = r_s/r$', fontsize=12)
ax.set_ylabel(r'Effective dimension $d_{\rm eff}$', fontsize=12)
ax.set_title(r'(b) Black Hole (Schwarzschild)', fontsize=14)
ax.set_ylim([1.5, 4.5])
ax.grid(True, alpha=0.3)
ax.text(0.5, 3.8, 'Near-horizon', fontsize=12, bbox=dict(boxstyle='round', facecolor='lightblue'))

# Panel C: Quantum Gravity
ax = axes[2]
eps_c_qg = 1.0
d_qg = d_eff(epsilon, 2.0, 4.0, 0.5, eps_c_qg)
ax.plot(epsilon, d_qg, 'g-', lw=3)
ax.set_xlabel(r'Constraint $\epsilon = E/E_P$', fontsize=12)
ax.set_ylabel(r'Effective dimension $d_{\rm eff}$', fontsize=12)
ax.set_title(r'(c) Quantum Gravity', fontsize=14)
ax.set_ylim([1.5, 4.5])
ax.grid(True, alpha=0.3)
ax.text(0.5, 3.8, 'Planck scale', fontsize=12, bbox=dict(boxstyle='round', facecolor='lightgreen'))

plt.tight_layout()
plt.savefig('../fig3_three_systems.pdf', dpi=300, bbox_inches='tight')
plt.savefig('../fig3_three_systems.png', dpi=300, bbox_inches='tight')
print('Figure 3 saved: three_systems.pdf/.png')
