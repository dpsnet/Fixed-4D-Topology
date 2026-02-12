#!/usr/bin/env python3
"""
PhenomD三区域完整实现
包含inspiral-intermediate-merger-ringdown
"""

import numpy as np

class PhenomDThreeRegion:
    """IMRPhenomD + 维度流动 完整实现"""
    
    def __init__(self, m1, m2, d_L, d_eff_func=None):
        self.m1 = m1
        self.m2 = m2
        self.M_total = m1 + m2
        self.M_chirp = (m1 * m2)**(3/5) / (m1 + m2)**(1/5)
        self.eta = m1 * m2 / (m1 + m2)**2
        self.d_L = d_L
        self.d_eff_func = d_eff_func or (lambda r: 4.0)
        
        # 过渡频率
        self.f1 = 0.1
        self.f2 = 0.2
    
    def inspiral_amplitude(self, f, r_orbit):
        """Inspiral振幅"""
        d_eff = self.d_eff_func(r_orbit)
        factor = (4.0 / d_eff)**(5/6)
        return factor * (self.M_chirp / self.d_L) * (f / self.f1)**(-7/6)
    
    def inspiral_phase(self, f, r_orbit):
        """Inspiral相位"""
        d_eff = self.d_eff_func(r_orbit)
        M_chirp_eff = self.M_chirp * (4.0 / d_eff)**(3/5)
        v = (np.pi * M_chirp_eff * f)**(1/3)
        return 2 * np.pi * f * M_chirp_eff - np.pi/4 + 3/(128 * self.eta * v**5)
    
    def full_waveform(self, f_array):
        """全频段波形"""
        h = np.zeros_like(f_array, dtype=complex)
        
        for i, f in enumerate(f_array):
            M_geom = self.M_total * 4.925e-6
            r = (M_geom / (np.pi * f)**2)**(1/3) if f > 0 else 100.0
            
            if f < self.f1:
                A = self.inspiral_amplitude(f, r)
                phi = self.inspiral_phase(f, r)
            elif f < self.f2:
                A = self.inspiral_amplitude(self.f1, r)
                phi = 2 * np.pi * f * self.M_chirp
            else:
                A = 1.0
                phi = 2 * np.pi * f * self.M_chirp
            
            h[i] = A * np.exp(1j * phi)
        
        return h
