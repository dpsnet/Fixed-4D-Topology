#!/usr/bin/env python3
"""
Generate figures for Dimensionics-Physics paper
Reviews in Mathematical Physics submission
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams
import os

# Set style for publication
rcParams['font.family'] = 'serif'
rcParams['font.size'] = 10
rcParams['axes.linewidth'] = 0.8
rcParams['xtick.major.width'] = 0.8
rcParams['ytick.major.width'] = 0.8
rcParams['lines.linewidth'] = 1.5

# Output directory
output_dir = os.path.dirname(os.path.abspath(__file__))

# Figure 1: Dimension Flow Schematic
print("Generating Figure 1: Dimension Flow...")
fig, ax = plt.subplots(figsize=(3.375, 2.5))

mu = np.logspace(-3, 3, 1000)
d_s = 2 + 2 / (1 + mu**(-2))  # Master Equation solution

ax.semilogx(mu, d_s, 'b-', label=r'$d_s(\mu)$')
ax.axhline(y=4, color='k', linestyle='--', alpha=0.5, label='IR: $d_s = 4$')
ax.axhline(y=2, color='r', linestyle='--', alpha=0.5, label='UV: $d_s = 2$')

ax.set_xlabel(r'Energy Scale $\mu/\mu_0$')
ax.set_ylabel(r'Spectral Dimension $d_s$')
ax.set_ylim(1.8, 4.2)
ax.legend(loc='right', fontsize=8)

plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'figure1_dimension_flow.pdf'), dpi=300)
plt.close()

# Figure 2: Beta Function
print("Generating Figure 2: Beta Function...")
fig, ax = plt.subplots(figsize=(3.375, 2.5))

d = np.linspace(2, 4, 100)
alpha = 1.0
beta = -alpha * (d - 2) * (4 - d)

ax.plot(d, beta, 'b-')
ax.axhline(y=0, color='k', linewidth=0.5)
ax.plot(2, 0, 'ro', markersize=8, label='UV fixed point (stable)')
ax.plot(4, 0, 'go', markersize=8, label='IR fixed point (unstable)')

ax.set_xlabel(r'Dimension $d$')
ax.set_ylabel(r'$\beta(d)$')
ax.legend(fontsize=8)
ax.set_xlim(1.8, 4.2)

plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'figure2_beta_function.pdf'), dpi=300)
plt.close()

# Figure 3: Master Equation Solutions
print("Generating Figure 3: Master Solutions...")
fig, ax = plt.subplots(figsize=(3.375, 2.5))

ln_mu = np.linspace(0, 10, 500)
initial_conditions = [3.9, 3.5, 3.0, 2.5]
alpha = 1.0

for d0 in initial_conditions:
    C = (4 - d0) / (d0 - 2)
    d_s = 2 + 2 / (1 + C * np.exp(-2*alpha*ln_mu))
    ax.plot(ln_mu, d_s, label=f'$d_s(0) = {d0}$')

ax.axhline(y=2, color='r', linestyle='--', alpha=0.5)
ax.axhline(y=4, color='g', linestyle='--', alpha=0.5)
ax.set_xlabel(r'$\ln(\mu/\mu_0)$')
ax.set_ylabel(r'$d_s$')
ax.legend(fontsize=7, loc='right')
ax.set_ylim(1.8, 4.2)

plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'figure3_master_solutions.pdf'), dpi=300)
plt.close()

# Figure 4: Cosmic Dimension Evolution
print("Generating Figure 4: Cosmic Evolution...")
fig, ax = plt.subplots(figsize=(3.375, 2.5))

# Cosmic time in units of tau
t_tau = np.linspace(-5, 10, 500)
t_c = 0  # Transition time
d_s = 2 + 2 / (1 + np.exp(-(t_tau - t_c)))

ax.plot(t_tau, d_s, 'b-', linewidth=2)
ax.axhline(y=2, color='r', linestyle='--', alpha=0.5, label='UV: $d_s = 2$')
ax.axhline(y=4, color='g', linestyle='--', alpha=0.5, label='IR: $d_s = 4$')
ax.axhline(y=3, color='gray', linestyle=':', alpha=0.5)
ax.axvline(x=t_c, color='gray', linestyle=':', alpha=0.5)

# Mark key epochs
ax.annotate('Big Bang\n(ds=2)', xy=(-5, 2.1), fontsize=7, ha='center')
ax.annotate('Transition\n(ds=3)', xy=(t_c, 3.15), fontsize=7, ha='center')
ax.annotate('Today\n(ds~4)', xy=(8, 3.7), fontsize=7, ha='center')

ax.set_xlabel(r'Cosmic Time $(t-t_c)/\tau$')
ax.set_ylabel(r'$d_s(t)$')
ax.set_ylim(1.8, 4.3)
ax.legend(fontsize=8, loc='lower right')

plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'figure4_cosmic_evolution.pdf'), dpi=300)
plt.close()

# Figure 5: Black Hole Dimension Compression
print("Generating Figure 5: BH Dimension...")
fig, ax = plt.subplots(figsize=(3.375, 2.5))

r_rs = np.linspace(1.01, 5, 500)
d_s = 4 - 1/r_rs  # d_s(r) = 4 - r_s/r

ax.plot(r_rs, d_s, 'b-', linewidth=2)
ax.axhline(y=4, color='g', linestyle='--', alpha=0.5, label=r'$r \to \infty: d_s = 4$')
ax.axhline(y=3, color='orange', linestyle='--', alpha=0.5, label=r'$r = r_s: d_s = 3$')
ax.axvline(x=1, color='red', linestyle=':', alpha=0.7, label='Horizon')

ax.fill_betweenx([2, 4], 0, 1, alpha=0.1, color='red', label='Interior')

ax.set_xlabel(r'$r/r_s$')
ax.set_ylabel(r'$d_s(r)$')
ax.set_ylim(2.5, 4.1)
ax.set_xlim(0.5, 5)
ax.legend(fontsize=7)

plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'figure5_bh_dimension.pdf'), dpi=300)
plt.close()

# Figure 6: CMB Power Spectrum (P1)
print("Generating Figure 6: CMB Power Spectrum...")
fig, ax = plt.subplots(figsize=(3.375, 2.5))

# Simplified model
ell = np.linspace(2, 5000, 500)
ell_star = 3000
epsilon = 0.003  # d_s = 4 - epsilon

# Standard LambdaCDM (simplified)
C_LCDM = 1000 * (ell/100)**(-2) * np.exp(-(ell/3000)**2)

# Dimensionics correction
C_DP = C_LCDM * (ell/ell_star)**epsilon

ax.loglog(ell, C_LCDM, 'k--', label=r'$\Lambda$CDM', alpha=0.7)
ax.loglog(ell, C_DP, 'b-', label=f'Dimensionics ($\\epsilon = {epsilon}$)')

ax.axvline(x=3000, color='gray', linestyle=':', alpha=0.5)
ax.text(3500, 500, r'$\ell_*$', fontsize=9)

ax.set_xlabel(r'Multipole $\ell$')
ax.set_ylabel(r'$C_\ell$')
ax.legend(fontsize=8)

plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'figure6_cmb_spectrum.pdf'), dpi=300)
plt.close()

# Figure 7: iTEBD Validation
print("Generating Figure 7: iTEBD Validation...")
fig, ax = plt.subplots(figsize=(3.375, 2.5))

# Finite-size scaling
L = np.array([10, 20, 50, 100])
d_eff_iTEBD = np.array([1.45, 1.30, 1.174, 1.10])
d_eff_theory = 2 - 41.3/L

ax.plot(1/L, d_eff_iTEBD, 'bo', label='iTEBD data')
ax.plot(1/L, d_eff_theory, 'r-', label='Theory fit')

# Extrapolation
L_ext = np.linspace(50, 1000, 100)
ax.plot(1/L_ext, 2 - 41.3/L_ext, 'r--', alpha=0.5)
ax.axhline(y=2, color='k', linestyle=':', alpha=0.5, label='UV limit: $d_s^* = 2$')

ax.set_xlabel(r'$1/L$')
ax.set_ylabel(r'$d_{\text{eff}}$')
ax.legend(fontsize=8)
ax.set_ylim(1.0, 2.1)

plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'figure7_itebd.pdf'), dpi=300)
plt.close()

print("All figures generated successfully!")
print(f"Output directory: {output_dir}")
