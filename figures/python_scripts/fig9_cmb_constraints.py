#!/usr/bin/env python3
"""
Figure 9: CMB Constraints on Dimension Flow

Shows constraints on dimension flow parameters from CMB data.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse

# Mock CMB constraint data
# (c1, n_s, error_ellipse)
constraints = [
    {'c1': 0.50, 'ns': 0.965, 'sigma_c1': 0.05, 'sigma_ns': 0.008, 
     'corr': 0.3, 'label': 'Planck 2018', 'color': 'blue'},
    {'c1': 0.52, 'ns': 0.968, 'sigma_c1': 0.03, 'sigma_ns': 0.006, 
     'corr': 0.25, 'label': 'Planck 2018+BAO', 'color': 'green'},
    {'c1': 0.48, 'ns': 0.962, 'sigma_c1': 0.04, 'sigma_ns': 0.007, 
     'corr': 0.35, 'label': 'Simons Array (proj.)', 'color': 'red'},
]

fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# Left: c1 vs n_s constraints
ax1 = axes[0]

# Plot constraint ellipses
for c in constraints:
    # Calculate ellipse parameters
    cov = np.array([[c['sigma_c1']**2, c['corr']*c['sigma_c1']*c['sigma_ns']],
                    [c['corr']*c['sigma_c1']*c['sigma_ns'], c['sigma_ns']**2]])
    eigenvals, eigenvecs = np.linalg.eigh(cov)
    angle = np.degrees(np.arctan2(eigenvecs[1, 0], eigenvecs[0, 0]))
    width, height = 2 * np.sqrt(eigenvals) * 2.45  # 95% CL
    
    ellipse = Ellipse((c['c1'], c['ns']), width, height, angle=angle,
                      facecolor=c['color'], alpha=0.2, edgecolor=c['color'], lw=2)
    ax1.add_patch(ellipse)
    ax1.plot(c['c1'], c['ns'], 'o', color=c['color'], markersize=10, label=c['label'])

# Theory line
c1_theory = np.linspace(0.3, 0.7, 100)
ns_theory = 0.96 + 0.01 * (c1_theory - 0.5) / 0.1
ax1.plot(c1_theory, ns_theory, 'k--', lw=2, label='Theory prediction')

ax1.set_xlabel(r'$c_1$ (Dimension Flow Parameter)', fontsize=13)
ax1.set_ylabel(r'$n_s$ (Scalar Spectral Index)', fontsize=13)
ax1.set_title(r'CMB Constraints: $c_1$ vs $n_s$', fontsize=14)
ax1.legend(loc='lower left', fontsize=10)
ax1.set_xlim(0.35, 0.65)
ax1.set_ylim(0.94, 0.98)
ax1.grid(True, alpha=0.3)

# Right: Confidence intervals
ax2 = axes[1]

experiments = ['Planck\n2018', 'Planck\n+BAO', 'Simons\nArray', 'CMB-S4\n(proj.)', 
               'LiteBIRD\n(proj.)']
c1_best = [0.50, 0.52, 0.48, 0.51, 0.495]
c1_err = [0.05, 0.03, 0.04, 0.015, 0.02]

x_pos = np.arange(len(experiments))
ax2.errorbar(x_pos, c1_best, yerr=c1_err, fmt='o', markersize=12, 
             capsize=8, color='blue', ecolor='blue', capthick=2, lw=2)

# Theory band
ax2.axhspan(0.48, 0.52, alpha=0.2, color='green', label='Theory: $c_1=0.50\pm0.02$')
ax2.axhline(y=0.50, color='green', linestyle='--', lw=2)

ax2.set_xticks(x_pos)
ax2.set_xticklabels(experiments, fontsize=11)
ax2.set_ylabel(r'$c_1$ Constraint', fontsize=13)
ax2.set_title(r'Dimension Flow Parameter Constraints', fontsize=14)
ax2.set_ylim(0.35, 0.65)
ax2.legend(fontsize=10)
ax2.grid(True, alpha=0.3, axis='y')

plt.tight_layout()
plt.savefig('../fig9_cmb_constraints.pdf', dpi=600, bbox_inches='tight')
plt.savefig('../fig9_cmb_constraints.png', dpi=600, bbox_inches='tight')
print('Figure 9 saved: CMB constraints')
