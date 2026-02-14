#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt
import json

with open('figure6_gw_spectrum.json', 'r') as f:
    data = json.load(f)

freq = np.array(data['frequency'])
Omega_std = np.array(data['Omega_standard'])
Omega_dim = np.array(data['Omega_dimflow'])
Omega_n = np.array(data['Omega_noise'])
Omega_astro = np.array(data['Omega_astro'])

fig, ax = plt.subplots(figsize=(10, 8))

# Plot spectra
ax.loglog(freq, Omega_std, 'b-', linewidth=1.5, 
          label='Standard inflation', alpha=0.7)
ax.loglog(freq, Omega_dim, 'r-', linewidth=2.5, 
          label='Dimension flow (with peak)')
ax.loglog(freq, Omega_n, 'k--', linewidth=1.5, 
          label='LISA noise', alpha=0.6)
ax.loglog(freq, Omega_astro, 'g-', linewidth=1.5, 
          label='Astrophysical BG', alpha=0.6)

# Mark peak
f_peak = data['peak']['f_peak']
ax.axvline(f_peak, color='red', linestyle=':', alpha=0.5)
ax.text(f_peak*2, 5e-15, r'$f_{\rm peak} \approx 0.3$ mHz', 
        fontsize=10, color='red')

# LISA band
ax.axvspan(1e-4, 1, alpha=0.1, color='gray', label='LISA band')

ax.set_xlabel(r'$f$ (Hz)', fontsize=14)
ax.set_ylabel(r'$h^2 \Omega_{\rm GW}(f)$', fontsize=14)
ax.legend(fontsize=10, loc='lower right')
ax.grid(True, alpha=0.3, which='both')
ax.set_xlim([1e-4, 1])
ax.set_ylim([1e-17, 1e-8])
plt.tight_layout()
plt.savefig('figure6_gw_spectrum.pdf', dpi=300)
print("Figure 6 saved")
