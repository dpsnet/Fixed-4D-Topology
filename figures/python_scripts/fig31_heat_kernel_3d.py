#!/usr/bin/env python3
"""
Figure 31: 3D Heat Kernel Visualization

Shows the heat kernel evolution in 3D space-time.
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation

fig = plt.figure(figsize=(14, 10))

# Create 3D surface plot of heat kernel
tau_values = [0.01, 0.1, 0.5, 1.0]

for idx, tau in enumerate(tau_values):
    ax = fig.add_subplot(2, 2, idx+1, projection='3d')
    
    # Spatial grid
    x = np.linspace(-5, 5, 50)
    y = np.linspace(-5, 5, 50)
    X, Y = np.meshgrid(x, y)
    
    # Heat kernel: K ~ exp(-r²/(4τ)) / (4πτ)^(d/2)
    r2 = X**2 + Y**2
    d_eff = 4 - 2 * np.exp(-tau)  # Dimension flow
    K = np.exp(-r2/(4*tau)) / (4*np.pi*tau)**(d_eff/2)
    
    surf = ax.plot_surface(X, Y, K, cmap='hot', alpha=0.8, 
                           rstride=1, cstride=1, linewidth=0, antialiased=True)
    ax.set_title(f'$\\tau$ = {tau}', fontsize=12)
    ax.set_zlim(0, 0.5)
    fig.colorbar(surf, ax=ax, shrink=0.5, aspect=10)

plt.suptitle('Heat Kernel Evolution with Dimension Flow', fontsize=16, y=1.02)
plt.tight_layout()
plt.savefig('../fig31_heat_kernel_3d.pdf', dpi=600, bbox_inches='tight')
plt.savefig('../fig31_heat_kernel_3d.png', dpi=600, bbox_inches='tight')
print('Figure 31 saved: 3D heat kernel')
