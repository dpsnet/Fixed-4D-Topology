#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt
import json

with open('figure1_three_systems.json', 'r') as f:
    data = json.load(f)

epsilon = np.array(data['epsilon'])
d_eff = np.array(data['d_eff'])

fig, ax = plt.subplots(figsize=(8, 6))
ax.plot(epsilon, d_eff, 'k-', linewidth=2.5, label='Universal law')
ax.set_xlabel('epsilon', fontsize=14)
ax.set_ylabel('d_eff', fontsize=14)
ax.set_xscale('log')
ax.set_xlim([1e-3, 1e2])
ax.set_ylim([1.5, 4.5])
ax.legend()
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('figure1_three_systems.pdf', dpi=300)
print("Figure 1 saved")
