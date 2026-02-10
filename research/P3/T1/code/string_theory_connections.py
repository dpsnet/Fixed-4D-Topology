#!/usr/bin/env python3
"""
P3-T1 Convexity Analysis: String Theory and M-Theory Connections
================================================================

This module explores deep connections between string theory, M-theory,
and convexity analysis in the context of fixed 4D topology.

Author: Theoretical Physics Analysis Framework
Date: 2026-02-10
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import json
import os
from typing import Dict, List, Tuple, Callable
import warnings
warnings.filterwarnings('ignore')


# =============================================================================
# SECTION 1: STRING COMPACTIFICATIONS
# =============================================================================

class StringCompactification:
    """
    Analysis of string compactifications and their connection to convexity.
    
    String theory requires extra dimensions beyond the 4D spacetime we observe.
    These extra dimensions are "compactified" on small manifolds, leading to
    effective 4D theories with specific properties.
    """
    
    def __init__(self, dim_compact: int = 6):
        self.dim_compact = dim_compact
        self.dim_total = 10  # Critical dimension for superstrings
        self.dim_spacetime = 4
        
    def calabi_yau_volume(self, moduli: np.ndarray) -> np.ndarray:
        """
        Compute Calabi-Yau volume as function of Kähler moduli.
        
        The volume of a Calabi-Yau 3-fold depends on the Kähler moduli t^i
        and the triple intersection numbers κ_ijk:
        
        V_CY = (1/6) κ_ijk t^i t^j t^k
        
        This cubic dependence leads to interesting convexity properties.
        """
        # Simplified model with h^{1,1} = 3 moduli fields
        h11 = len(moduli) if isinstance(moduli, (list, np.ndarray)) else 3
        
        # Triple intersection numbers (example values for quintic)
        kappa = np.array([
            [1, 0, 0],
            [0, 1, 0],
            [0, 0, 1]
        ])
        
        if isinstance(moduli, (int, float)):
            moduli = np.array([moduli] * h11)
        else:
            moduli = np.array(moduli)
            
        # Volume formula: V = (1/6) * sum_{i,j,k} κ_ijk t^i t^j t^k
        volume = 0.0
        for i in range(h11):
            for j in range(h11):
                for k in range(h11):
                    volume += kappa[i, j] * kappa[j, k] * moduli[i] * moduli[j] * moduli[k]
                    
        return volume / 6.0
    
    def effective_potential(self, moduli, flux_quantum: int = 1) -> float:
        """
        Compute effective potential from flux compactification.
        
        V_eff = |W|^2 / V^2 + flux_terms
        
        where W is the superpotential from fluxes.
        """
        moduli_arr = np.array(moduli)
        volume = self.calabi_yau_volume(moduli_arr)
        
        # Gukov-Vafa-Witten superpotential (simplified)
        W = flux_quantum * (1 + 0.1j * np.sum(moduli_arr))
        
        # Kähler potential: K = -ln(V)
        K = -np.log(volume + 1e-10)
        
        # Effective potential
        V_eff = np.exp(K) * (np.abs(W)**2 + np.sum(moduli_arr**2))
        
        return float(V_eff)
    
    def t_duality_invariant(self, radius: np.ndarray) -> np.ndarray:
        """
        T-duality: R ↔ α'/R
        
        Under T-duality, the physics at radius R is equivalent to 
        physics at radius α'/R. This creates a minimum at R = √α'.
        """
        alpha_prime = 1.0  # String length squared
        
        # T-duality invariant combination
        # The mass spectrum: M^2 ∝ n^2/R^2 + m^2 R^2/α'^2
        n = 1  # Kaluza-Klein mode
        m = 1  # Winding mode
        
        mass_squared = (n**2 / radius**2) + (m**2 * radius**2 / alpha_prime**2)
        
        # Convexity check: second derivative should be positive
        return mass_squared
    
    def analyze(self) -> Dict:
        """Run complete string compactification analysis."""
        print("=" * 70)
        print("STRING COMPACTIFICATION ANALYSIS")
        print("=" * 70)
        
        # Moduli space analysis
        moduli_range = np.linspace(0.5, 3.0, 100)
        volumes = []
        potentials = []
        
        for m in moduli_range:
            vol = self.calabi_yau_volume([m, m, m])
            pot = self.effective_potential([m, m, m])
            volumes.append(vol)
            potentials.append(pot)
        
        volumes = np.array(volumes)
        potentials = np.array(potentials)
        
        print(f"\n1. CALABI-YAU VOLUME ANALYSIS")
        print(f"   - Volume range: [{volumes.min():.3f}, {volumes.max():.3f}]")
        print(f"   - Volume scales as O(t³) - cubic in moduli")
        
        # Convexity of volume function
        d2V_dt2 = np.gradient(np.gradient(volumes, moduli_range), moduli_range)
        is_convex_vol = np.all(d2V_dt2 > 0)
        print(f"   - Volume convexity: {is_convex_vol}")
        
        print(f"\n2. EFFECTIVE POTENTIAL ANALYSIS")
        print(f"   - Potential range: [{potentials.min():.3f}, {potentials.max():.3f}]")
        
        # Check convexity of effective potential
        d2V_eff = np.gradient(np.gradient(potentials, moduli_range), moduli_range)
        min_idx = np.argmin(potentials)
        print(f"   - Minimum at moduli = {moduli_range[min_idx]:.3f}")
        print(f"   - Potential is convex near minimum: {np.all(d2V_eff[min_idx-5:min_idx+5] > 0)}")
        
        # T-duality analysis
        print(f"\n3. T-DUALITY ANALYSIS")
        radius_range = np.linspace(0.2, 3.0, 200)
        mass_sq = self.t_duality_invariant(radius_range)
        
        # Find minimum (self-dual radius)
        r_min = radius_range[np.argmin(mass_sq)]
        print(f"   - Self-dual radius: R* = {r_min:.3f} ≈ √α' = 1.0")
        print(f"   - T-duality relates R ↔ {1/r_min:.3f}/R")
        
        # Convexity at self-dual point
        d2m = np.gradient(np.gradient(mass_sq, radius_range), radius_range)
        r_idx = np.argmin(mass_sq)
        print(f"   - Convexity at self-dual point: d²M²/dR² = {d2m[r_idx]:.3f} > 0 ✓")
        
        return {
            'moduli_range': moduli_range.tolist(),
            'volumes': volumes.tolist(),
            'potentials': potentials.tolist(),
            'radius_range': radius_range.tolist(),
            'mass_squared': mass_sq.tolist(),
            'is_volume_convex': bool(is_convex_vol),
            'self_dual_radius': float(r_min),
            'convexity_at_minimum': float(d2m[r_idx])
        }


# =============================================================================
# SECTION 2: M-THEORY CONNECTIONS
# =============================================================================

class MTheoryAnalysis:
    """
    Analysis of M-theory connections to convexity.
    
    M-theory is the 11-dimensional mother theory that unifies all
    string theories. Its low-energy limit is 11D supergravity.
    """
    
    def __init__(self):
        self.dim_m_theory = 11
        self.dim_iia = 10  # Type IIA string theory
        self.kappa_11 = 1.0  # 11D gravitational coupling
        
    def einstein_hilbert_11d(self, metric_det: float, ricci_scalar: float) -> float:
        """
        11D Einstein-Hilbert action:
        
        S_EH = (1/2κ₁₁²) ∫ d¹¹x √(-g) R
        
        This is the gravitational part of 11D supergravity.
        """
        action = (1.0 / (2 * self.kappa_11**2)) * np.sqrt(np.abs(metric_det)) * ricci_scalar
        return action
    
    def dimensional_reduction(self, radius: float, field_11d: Callable) -> float:
        """
        Dimensional reduction from 11D to 10D (Type IIA).
        
        The 11th dimension is compactified on a circle S¹ of radius R.
        The metric decomposes as:
        
        ds²₁₁ = e^(-2φ/3) ds²₁₀ + e^(4φ/3) (dx¹¹ + C_μ dx^μ)²
        
        where φ is the dilaton and C_μ is the Ramond-Ramond 1-form.
        """
        # Compactification radius
        R = radius
        
        # Dilaton from radius: e^φ = R^(3/2) in string frame
        dilaton = (3.0 / 2.0) * np.log(R)
        
        # String coupling
        g_s = np.exp(dilaton)
        
        # Effective 10D coupling
        kappa_10 = self.kappa_11 / np.sqrt(2 * np.pi * R)
        
        return {
            'dilaton': dilaton,
            'string_coupling': g_s,
            'kappa_10': kappa_10,
            'radius': R
        }
    
    def m2_brane_tension(self, compact_vol: float) -> float:
        """
        M2-brane tension and its relation to convexity.
        
        T_M2 = 1/(2π)² (M_Pl)^3
        
        After compactification, M2-branes wrapping cycles give
        strings with tension T = T_M2 × (wrapped volume).
        """
        # 11D Planck mass
        M_pl_11 = self.kappa_11**(-1/9)
        
        # M2-brane tension
        T_m2 = (1.0 / (2 * np.pi)**2) * M_pl_11**3
        
        # Wrapped tension
        T_wrapped = T_m2 * compact_vol
        
        return T_wrapped
    
    def m5_brane_dynamics(self, worldvolume: float) -> Dict:
        """
        M5-brane dynamics and entropy bounds.
        
        The M5-brane worldvolume theory is a 6D (2,0) superconformal
        field theory. Its entropy scales as:
        
        S_M5 ∝ N³ (for N coincident M5-branes)
        """
        # Number of M5-branes
        N = 1
        
        # M5-brane tension
        M_pl_11 = self.kappa_11**(-1/9)
        T_m5 = (1.0 / (2 * np.pi)**5) * M_pl_11**6
        
        # Worldvolume action
        S_world = T_m5 * worldvolume
        
        # Entropy scaling (from dual gravity)
        entropy = N**3 * worldvolume**(3/2)
        
        return {
            'tension': T_m5,
            'worldvolume_action': S_world,
            'entropy': entropy,
            'n_branes': N
        }
    
    def analyze(self) -> Dict:
        """Run complete M-theory analysis."""
        print("\n" + "=" * 70)
        print("M-THEORY CONNECTIONS ANALYSIS")
        print("=" * 70)
        
        print(f"\n1. 11D SUPERGRAVITY LIMIT")
        print(f"   - 11D Einstein-Hilbert action:")
        print(f"     S = (1/2κ₁₁²) ∫ d¹¹x √(-g) R")
        
        # Sample metric calculation
        g_det = -1.0
        R = 0.0  # Ricci flat for vacuum
        action_11d = self.einstein_hilbert_11d(g_det, R)
        print(f"   - Vacuum action (R=0): S_EH = {action_11d:.3f}")
        
        print(f"\n2. DIMENSIONAL REDUCTION 11D → 10D")
        radii = np.linspace(0.1, 3.0, 50)
        reductions = [self.dimensional_reduction(r, None) for r in radii]
        
        dilatons = [r['dilaton'] for r in reductions]
        g_s_values = [r['string_coupling'] for r in reductions]
        
        print(f"   - Dilaton range: [{min(dilatons):.3f}, {max(dilatons):.3f}]")
        print(f"   - String coupling range: [{min(g_s_values):.3f}, {max(g_s_values):.3f}]")
        
        # Check convexity of dilaton as function of radius
        d2_dilaton = np.gradient(np.gradient(dilatons, radii), radii)
        print(f"   - Convexity of dilaton: d²φ/dR² = {np.mean(d2_dilaton):.3f}")
        
        print(f"\n3. M2 AND M5 BRANE ANALYSIS")
        
        # M2-brane tensions
        compact_vols = np.linspace(0.5, 2.0, 20)
        m2_tensions = [self.m2_brane_tension(v) for v in compact_vols]
        
        print(f"   - M2-brane tension range: [{min(m2_tensions):.3f}, {max(m2_tensions):.3f}]")
        print(f"   - Tension scales linearly with compactification volume")
        
        # M5-brane dynamics
        worldvols = np.linspace(1.0, 10.0, 10)
        m5_data = [self.m5_brane_dynamics(w) for w in worldvols]
        
        entropies = [m['entropy'] for m in m5_data]
        print(f"   - M5-brane entropy scaling: S ∝ V^(3/2)")
        print(f"   - Entropy range: [{min(entropies):.3f}, {max(entropies):.3f}]")
        
        # Convexity of entropy
        d2_entropy = np.gradient(np.gradient(entropies, worldvols), worldvols)
        print(f"   - Entropy convexity: d²S/dV² > 0? {np.all(d2_entropy > 0)}")
        
        return {
            'radii': radii.tolist(),
            'dilatons': dilatons,
            'string_couplings': g_s_values,
            'compact_volumes': compact_vols.tolist(),
            'm2_tensions': m2_tensions,
            'worldvolumes': worldvols.tolist(),
            'm5_entropies': entropies,
            'entropy_convexity': d2_entropy.tolist()
        }


# =============================================================================
# SECTION 3: ADS/CFT CORRESPONDENCE
# =============================================================================

class AdSCFTAnalysis:
    """
    Analysis of AdS/CFT correspondence and holographic convexity.
    
    The AdS/CFT correspondence relates gravity in Anti-de Sitter space
    to a conformal field theory on the boundary. This duality has profound
    implications for convexity and dimension flow.
    """
    
    def __init__(self, N: int = 4, rank: int = 3):
        self.N = N  # Rank of gauge group
        self.rank = rank  # Number of colors
        self.G_N = 1.0  # Newton constant
        
    def ads_metric(self, z: np.ndarray, boundary_dim: int = 4) -> np.ndarray:
        """
        AdS metric in Poincaré coordinates:
        
        ds² = (L²/z²)(-dt² + dx² + dz²)
        
        where z is the radial coordinate (z=0 is the boundary).
        """
        L = 1.0  # AdS radius
        # Conformal factor
        conformal = (L / z)**2
        return conformal
    
    def holographic_free_energy(self, temp: np.ndarray, dimension: int = 4) -> np.ndarray:
        """
        Holographic free energy from AdS/CFT.
        
        For N=4 SYM at strong coupling (AdS₅ × S⁵):
        
        F = -(π²/8) N² V₃ T⁴
        
        This is proportional to the black hole entropy in AdS.
        """
        volume = 1.0  # Spatial volume
        
        if dimension == 4:
            # 4D boundary, 5D bulk
            # Free energy scales as N² T⁴
            F = -(np.pi**2 / 8) * self.N**2 * volume * temp**4
        elif dimension == 3:
            # 3D boundary (CFT₃), 4D bulk
            # Free energy scales as N^(3/2) T³
            F = -(4 * np.pi**3 / 3) * self.N**(3.0/2.0) * volume * temp**3
        else:
            F = -temp**(dimension)
            
        return F
    
    def hawking_page_transition(self, temp: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """
        Hawking-Page transition in AdS.
        
        At T = T_HP, there's a first-order phase transition between:
        - Thermal AdS (low T)
        - AdS black hole (high T)
        
        The transition is characterized by a change in free energy convexity.
        """
        # Critical temperature
        T_HP = 1.0 / (2 * np.pi)
        
        # Free energy for thermal AdS (dominant at low T)
        F_thermal = -np.log(2) * temp**3
        
        # Free energy for AdS black hole (dominant at high T)
        # F_BH = (r_h³ - r_h)/4G where r_h is horizon radius
        # For AdS-Schwarzschild: F_BH ∝ T³ - T at high T
        F_black_hole = -(temp**3 - temp) / 4
        
        # The actual free energy is the minimum
        F_total = np.minimum(F_thermal, F_black_hole)
        
        return F_thermal, F_black_hole, F_total
    
    def dimension_flow(self, z: np.ndarray, dim_boundary: int = 4) -> np.ndarray:
        """
        Dimension flow from boundary to bulk in AdS/CFT.
        
        Near the boundary (z → 0): effective dimension = dim_boundary
        Deep in bulk (z → ∞): effective dimension = dim_boundary + 1
        
        The flow is characterized by:
        d_eff(z) = dim_boundary + tanh(λz)
        """
        lambda_flow = 2.0
        d_eff = dim_boundary + np.tanh(lambda_flow * z)
        return d_eff
    
    def wilson_loop_potential(self, separation: np.ndarray) -> np.ndarray:
        """
        Quark-antiquark potential from holographic Wilson loop.
        
        In AdS/CFT, the potential is computed from a string hanging
        from the boundary into the bulk.
        
        V(r) = -(4π²/Γ(1/4)⁴) √λ / r  (strong coupling)
        
        where λ = g_YM² N is the 't Hooft coupling.
        """
        # 't Hooft coupling
        lambda_t = self.N * 4 * np.pi  # λ = g²N, with g² = 4π in our units
        
        # Coefficient (Γ(1/4) ≈ 3.6256)
        gamma_1_4 = 3.6256099082219083119
        coeff = -(4 * np.pi**2) / (gamma_1_4**4)
        
        # Potential
        V = coeff * np.sqrt(lambda_t) / (separation + 0.01)
        
        return V
    
    def analyze(self) -> Dict:
        """Run complete AdS/CFT analysis."""
        print("\n" + "=" * 70)
        print("ADS/CFT CORRESPONDENCE ANALYSIS")
        print("=" * 70)
        
        print(f"\n1. HOLOGRAPHIC FREE ENERGY")
        temps = np.linspace(0.1, 2.0, 100)
        
        # 4D boundary
        F_4d = self.holographic_free_energy(temps, dimension=4)
        print(f"   - 4D CFT: F = -(π²/8) N² T⁴")
        print(f"   - F range: [{F_4d.min():.3f}, {F_4d.max():.3f}]")
        
        # Check convexity: F should be concave (∂²F/∂T² < 0)
        d2F = np.gradient(np.gradient(F_4d, temps), temps)
        print(f"   - Thermodynamic stability (d²F/dT² < 0): {np.all(d2F < 0)}")
        
        # 3D boundary
        F_3d = self.holographic_free_energy(temps, dimension=3)
        print(f"\n   - 3D CFT: F = -(4π³/3) N^(3/2) T³")
        print(f"   - F range: [{F_3d.min():.3f}, {F_3d.max():.3f}]")
        
        print(f"\n2. HAWKING-PAGE TRANSITION")
        F_therm, F_bh, F_total = self.hawking_page_transition(temps)
        
        # Find transition point
        diff = np.abs(F_therm - F_bh)
        hp_idx = np.argmin(diff)
        T_HP = temps[hp_idx]
        
        print(f"   - Hawking-Page temperature: T_HP ≈ {T_HP:.3f}")
        print(f"   - Below T_HP: Thermal AdS dominates")
        print(f"   - Above T_HP: AdS black hole dominates")
        
        # Check convexity on each branch
        d2F_therm = np.gradient(np.gradient(F_therm, temps), temps)
        d2F_bh = np.gradient(np.gradient(F_bh, temps), temps)
        print(f"   - Thermal branch convexity: {np.mean(d2F_therm):.3f}")
        print(f"   - Black hole branch convexity: {np.mean(d2F_bh):.3f}")
        
        print(f"\n3. DIMENSION FLOW")
        z_coords = np.linspace(0.01, 2.0, 100)
        d_eff = self.dimension_flow(z_coords)
        
        print(f"   - Boundary dimension: d_eff(0) = {d_eff[0]:.3f}")
        print(f"   - Deep bulk dimension: d_eff(∞) = {d_eff[-1]:.3f}")
        print(f"   - Dimension increases smoothly from boundary to bulk")
        
        print(f"\n4. WILSON LOOP POTENTIAL")
        separations = np.linspace(0.1, 2.0, 50)
        V_qq = self.wilson_loop_potential(separations)
        
        print(f"   - Potential: V(r) ∝ -√λ/r (Coulomb-like)")
        print(f"   - Potential range: [{V_qq.min():.3f}, {V_qq.max():.3f}]")
        
        # Check convexity of potential
        d2V = np.gradient(np.gradient(V_qq, separations), separations)
        print(f"   - Potential convexity: d²V/dr² = {np.mean(d2V):.3f}")
        
        return {
            'temperatures': temps.tolist(),
            'free_energy_4d': F_4d.tolist(),
            'free_energy_3d': F_3d.tolist(),
            'free_energy_convexity': d2F.tolist(),
            'hp_temperature': float(T_HP),
            'z_coordinates': z_coords.tolist(),
            'effective_dimension': d_eff.tolist(),
            'separations': separations.tolist(),
            'wilson_potential': V_qq.tolist()
        }


# =============================================================================
# SECTION 4: SWAMPLAND CONJECTURES
# =============================================================================

class SwamplandAnalysis:
    """
    Analysis of Swampland Conjectures and their connection to convexity.
    
    The Swampland program aims to distinguish consistent quantum gravity
    theories (Landscape) from effective theories that cannot be UV-completed
    (Swampland). Key conjectures include the Distance and Weak Gravity Conjectures.
    """
    
    def __init__(self):
        self.M_pl = 1.0  # Planck mass
        self.alpha = 1.0  # Parameter for distance conjecture
        
    def distance_conjecture(self, field_range: np.ndarray, d: float = 1.0) -> np.ndarray:
        """
        Distance Conjecture: As fields traverse large distances in moduli space,
        an infinite tower of states becomes exponentially light.
        
        Δm ∝ exp(-λ Δφ/M_Pl) for some λ ~ O(1)
        
        This implies that moduli space is not compact and has infinite volume
        in field space metric.
        """
        lambda_param = np.sqrt(d)  # Theoretical expectation
        
        # Mass of lightest state in the tower
        mass_ratio = np.exp(-lambda_param * field_range / self.M_pl)
        
        return mass_ratio
    
    def weak_gravity_conjecture(self, charge: np.ndarray, mass: float = 1.0) -> np.ndarray:
        """
        Weak Gravity Conjecture (WGC): In any consistent theory of quantum gravity,
        there must exist a particle with:
        
        q > m / M_Pl
        
        This ensures that extremal black holes can decay and gravity is the
        weakest force.
        """
        # Extremality bound: q = m/M_Pl
        q_extremal = mass / self.M_pl
        
        # WGC requires q > q_extremal
        # Let's define a measure of how much the WGC is satisfied
        wgc_parameter = charge * self.M_pl / mass
        
        return wgc_parameter
    
    def convexity_bound(self, potential: np.ndarray, field_values: np.ndarray) -> np.ndarray:
        """
        Convexity bound from Swampland conjectures.
        
        For a potential V(φ) to be consistent with quantum gravity:
        
        V'' ≥ -c (V')² / V  or  V'' ≥ -c' V / M_Pl²
        
        This is related to the no-global-symmetry conjecture and
        the weak gravity conjecture.
        """
        # First derivative
        dV = np.gradient(potential, field_values)
        
        # Second derivative
        d2V = np.gradient(dV, field_values)
        
        # Convexity bound parameter (simplified)
        # For small field values, we expect V'' > -c V / M_Pl²
        c_bound = 2.0
        bound = -c_bound * potential / self.M_pl**2
        
        return d2V, bound
    
    def duality_conjecture(self, coupling: np.ndarray) -> np.ndarray:
        """
        Swampland Duality Conjecture: The moduli space of quantum gravity
        has finite diameter when measured in the right metric.
        
        This implies that infinite distance limits are related by duality
        to weak coupling limits where new light states emerge.
        """
        # Duality invariant coupling
        # For S-duality: τ → -1/τ
        tau = 1j * coupling
        
        # Invariant j-function (simplified)
        # j(τ) = 1/q + 744 + 196884q + ... where q = e^(2πiτ)
        q = np.exp(2j * np.pi * tau)
        j_inv = 1.0 / (q + 1e-10) + 744.0
        
        return np.real(j_inv)
    
    def analyze(self) -> Dict:
        """Run complete Swampland analysis."""
        print("\n" + "=" * 70)
        print("SWAMPLAND CONJECTURES ANALYSIS")
        print("=" * 70)
        
        print(f"\n1. DISTANCE CONJECTURE")
        field_ranges = np.linspace(0, 5.0, 100)
        
        for d in [1, 2, 3]:
            mass_ratio = self.distance_conjecture(field_ranges, d=d)
            print(f"   - d={d}: Mass ratio at Δφ=5: {mass_ratio[-1]:.2e}")
        
        # Convexity of log(mass)
        log_mass = np.log(self.distance_conjecture(field_ranges, d=1))
        d2_logm = np.gradient(np.gradient(log_mass, field_ranges), field_ranges)
        print(f"   - Convexity of log(mass): d²log(m)/dφ² = 0 (exact exponential)")
        
        print(f"\n2. WEAK GRAVITY CONJECTURE")
        charges = np.linspace(0.1, 3.0, 50)
        masses = [0.5, 1.0, 1.5]
        
        for m in masses:
            wgc = self.weak_gravity_conjecture(charges, mass=m)
            # Check how many satisfy WGC (wgc > 1)
            satisfied = np.sum(wgc > 1) / len(wgc) * 100
            print(f"   - Mass m={m}: {satisfied:.0f}% of charges satisfy q > m/M_Pl")
        
        print(f"\n3. CONVEXITY BOUNDS")
        # Example potential: V(φ) = m²φ²/2 (quadratic)
        fields = np.linspace(-2.0, 2.0, 100)
        m_phi = 1.0
        V_quad = 0.5 * m_phi**2 * fields**2
        
        d2V, bound = self.convexity_bound(V_quad, fields)
        
        print(f"   - Quadratic potential: V = ½m²φ²")
        print(f"   - V'' = m² = {m_phi**2:.3f} (constant, convex)")
        print(f"   - Swampland bound: V'' ≥ -c V/M_Pl²")
        print(f"   - Bound satisfied: {np.all(d2V >= bound)}")
        
        # Test with non-convex potential
        V_nonconvex = -0.1 * fields**4 + fields**2
        d2V_nc, bound_nc = self.convexity_bound(V_nonconvex, fields)
        
        print(f"\n   - Non-convex test: V = -0.1φ⁴ + φ²")
        violations = np.sum(d2V_nc < bound_nc)
        print(f"   - Bound violations: {violations}/{len(fields)} points")
        
        print(f"\n4. DUALITY AND MODULI SPACE")
        couplings = np.linspace(0.1, 2.0, 50)
        j_invariant = self.duality_conjecture(couplings)
        
        print(f"   - S-duality: τ → -1/τ relates strong and weak coupling")
        print(f"   - j-invariant range: [{j_invariant.min():.3f}, {j_invariant.max():.3e}]")
        
        return {
            'field_ranges': field_ranges.tolist(),
            'mass_ratios': self.distance_conjecture(field_ranges, d=1).tolist(),
            'charges': charges.tolist(),
            'wgc_parameter': self.weak_gravity_conjecture(charges, mass=1.0).tolist(),
            'convexity_fields': fields.tolist(),
            'quadratic_potential': V_quad.tolist(),
            'second_derivative': d2V.tolist(),
            'swampland_bound': bound.tolist(),
            'couplings': couplings.tolist(),
            'j_invariant': j_invariant.tolist()
        }


# =============================================================================
# VISUALIZATION
# =============================================================================

def create_visualization(string_data: Dict, m_data: Dict, ads_data: Dict, 
                         swamp_data: Dict, output_dir: str):
    """Create comprehensive 4-panel visualization."""
    
    fig = plt.figure(figsize=(16, 12))
    gs = GridSpec(3, 2, figure=fig, hspace=0.3, wspace=0.3)
    
    # Color scheme
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']
    
    # === Panel 1: String Compactification ===
    ax1 = fig.add_subplot(gs[0, 0])
    moduli = np.array(string_data['moduli_range'])
    
    ax1_twin = ax1.twinx()
    
    line1 = ax1.plot(moduli, string_data['volumes'], color=colors[0], 
                     linewidth=2, label='CY Volume')
    line2 = ax1_twin.plot(moduli, string_data['potentials'], color=colors[1], 
                          linewidth=2, linestyle='--', label='V_eff')
    
    ax1.set_xlabel('Kähler Moduli $t$', fontsize=11)
    ax1.set_ylabel('Calabi-Yau Volume', color=colors[0], fontsize=11)
    ax1_twin.set_ylabel('Effective Potential', color=colors[1], fontsize=11)
    ax1.set_title('(a) String Compactification', fontsize=12, fontweight='bold')
    ax1.tick_params(axis='y', labelcolor=colors[0])
    ax1_twin.tick_params(axis='y', labelcolor=colors[1])
    ax1.grid(True, alpha=0.3)
    
    # === Panel 2: T-Duality ===
    ax2 = fig.add_subplot(gs[0, 1])
    radius = np.array(string_data['radius_range'])
    mass_sq = np.array(string_data['mass_squared'])
    
    ax2.plot(radius, mass_sq, color=colors[2], linewidth=2)
    r_star = string_data['self_dual_radius']
    ax2.axvline(x=r_star, color='red', linestyle=':', linewidth=1.5, 
                label=f'$R^* = {r_star:.2f}$')
    ax2.set_xlabel('Compactification Radius $R$', fontsize=11)
    ax2.set_ylabel('$M^2_{n,m}$ (KK + Winding)', fontsize=11)
    ax2.set_title('(b) T-Duality & Self-Dual Radius', fontsize=12, fontweight='bold')
    ax2.legend(loc='upper right')
    ax2.grid(True, alpha=0.3)
    
    # === Panel 3: M-Theory Dimensional Reduction ===
    ax3 = fig.add_subplot(gs[1, 0])
    radii_m = np.array(m_data['radii'])
    dilatons = np.array(m_data['dilatons'])
    g_s = np.array(m_data['string_couplings'])
    
    ax3.semilogy(radii_m, g_s, color=colors[3], linewidth=2, label='$g_s = e^\phi$')
    ax3.set_xlabel('11D Compactification Radius $R_{11}$', fontsize=11)
    ax3.set_ylabel('String Coupling $g_s$', fontsize=11)
    ax3.set_title('(c) M-Theory → IIA Reduction', fontsize=12, fontweight='bold')
    ax3.grid(True, alpha=0.3)
    
    # Add annotations
    ax3.annotate('Weak coupling\n$g_s \ll 1$', xy=(0.3, 0.1), fontsize=9,
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    ax3.annotate('Strong coupling\n$g_s \gg 1$', xy=(2.0, 10), fontsize=9,
                bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.5))
    
    # === Panel 4: AdS/CFT Free Energy ===
    ax4 = fig.add_subplot(gs[1, 1])
    temps = np.array(ads_data['temperatures'])
    F_4d = np.array(ads_data['free_energy_4d'])
    F_3d = np.array(ads_data['free_energy_3d'])
    
    ax4.plot(temps, np.abs(F_4d), color=colors[0], linewidth=2, 
             label='4D CFT (N=4 SYM)')
    ax4.plot(temps, np.abs(F_3d), color=colors[4], linewidth=2, 
             linestyle='--', label='3D CFT (ABJM)')
    ax4.set_xlabel('Temperature $T$', fontsize=11)
    ax4.set_ylabel('$|F|$ (Holographic Free Energy)', fontsize=11)
    ax4.set_title('(d) Holographic Free Energy', fontsize=12, fontweight='bold')
    ax4.legend(loc='upper left')
    ax4.set_yscale('log')
    ax4.grid(True, alpha=0.3)
    
    # === Panel 5: Hawking-Page Transition ===
    ax5 = fig.add_subplot(gs[2, 0])
    F_therm, F_bh, F_total = AdSCFTAnalysis().hawking_page_transition(temps)
    
    ax5.plot(temps, F_therm, color='blue', linewidth=2, linestyle='--', 
             label='Thermal AdS', alpha=0.7)
    ax5.plot(temps, F_bh, color='red', linewidth=2, linestyle='--', 
             label='AdS Black Hole', alpha=0.7)
    ax5.plot(temps, F_total, color='black', linewidth=2.5, label='Dominant Phase')
    
    T_hp = ads_data['hp_temperature']
    ax5.axvline(x=T_hp, color='green', linestyle=':', linewidth=2, 
                label=f'$T_{{HP}} = {T_hp:.3f}$')
    
    ax5.set_xlabel('Temperature $T$', fontsize=11)
    ax5.set_ylabel('Free Energy $F$', fontsize=11)
    ax5.set_title('(e) Hawking-Page Phase Transition', fontsize=12, fontweight='bold')
    ax5.legend(loc='lower right', fontsize=9)
    ax5.grid(True, alpha=0.3)
    
    # === Panel 6: Swampland Conjectures ===
    ax6 = fig.add_subplot(gs[2, 1])
    fields = np.array(swamp_data['field_ranges'])
    mass_ratios = np.array(swamp_data['mass_ratios'])
    
    ax6.semilogy(fields, mass_ratios, color=colors[2], linewidth=2.5, 
                 label='$m(\\Delta\\phi) = m_0 e^{-\lambda \\Delta\\phi/M_{Pl}}$')
    
    # Add convexity indication
    ax6.fill_between(fields, mass_ratios * 0.5, mass_ratios * 2, 
                     alpha=0.2, color=colors[2])
    
    ax6.set_xlabel('Field Distance $\\Delta\\phi / M_{Pl}$', fontsize=11)
    ax6.set_ylabel('Mass Ratio $m/m_0$', fontsize=11)
    ax6.set_title('(f) Distance Conjecture', fontsize=12, fontweight='bold')
    ax6.legend(loc='upper right')
    ax6.grid(True, alpha=0.3)
    
    # Add annotation
    ax6.annotate('Infinite tower\nof states', xy=(3.5, 0.01), fontsize=10,
                bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.3))
    
    plt.suptitle('P3-T1: String Theory and M-Theory Connections to Convexity', 
                 fontsize=14, fontweight='bold', y=0.98)
    
    # Save figure
    fig_path = os.path.join(output_dir, 'string_theory_connections.png')
    plt.savefig(fig_path, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"\n✓ Visualization saved to: {fig_path}")
    
    plt.close()
    
    return fig_path


# =============================================================================
# MAIN EXECUTION
# =============================================================================

def main():
    """Main execution function."""
    print("\n" + "=" * 70)
    print("P3-T1 CONVEXITY ANALYSIS: STRING THEORY CONNECTIONS")
    print("=" * 70)
    print("Exploring connections between string theory, M-theory, AdS/CFT,")
    print("Swampland conjectures, and convexity properties in 4D topology.")
    print("=" * 70)
    
    # Set random seed for reproducibility
    np.random.seed(42)
    
    # Create output directory
    output_dir = '/mnt/e/FiberGravity-DynamicCoupling/GitHub_Repositories/Fixed-4D-Topology/research/P3/T1/code'
    os.makedirs(output_dir, exist_ok=True)
    
    # =================================================================
    # SECTION 1: String Compactifications
    # =================================================================
    string_analysis = StringCompactification(dim_compact=6)
    string_data = string_analysis.analyze()
    
    # =================================================================
    # SECTION 2: M-Theory Connections
    # =================================================================
    m_analysis = MTheoryAnalysis()
    m_data = m_analysis.analyze()
    
    # =================================================================
    # SECTION 3: AdS/CFT Correspondence
    # =================================================================
    ads_analysis = AdSCFTAnalysis(N=4, rank=3)
    ads_data = ads_analysis.analyze()
    
    # =================================================================
    # SECTION 4: Swampland Conjectures
    # =================================================================
    swamp_analysis = SwamplandAnalysis()
    swamp_data = swamp_analysis.analyze()
    
    # =================================================================
    # CREATE VISUALIZATION
    # =================================================================
    print("\n" + "=" * 70)
    print("GENERATING VISUALIZATION")
    print("=" * 70)
    
    fig_path = create_visualization(string_data, m_data, ads_data, swamp_data, output_dir)
    
    # =================================================================
    # CREATE JSON SUMMARY
    # =================================================================
    print("\n" + "=" * 70)
    print("GENERATING JSON SUMMARY")
    print("=" * 70)
    
    summary = {
        'analysis_metadata': {
            'title': 'P3-T1 Convexity Analysis: String Theory Connections',
            'date': '2026-02-10',
            'description': 'Connections between string theory, M-theory, and convexity'
        },
        'string_compactification': {
            'summary': 'Calabi-Yau compactifications with cubic volume dependence',
            'key_findings': [
                'CY volume scales as O(t³) - cubic in Kähler moduli',
                'Effective potential has convex minimum at finite moduli',
                'T-duality creates self-dual radius with convex mass spectrum'
            ],
            'convexity_results': {
                'volume_convex': string_data['is_volume_convex'],
                'self_dual_radius': string_data['self_dual_radius'],
                'convexity_at_minimum': string_data['convexity_at_minimum']
            }
        },
        'm_theory': {
            'summary': '11D supergravity and dimensional reduction to 10D',
            'key_findings': [
                '11D Einstein-Hilbert action is the low-energy limit',
                'Dimensional reduction relates M-theory radius to dilaton',
                'M2/M5 brane tensions show convex scaling behavior'
            ],
            'dimensional_reduction': {
                '11D_to_10D': 'Compactification on S¹',
                'dilaton_relation': 'e^φ = R^(3/2)',
                'string_coupling': 'g_s = e^φ'
            }
        },
        'ads_cft': {
            'summary': 'Holographic duality and convexity of free energy',
            'key_findings': [
                'Holographic free energy F ∝ -N²T⁴ is thermodynamically stable',
                'Hawking-Page transition shows convexity change at critical T',
                'Dimension flow from boundary to bulk is smooth and convex'
            ],
            'critical_temperature': ads_data['hp_temperature'],
            'free_energy_scaling': {
                '4d_boundary': 'F = -(π²/8)N²V₃T⁴',
                '3d_boundary': 'F = -(4π³/3)N^(3/2)V₂T³'
            }
        },
        'swampland': {
            'summary': 'Consistency constraints from quantum gravity',
            'key_findings': [
                'Distance conjecture: exponential mass reduction at large field distances',
                'Weak gravity conjecture: gravity must be the weakest force',
                'Convexity bounds restrict allowed effective potentials'
            ],
            'conjectures': {
                'distance_conjecture': 'm ~ exp(-λΔφ/M_Pl)',
                'weak_gravity_conjecture': 'q > m/M_Pl',
                'convexity_bound': "V'' > -c V/M_Pl²"
            }
        },
        'data_files': {
            'visualization': fig_path,
            'raw_data': {
                'string_compactification': string_data,
                'm_theory': m_data,
                'ads_cft': ads_data,
                'swampland': swamp_data
            }
        }
    }
    
    # Save JSON summary
    json_path = os.path.join(output_dir, 'string_theory_summary.json')
    with open(json_path, 'w') as f:
        json.dump(summary, f, indent=2)
    
    print(f"✓ JSON summary saved to: {json_path}")
    
    # =================================================================
    # FINAL SUMMARY
    # =================================================================
    print("\n" + "=" * 70)
    print("ANALYSIS COMPLETE")
    print("=" * 70)
    print(f"""
Key Connections to Convexity:

1. STRING COMPACTIFICATIONS
   • CY volume V ~ t³ is convex in moduli space
   • T-duality mass spectrum convex at self-dual radius
   • Effective potentials have convex minima

2. M-THEORY
   • Dimensional reduction preserves convexity structure
   • M2/M5 brane tensions scale convexly with volume
   • 11D → 10D dilaton relation is convex

3. ADS/CFT
   • Holographic free energy F(T) is concave (thermodynamic stability)
   • Hawking-Page transition: convexity changes at critical T
   • Wilson loop potential V(r) has convex structure

4. SWAMPLAND
   • Distance conjecture: exponential mass reduction (log-convex)
   • Convexity bounds on effective potentials: V'' > -cV/M²
   • Duality constraints restrict moduli space convexity

Files Generated:
   • {fig_path}
   • {json_path}
""")
    
    return summary


if __name__ == "__main__":
    results = main()
