#!/usr/bin/env python3
"""
Figure 15: Cosmological Evolution of Dimensions

Shows how effective dimension evolves with cosmic time.
"""

import numpy as np
import matplotlib.pyplot as plt

# Cosmic time (normalized to present)
t = np.logspace(-6, 0, 500)  # From inflation to present

# Different models for dimension evolution
def dimension_model_1(t):
    """Smooth transition"""
    return 2 + 2 * np.tanh(np.log10(t) + 3)

def dimension_model_2(t):
    """Phase transition"""
    return np.where(t < 1e-4, 2.0, 4.0)

def dimension_model_3(t):
    """Gradual increase"""
    return 2 + 2 / (1 + (t/0.001)**0.5)

fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# Left: Dimension evolution
ax1 = axes[0]
ax1.semilogx(t, dimension_model_1(t), 'b-', lw=2.5, label='Smooth Transition')
ax1.semilogx(t, dimension_model_3(t), 'r--', lw=2.5, label='Gradual Increase')

# Add cosmological epochs
epochs = [
    (1e-6, 'Inflation', 3.0),
    (1e-4, 'Reheating', 2.8),
    (1e-2, 'BBN', 3.5),
    (1, 'Present', 3.95),
]

for t_epoch, name, d_val in epochs:
    ax1.axvline(x=t_epoch, color='gray', linestyle=':', alpha=0.5)
    ax1.annotate(name, (t_epoch, 2.2), rotation=90, fontsize=9, ha='right')

ax1.axhline(y=4, color='gray', linestyle='--', alpha=0.5)
ax1.axhline(y=2, color='gray', linestyle='--', alpha=0.5)
ax1.set_xlabel('Cosmic Time $t/t_0$', fontsize=13)
ax1.set_ylabel('Effective Dimension $d_{eff}$', fontsize=13)
ax1.set_title('Cosmological Dimension Evolution', fontsize=14)
ax1.legend(fontsize=11)
ax1.set_ylim(1.5, 4.5)
ax1.grid(True, alpha=0.3)

# Right: Temperature vs dimension
ax2 = axes[1]

# Temperature evolution (T ~ t^(-1/2) in radiation domination)
T = 1e15 * t**(-0.5)  # GeV

d_eff = dimension_model_1(t)

ax2.semilogx(T, d_eff, 'purple', lw=3)
ax2.axhline(y=4, color='gray', linestyle='--', alpha=0.5)
ax2.axhline(y=2, color='gray', linestyle='--', alpha=0.5)

# Mark energy scales
scales = [
    (1e19, 'Planck', 2.1),
    (1e16, 'GUT', 2.3),
    (1e3, 'EW', 3.2),
    (1e-3, 'CMB', 3.9),
]

for T_pt, name, d_pt in scales:
    ax2.plot(T_pt, d_pt, 'o', markersize=12, color='red')
    ax2.annotate(name, (T_pt, d_pt), xytext=(10, 10), 
                 textcoords='offset points', fontsize=10,
                 bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.5))

ax2.set_xlabel('Temperature $T$ (GeV)', fontsize=13)
ax2.set_ylabel('Effective Dimension $d_{eff}$', fontsize=13)
ax2.set_title('Dimension vs Temperature', fontsize=14)
ax2.set_xlim(1e-4, 1e20)
ax2.set_ylim(1.5, 4.5)
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('../fig15_cosmological_evolution.pdf', dpi=600, bbox_inches='tight')
plt.savefig('../fig15_cosmological_evolution.png', dpi=600, bbox_inches='tight')
print('Figure 15 saved: cosmological evolution')
