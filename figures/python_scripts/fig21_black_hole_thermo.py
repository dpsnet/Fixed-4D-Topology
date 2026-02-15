#!/usr/bin/env python3
"""
Figure 21: Black Hole Thermodynamics with Dimension Flow

Shows how thermodynamic relations change with varying spectral dimension.
"""

import numpy as np
import matplotlib.pyplot as plt

# Mass range (in solar masses)
M = np.logspace(0, 8, 500)

# Standard 4D relations
def T_hawking_4d(M):
    """Hawking temperature in 4D"""
    return 6.17e-8 / M  # K

def S_bekenstein_4d(M):
    """Bekenstein-Hawking entropy in 4D"""
    return 1.05e77 * M**2  # dimensionless

# Modified with dimension flow (d_eff = 2 near Planck scale)
def T_modified(M, M_planck=1e-5):
    """Modified temperature with dimension flow"""
    x = M / M_planck
    d_eff = 2 + 2 * np.tanh(np.log10(x))
    return T_hawking_4d(M) * (x)**((4-d_eff)/2)

def S_modified(M, M_planck=1e-5):
    """Modified entropy with dimension flow"""
    x = M / M_planck
    d_eff = 2 + 2 * np.tanh(np.log10(x))
    return S_bekenstein_4d(M) * (x)**((d_eff-4))

fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# Left: Temperature
ax1 = axes[0]
ax1.loglog(M, T_hawking_4d(M), 'b--', lw=2, label='Standard 4D')
ax1.loglog(M, T_modified(M), 'r-', lw=2.5, label='With Dimension Flow')

ax1.axvline(x=1e-5, color='gray', linestyle=':', alpha=0.7, label='Planck Mass')
ax1.set_xlabel('Black Hole Mass $M$ ($M_\odot$)', fontsize=13)
ax1.set_ylabel('Temperature $T$ (K)', fontsize=13)
ax1.set_title('Modified Hawking Temperature', fontsize=14)
ax1.legend(fontsize=11)
ax1.grid(True, alpha=0.3)

# Right: Entropy
ax2 = axes[1]
ax2.loglog(M, S_bekenstein_4d(M), 'b--', lw=2, label='Standard 4D')
ax2.loglog(M, S_modified(M), 'r-', lw=2.5, label='With Dimension Flow')

ax2.axvline(x=1e-5, color='gray', linestyle=':', alpha=0.7, label='Planck Mass')
ax2.set_xlabel('Black Hole Mass $M$ ($M_\odot$)', fontsize=13)
ax2.set_ylabel('Entropy $S$ ($k_B$)', fontsize=13)
ax2.set_title('Modified Bekenstein-Hawking Entropy', fontsize=14)
ax2.legend(fontsize=11)
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('../fig21_black_hole_thermo.pdf', dpi=600, bbox_inches='tight')
plt.savefig('../fig21_black_hole_thermo.png', dpi=600, bbox_inches='tight')
print('Figure 21 saved: black hole thermodynamics')
