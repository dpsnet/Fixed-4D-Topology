#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt
import json

with open('figure4_gw150914_posteriors.json', 'r') as f:
    data = json.load(f)

fig, axes = plt.subplots(2, 2, figsize=(12, 10))

# Top-left: Chirp mass
ax = axes[0, 0]
m_std = np.array(data['standard_model']['chirp_mass'])
m_dim = np.array(data['dimflow_model']['chirp_mass'])
ax.hist(m_std, bins=50, alpha=0.5, color='blue', label='Standard (d=4)')
ax.hist(m_dim, bins=50, alpha=0.5, color='red', label='DimFlow')
ax.axvline(28.2, color='blue', linestyle='--')
ax.axvline(26.4, color='red', linestyle='--')
ax.set_xlabel(r'$M_{\rm chirp}$ ($M_\odot$)')
ax.set_ylabel('Probability')
ax.legend()

# Top-right: Luminosity distance
ax = axes[0, 1]
d_std = np.array(data['standard_model']['luminosity_distance'])
d_dim = np.array(data['dimflow_model']['luminosity_distance'])
ax.hist(d_std, bins=50, alpha=0.5, color='blue', label='Standard')
ax.hist(d_dim, bins=50, alpha=0.5, color='red', label='DimFlow')
ax.axvline(438, color='blue', linestyle='--')
ax.axvline(485, color='red', linestyle='--')
ax.set_xlabel(r'$d_L$ (Mpc)')
ax.legend()

# Bottom-left: d_eff
ax = axes[1, 0]
d_eff = np.array(data['dimflow_model']['d_eff'])
ax.hist(d_eff, bins=50, alpha=0.6, color='green')
ax.axvline(3.72, color='darkgreen', linestyle='--', linewidth=2)
ax.axvline(4.0, color='gray', linestyle=':', label='d=4')
ax.set_xlabel(r'$d_{\rm eff}$')
ax.set_ylabel('Probability')
ax.text(0.6, 0.8, f'MAP: $d_{{\rm eff}}$ = 3.72', transform=ax.transAxes)

# Bottom-right: Bayes factor
ax = axes[1, 1]
ax.axis('off')
bf = data['bayes_factor']
ax.text(0.5, 0.7, f'Bayes Factor', ha='center', fontsize=16, weight='bold')
ax.text(0.5, 0.5, f"B = {bf['B']:.1f}", ha='center', fontsize=24)
ax.text(0.5, 0.3, f"[{bf['B_ci_low']:.1f}, {bf['B_ci_high']:.1f}]", 
        ha='center', fontsize=12)
ax.text(0.5, 0.1, 'Moderate Evidence', ha='center', fontsize=14, 
        style='italic', color='green')

plt.tight_layout()
plt.savefig('figure4_gw150914_posteriors.pdf', dpi=300)
print("Figure 4 saved")
