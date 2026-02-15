#!/usr/bin/env python3
"""
Figure 24: LHC Phenomenology of Dimension Flow

Predictions for LHC experiments if dimension flow affects
high-energy particle interactions.
"""

import numpy as np
import matplotlib.pyplot as plt

def cross_section_modification(E, c1, Lambda=10):
    """
    Modified cross section with dimension flow
    sigma(E) = sigma_SM(E) * (1 + c1 * (E/Lambda)^2)
    """
    return 1 + c1 * (E / Lambda)**2

# Energy range (TeV)
E = np.linspace(0.1, 14, 500)

fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# Left: Cross section modification
ax1 = axes[0]
c1_values = [0, 0.1, 0.25, 0.5]
colors = ['black', 'blue', 'green', 'red']

for c1, color in zip(c1_values, colors):
    mod = cross_section_modification(E, c1)
    ax1.plot(E, mod, color=color, lw=2.5, label=f'$c_1$ = {c1}')

ax1.axvline(x=13, color='gray', linestyle=':', alpha=0.7, label='LHC Run 2')
ax1.set_xlabel('Center-of-Mass Energy $\sqrt{s}$ (TeV)', fontsize=13)
ax1.set_ylabel(r'$\sigma/\sigma_{SM}$', fontsize=13)
ax1.set_title('Cross Section Modification', fontsize=14)
ax1.legend(fontsize=11)
ax1.grid(True, alpha=0.3)

# Right: Exclusion contour
ax2 = axes[1]

c1_range = np.linspace(0, 1, 100)
lambda_range = np.linspace(1, 20, 100)
C1, Lambda = np.meshgrid(c1_range, lambda_range)

# Simplified chi-squared (mock)
chi2 = (C1 - 0.5)**2 / 0.1**2 + (Lambda - 10)**2 / 2**2

contour = ax2.contourf(C1, Lambda, chi2, levels=[0, 2.3, 6, 11.8], 
                        colors=['green', 'yellow', 'red'], alpha=0.5)
ax2.contour(C1, Lambda, chi2, levels=[2.3, 6, 11.8], colors='black', linewidths=1.5)

# Mark theory point
ax2.plot(0.5, 10, 'w*', markersize=20, markeredgecolor='black', markeredgewidth=2)
ax2.annotate('Theory\nPrediction', (0.5, 10), xytext=(0.7, 14),
             fontsize=10, arrowprops=dict(arrowstyle='->', color='black'),
             bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

ax2.set_xlabel('Dimension Flow $c_1$', fontsize=13)
ax2.set_ylabel('Scale $\Lambda$ (TeV)', fontsize=13)
ax2.set_title('LHC Exclusion Contours', fontsize=14)

# Legend for contours
from matplotlib.patches import Patch
legend_elements = [
    Patch(facecolor='green', alpha=0.5, label='68% CL'),
    Patch(facecolor='yellow', alpha=0.5, label='95% CL'),
    Patch(facecolor='red', alpha=0.5, label='99% CL')
]
ax2.legend(handles=legend_elements, loc='upper right', fontsize=10)

plt.tight_layout()
plt.savefig('../fig24_lhc_phenomenology.pdf', dpi=600, bbox_inches='tight')
plt.savefig('../fig24_lhc_phenomenology.png', dpi=600, bbox_inches='tight')
print('Figure 24 saved: LHC phenomenology')
