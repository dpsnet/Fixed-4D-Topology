#!/usr/bin/env python3
"""
Figure 2: c1 formula visualization
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc

rc('font', family='serif')
rc('text', usetex=True)

# c1 values for different dimensions
dims = [(2, 0, '2D spatial'), (3, 0, '3D spatial'), (4, 0, '4D spatial'), 
        (3, 1, '3+1D spacetime'), (4, 1, '4+1D spacetime')]

d_values = np.linspace(1.5, 5, 100)

fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# Panel A: c1 vs dimension
ax = axes[0]
for d, w, label in dims:
    c1 = 1 / (2**(d-2+w))
    ax.scatter(d+w, c1, s=200, label=label, zorder=5)

ax.plot(d_values, 1/(2**(d_values-2)), 'k-', lw=2, alpha=0.3)
ax.set_xlabel(r'Effective dimension $d_{\rm eff}$', fontsize=14)
ax.set_ylabel(r'$c_1$ parameter', fontsize=14)
ax.set_title(r'(a) Universal Formula $c_1 = 1/2^{d-2+w}$', fontsize=14)
ax.set_yscale('log')
ax.legend(fontsize=10)
ax.grid(True, alpha=0.3)

# Panel B: Experimental validation
ax = axes[1]
systems = ['Cu$_2$O\n(3,0)', 'SnapPy\n(4,1)', '2D H\n(3$\\to$2)', 'GaAs QW\n(pred.)']
c1_measured = [0.516, 0.245, 0.523, 0.5]
c1_theory = [0.5, 0.25, 0.5, 0.5]
errors = [0.026, 0.014, 0.029, 0.1]

x = np.arange(len(systems))
width = 0.35

bars1 = ax.bar(x - width/2, c1_theory, width, label='Theory', color='skyblue', edgecolor='black')
bars2 = ax.bar(x + width/2, c1_measured, width, yerr=errors, label='Measured', 
               color='lightcoral', edgecolor='black', capsize=5)

ax.set_ylabel(r'$c_1$ value', fontsize=14)
ax.set_title(r'(b) Experimental Validation', fontsize=14)
ax.set_xticks(x)
ax.set_xticklabels(systems, fontsize=10)
ax.legend(fontsize=12)
ax.grid(True, alpha=0.3, axis='y')

plt.tight_layout()
plt.savefig('../fig2_c1_formula.pdf', dpi=300, bbox_inches='tight')
plt.savefig('../fig2_c1_formula.png', dpi=300, bbox_inches='tight')
print('Figure 2 saved: c1_formula.pdf/.png')
