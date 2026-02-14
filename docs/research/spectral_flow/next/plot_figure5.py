#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt
import json

with open('figure5_flrw_evolution.json', 'r') as f:
    data = json.load(f)

t = np.array(data['time'])
d = np.array(data['dimension'])

fig, ax = plt.subplots(figsize=(10, 7))

# Main curve
ax.plot(t, d, 'b-', linewidth=2.5, label=r'$d_{\rm eff}(t)$')

# Asymptotes
ax.axhline(2, color='gray', linestyle='--', alpha=0.5)
ax.axhline(4, color='gray', linestyle='--', alpha=0.5)
ax.text(1e-40, 2.1, r'$d=2$', fontsize=10, color='gray')
ax.text(1e-40, 3.8, r'$d=4$', fontsize=10, color='gray')

# Key epochs
epochs = data['key_epochs']
colors_ep = {'Planck': 'purple', 'GUT_start': 'red', 
             'GUT_end': 'orange', 'Electroweak': 'green', 'BBN': 'blue'}

for name, info in epochs.items():
    if name in colors_ep:
        ax.axvline(info['t'], color=colors_ep[name], linestyle=':', alpha=0.6)
        ax.text(info['t'], 2.5, name, rotation=90, fontsize=8, 
                color=colors_ep[name], ha='right')

# GUT transition shading
ax.axvspan(1e-36, 1e-32, alpha=0.2, color='yellow', label='GUT transition')

ax.set_xlabel(r'$t$ (s)', fontsize=14)
ax.set_ylabel(r'$d_{\rm eff}$', fontsize=14)
ax.set_xscale('log')
ax.set_xlim([t.min(), 1e3])
ax.set_ylim([1.5, 4.5])
ax.legend(fontsize=10)
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('figure5_flrw_evolution.pdf', dpi=300)
print("Figure 5 saved")
