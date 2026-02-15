#!/usr/bin/env python3
"""
Figure 7: Gravitational Wave Propagation in Varying Dimensions

Shows how gravitational waves are affected by dimension flow,
predicting frequency-dependent propagation effects.
"""

import numpy as np
import matplotlib.pyplot as plt

def gw_phase_velocity(f, d_s, c=1):
    """
    Phase velocity of GW in d_s dimensions
    v_ph ∝ f^((4-d_s)/2) for d_s ≠ 4
    """
    return c * (f / 100)**((4 - d_s) / 2)

def gw_group_velocity(f, d_s, c=1):
    """
    Group velocity of GW in d_s dimensions
    v_gr = v_ph * (d_s/4)
    """
    v_ph = gw_phase_velocity(f, d_s, c)
    return v_ph * (d_s / 4)

# Frequency range (Hz)
f = np.logspace(1, 4, 500)  # 10 Hz to 10 kHz (LIGO band)

# Different spectral dimensions
dims = [
    (4.0, 'black', 'd_s = 4 (GR)'),
    (3.5, 'blue', 'd_s = 3.5'),
    (3.0, 'green', 'd_s = 3.0'),
    (2.5, 'red', 'd_s = 2.5'),
    (2.0, 'purple', 'd_s = 2.0'),
]

fig, axes = plt.subplots(2, 2, figsize=(14, 12))

# Panel 1: Phase velocity
ax1 = axes[0, 0]
for d_s, color, label in dims:
    v_ph = gw_phase_velocity(f, d_s)
    ax1.loglog(f, v_ph, color=color, lw=2, label=label)
ax1.axhline(y=1, color='gray', linestyle='--', alpha=0.5)
ax1.set_xlabel('Frequency f (Hz)', fontsize=12)
ax1.set_ylabel('Phase Velocity v/c', fontsize=12)
ax1.set_title('GW Phase Velocity vs Frequency', fontsize=13)
ax1.legend(fontsize=10)
ax1.grid(True, alpha=0.3)

# Panel 2: Group velocity
ax2 = axes[0, 1]
for d_s, color, label in dims:
    v_gr = gw_group_velocity(f, d_s)
    ax2.loglog(f, v_gr, color=color, lw=2, label=label)
ax2.axhline(y=1, color='gray', linestyle='--', alpha=0.5)
ax2.set_xlabel('Frequency f (Hz)', fontsize=12)
ax2.set_ylabel('Group Velocity v/c', fontsize=12)
ax2.set_title('GW Group Velocity vs Frequency', fontsize=13)
ax2.legend(fontsize=10)
ax2.grid(True, alpha=0.3)

# Panel 3: Time delay
ax3 = axes[1, 0]
distance = 100  # Mpc
for d_s, color, label in dims:
    if d_s != 4.0:
        v_gr = gw_group_velocity(f, d_s)
        delay = distance * (1/v_gr - 1) * 3.086e22 / 2.998e8 / 3600  # hours
        ax3.semilogx(f, delay, color=color, lw=2, label=label)
ax3.set_xlabel('Frequency f (Hz)', fontsize=12)
ax3.set_ylabel('Time Delay (hours)', fontsize=12)
ax3.set_title(f'GW Time Delay (D={distance} Mpc)', fontsize=13)
ax3.legend(fontsize=10)
ax3.grid(True, alpha=0.3)

# Panel 4: Dimension flow prediction
ax4 = axes[1, 1]
# Effective dimension from energy scale
E = np.logspace(0, 20, 500)  # Energy in GeV
d_eff = 4 - 2 / (1 + (1e16/E)**0.5)  # Simple model

ax4.semilogx(E, d_eff, 'b-', lw=3, label='Predicted $d_{eff}$')
ax4.axhline(y=4, color='gray', linestyle='--', alpha=0.5)
ax4.axhline(y=2, color='gray', linestyle='--', alpha=0.5)

# Mark energy scales
scales = [
    (1e-12, 'LIGO\n(100 Hz)', 'green'),
    (1e-4, 'CMB\n(meV)', 'orange'),
    (1e3, 'LHC\n(TeV)', 'red'),
    (1e16, 'Planck', 'purple'),
]

for E_pt, label, color in scales:
    d_pt = 4 - 2 / (1 + (1e16/E_pt)**0.5)
    ax4.plot(E_pt, d_pt, 'o', markersize=15, color=color, 
             markeredgecolor='black', markeredgewidth=1.5)
    ax4.annotate(label, (E_pt, d_pt), xytext=(10, 10), 
                 textcoords='offset points', fontsize=9,
                 bbox=dict(boxstyle='round', facecolor=color, alpha=0.3))

ax4.set_xlabel('Energy E (GeV)', fontsize=12)
ax4.set_ylabel('Effective Dimension $d_{eff}$', fontsize=12)
ax4.set_title('Dimension Flow vs Energy Scale', fontsize=13)
ax4.set_ylim(1.5, 4.5)
ax4.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('../fig7_gravitational_wave.pdf', dpi=600, bbox_inches='tight')
plt.savefig('../fig7_gravitational_wave.png', dpi=600, bbox_inches='tight')
print('Figure 7 saved: gravitational wave effects')
