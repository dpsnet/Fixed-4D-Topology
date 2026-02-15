#!/usr/bin/env python3
"""
Figure 35: Fourier Analysis of Dimension Flow

Frequency domain representation of dimension flow signals.
"""

import numpy as np
import matplotlib.pyplot as plt
from numpy.fft import fft, fftfreq

# Time domain signal
t = np.linspace(0, 10, 1000)

# Different dimension flow signals
def signal_constant(t):
    """Constant dimension"""
    return 4.0 * np.ones_like(t)

def signal_flow(t, tau=1.0):
    """Dimension flow signal"""
    return 2 + 2 * np.tanh((t - 5) / tau)

def signal_oscillating(t):
    """Oscillating dimension (speculative)"""
    return 3 + np.sin(2*np.pi*t) * np.exp(-t/5)

fig, axes = plt.subplots(2, 2, figsize=(14, 10))

signals = [
    ('Constant', signal_constant, 'blue'),
    ('Flow', signal_flow, 'red'),
    ('Oscillating', signal_oscillating, 'green'),
]

# Time domain plots
for idx, (name, sig_func, color) in enumerate(signals[:2]):
    ax = axes[0, idx]
    s = sig_func(t)
    ax.plot(t, s, color=color, lw=2)
    ax.set_xlabel('Time', fontsize=12)
    ax.set_ylabel('Dimension $d$', fontsize=12)
    ax.set_title(f'{name} (Time Domain)', fontsize=13)
    ax.grid(True, alpha=0.3)
    ax.set_ylim(0, 5)

# Frequency domain
for idx, (name, sig_func, color) in enumerate(signals[1:]):  # Skip constant
    ax = axes[1, idx]
    s = sig_func(t)
    
    # FFT
    dt = t[1] - t[0]
    freqs = fftfreq(len(t), dt)
    spectrum = np.abs(fft(s))
    
    # Plot positive frequencies only
    pos_mask = freqs > 0
    ax.semilogy(freqs[pos_mask], spectrum[pos_mask], color=color, lw=2)
    ax.set_xlabel('Frequency', fontsize=12)
    ax.set_ylabel('Power Spectrum', fontsize=12)
    ax.set_title(f'{name} (Frequency Domain)', fontsize=13)
    ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('../fig35_fourier_transform.pdf', dpi=600, bbox_inches='tight')
plt.savefig('../fig35_fourier_transform.png', dpi=600, bbox_inches='tight')
print('Figure 35 saved: Fourier analysis')
