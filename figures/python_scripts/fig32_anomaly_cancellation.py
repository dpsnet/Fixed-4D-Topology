#!/usr/bin/env python3
"""
Figure 32: Anomaly Cancellation in Dimension Flow

Shows how quantum anomalies are affected by dimension flow.
"""

import numpy as np
import matplotlib.pyplot as plt

# Energy scale
E = np.logspace(0, 16, 500)

# Effective dimension
M_planck = 1e19  # GeV
d_eff = 2 + 2 / (1 + (E/M_planck)**0.5)

# Anomaly coefficients (simplified)
def anomaly_coeff(d):
    """Chiral anomaly coefficient"""
    return d - 2  # Simplified

def trace_anomaly(d):
    """Trace anomaly coefficient"""
    return (d - 2) * (d - 4) / 12  # Simplified

fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# Left: Anomaly vs energy
ax1 = axes[0]
c_chiral = [anomaly_coeff(d) for d in d_eff]
c_trace = [trace_anomaly(d) for d in d_eff]

ax1.semilogx(E, c_chiral, 'b-', lw=2.5, label='Chiral Anomaly')
ax1.semilogx(E, c_trace, 'r--', lw=2.5, label='Trace Anomaly')

ax1.axvline(x=M_planck, color='gray', linestyle=':', alpha=0.7, label='Planck Scale')
ax1.set_xlabel('Energy $E$ (GeV)', fontsize=13)
ax1.set_ylabel('Anomaly Coefficient', fontsize=13)
ax1.set_title('Quantum Anomalies with Dimension Flow', fontsize=14)
ax1.legend(fontsize=11)
ax1.grid(True, alpha=0.3)

# Right: Anomaly cancellation condition
ax2 = axes[1]

# Simplified model: different species contributions
species = np.arange(1, 11)
dimensions = [2, 2.5, 3, 3.5, 4]
colors = plt.cm.viridis(np.linspace(0, 1, len(dimensions)))

for d, color in zip(dimensions, colors):
    contribution = species * (d - 2) / 2
    ax2.plot(species, contribution, 'o-', color=color, lw=2, 
             label=f'd = {d}', markersize=8)

ax2.axhline(y=0, color='black', linestyle='--', alpha=0.5, label='Cancellation')
ax2.set_xlabel('Species Index', fontsize=13)
ax2.set_ylabel('Anomaly Contribution', fontsize=13)
ax2.set_title('Anomaly Cancellation by Species', fontsize=14)
ax2.legend(fontsize=10)
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('../fig32_anomaly_cancellation.pdf', dpi=600, bbox_inches='tight')
plt.savefig('../fig32_anomaly_cancellation.png', dpi=600, bbox_inches='tight')
print('Figure 32 saved: anomaly cancellation')
