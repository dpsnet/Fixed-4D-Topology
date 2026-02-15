#!/usr/bin/env python3
"""
Figure 1: Heat kernel and spectral dimension
for unified dimension flow review paper.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc

# LaTeX style
rc('font', family='serif')
rc('text', usetex=True)

# Parameters
tau = np.logspace(-2, 2, 500)
d = 4  # topological dimension

# Heat kernel for smooth manifold
K_smooth = (4 * np.pi * tau)**(-d/2)

# Heat kernel with dimension flow (model)
c1 = 0.5
tau0 = 1.0
d_eff = 2 + 2 / (1 + (tau/tau0)**(1/c1))
K_flow = (4 * np.pi * tau)**(-d_eff/2)

fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# Panel A: Heat kernel
ax = axes[0]
ax.loglog(tau, K_smooth, 'k--', lw=2, label='Smooth $d=4$')
ax.loglog(tau, K_flow, 'b-', lw=2, label='Dimension flow')
ax.set_xlabel(r'Diffusion time $\tau$', fontsize=14)
ax.set_ylabel(r'Heat kernel $K(\tau)$', fontsize=14)
ax.set_title(r'(a) Return Probability', fontsize=14)
ax.legend(fontsize=12)
ax.grid(True, alpha=0.3)

# Panel B: Spectral dimension
ax = axes[1]
d_s_smooth = np.full_like(tau, d)
d_s_flow = 2 + 2 / (1 + (tau/tau0)**(1/c1))
ax.semilogx(tau, d_s_smooth, 'k--', lw=2, label='Smooth $d=4$')
ax.semilogx(tau, d_s_flow, 'b-', lw=2, label='Dimension flow')
ax.axhline(y=2, color='r', linestyle=':', alpha=0.5, label='UV limit $d_s=2$')
ax.set_xlabel(r'Diffusion time $\tau$', fontsize=14)
ax.set_ylabel(r'Spectral dimension $d_s(\tau)$', fontsize=14)
ax.set_title(r'(b) Spectral Dimension Flow', fontsize=14)
ax.set_ylim([1.5, 4.5])
ax.legend(fontsize=12)
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('../fig1_heat_kernel.pdf', dpi=300, bbox_inches='tight')
plt.savefig('../fig1_heat_kernel.png', dpi=300, bbox_inches='tight')
print('Figure 1 saved: heat_kernel.pdf/.png')
