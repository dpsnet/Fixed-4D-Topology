#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt
import json
from scipy import stats

with open('figure2_c1_distribution.json', 'r') as f:
    data = json.load(f)

fig, ax = plt.subplots(figsize=(10, 8))

colors = {'geometric': 'blue', 'linear': 'green', 'power': 'red'}
alphas = {'geometric': 0.6, 'linear': 0.5, 'power': 0.4}

for method, info in data['methods'].items():
    values = np.array(info['values'])
    ax.hist(values, bins=50, density=True, alpha=alphas[method], 
            color=colors[method], label=f"{method}: $c_1$={info['mean']:.3f}")
    
    # KDE
    kde = stats.gaussian_kde(values)
    x_range = np.linspace(values.min(), values.max(), 100)
    ax.plot(x_range, kde(x_range), color=colors[method], linewidth=2)

# Theoretical value
ax.axvline(0.25, color='black', linestyle='--', linewidth=2, 
           label=r'Theory: $c_1 = 1/4$')

ax.set_xlabel(r'$c_1$ coefficient', fontsize=14)
ax.set_ylabel('Probability density', fontsize=14)
ax.legend(fontsize=10)
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('figure2_c1_distribution.pdf', dpi=300)
print("Figure 2 saved")
