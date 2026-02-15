#!/usr/bin/env python3
"""
Figure 14: Quantum Information and Dimension Flow

Entropy scaling and entanglement structure in dimension flow.
"""

import numpy as np
import matplotlib.pyplot as plt

def entanglement_entropy(L, d_eff, c=1):
    """
    Entanglement entropy for region of size L
    S ~ c * L^(d_eff-2) for d_eff > 2
    S ~ c * log(L) for d_eff = 2
    """
    if abs(d_eff - 2) < 0.01:
        return c * np.log(L)
    else:
        return c * L**(d_eff - 2)

# System size
L = np.logspace(0, 3, 200)

fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# Left: Entropy vs system size
ax1 = axes[0]
dims = [(4, 'blue', 'd=4 (Area Law)'), 
        (3, 'green', 'd=3'),
        (2.5, 'orange', 'd=2.5'),
        (2, 'red', 'd=2 (Logarithmic)')]

for d_eff, color, label in dims:
    S = entanglement_entropy(L, d_eff)
    if d_eff == 2:
        ax1.loglog(L, S, color=color, lw=2.5, label=label)
    else:
        ax1.loglog(L, S, color=color, lw=2.5, label=label)

ax1.set_xlabel('Region Size $L$', fontsize=13)
ax1.set_ylabel('Entanglement Entropy $S$', fontsize=13)
ax1.set_title('Entanglement Scaling with Dimension', fontsize=14)
ax1.legend(fontsize=10, loc='upper left')
ax1.grid(True, alpha=0.3)

# Right: Entropy derivative (effective dimension)
ax2 = axes[1]

for d_eff, color, label in dims:
    S = entanglement_entropy(L, d_eff)
    dS_dlnL = np.gradient(S, np.log(L))
    ax2.semilogx(L[10:-10], dS_dlnL[10:-10], color=color, lw=2.5, label=label)

ax2.axhline(y=2, color='gray', linestyle='--', alpha=0.5, label='d=2 reference')
ax2.set_xlabel('Region Size $L$', fontsize=13)
ax2.set_ylabel(r'$dS_{eff}/d\ln L$', fontsize=13)
ax2.set_title('Effective Dimension from Entropy', fontsize=14)
ax2.legend(fontsize=10)
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('../fig14_quantum_information.pdf', dpi=600, bbox_inches='tight')
plt.savefig('../fig14_quantum_information.png', dpi=600, bbox_inches='tight')
print('Figure 14 saved: quantum information')
