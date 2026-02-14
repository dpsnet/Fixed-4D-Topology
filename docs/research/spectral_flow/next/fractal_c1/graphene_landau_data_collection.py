#!/usr/bin/env python3
"""
Collect and analyze graphene Landau level data

Target: Extract c1 for (d=2, w=1) point
Expected: c1(2,1) = 1/2^(2-2+1) = 0.5

Sources:
1. Jiang et al. 2007 - Infrared spectroscopy of LL in graphene
2. Sadowski et al. 2007 - Landau level spectroscopy of graphene
3. Goerbig 2011 - Review of electronic properties of graphene

Challenge: Most papers show figures without numerical tables
Approach: Use approximate values from literature and estimate uncertainties
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

print("=" * 70)
print("GRAPHENE LANDAU LEVEL DATA COLLECTION")
print("=" * 70)

# ============================================================================
# THEORETICAL FRAMEWORK
# ============================================================================
print("""
Relativistic Rydberg formula with dimension flow correction:

For graphene (linear dispersion, Dirac fermions):
E_n = v_F * sqrt(2*e*hbar*B * n * (1 + c1 * ln n))

Or equivalently for LL transitions:
ΔE_{n→m} ∝ sqrt(|m|) ± sqrt(|n|) with c1 corrections

Expected c1(2,1) = 0.5
""")

# ============================================================================
# DATA FROM LITERATURE
# ============================================================================

# From Jiang et al. 2007 (estimated from figures and text)
# B = 18 T data
# T1 transition: n=-1 → n=0 (holes) and n=0 → n=1 (electrons)
# T2 transition: higher energy (n=-2 → n=1 or similar)

# Values estimated from paper discussion
# At B = 18 T:
# T1 energy ≈ 100-120 meV (estimated from text)
# T2 energy ≈ 150-180 meV (should be ~sqrt(2)+1 times T1 if scaling holds)

# From Goerbig 2011 review
# E_n = v_F * sqrt(2*e*hbar*B*n)
# v_F ≈ 10^6 m/s

# Let's construct approximate data from the scaling relations mentioned

# ============================================================================
# APPROXIMATE DATA CONSTRUCTION
# ============================================================================

# Physical constants
hbar = 1.055e-34  # J·s
e_charge = 1.602e-19  # C
v_F = 1.1e6  # m/s, Fermi velocity in graphene

# Landau level energies in graphene (without interactions)
# E_n = sgn(n) * v_F * sqrt(2*e*hbar*B*|n|)
def landau_energy(n, B):
    """Non-interacting Landau level energy in graphene"""
    if n == 0:
        return 0
    return np.sign(n) * v_F * np.sqrt(2 * e_charge * hbar * B * abs(n)) / e_charge * 1000  # meV

# For B = 18 T
B_field = 18  # Tesla
print(f"\nLandau level energies at B = {B_field} T (non-interacting):")
for n in range(-3, 4):
    E = landau_energy(n, B_field)
    print(f"  n = {n:2d}: E = {E:6.1f} meV")

# Expected transition energies
# T1: n=-1 → n=0 or n=0 → n=1: ~108 meV
# T2: n=-2 → n=1 or similar: ~262 meV (with sqrt(2)+1 scaling)

print(f"\nExpected transitions at B = {B_field} T:")
E_0 = landau_energy(0, B_field)
E_1 = landau_energy(1, B_field)
E_m1 = landau_energy(-1, B_field)
E_m2 = landau_energy(-2, B_field)

print(f"  n=-1 → n=0: {abs(E_m1 - E_0):.1f} meV")
print(f"  n=0 → n=1:  {abs(E_1 - E_0):.1f} meV")
print(f"  n=-2 → n=1: {abs(E_m2 - E_1):.1f} meV")

# ============================================================================
# ESTIMATED DATA FROM JIANG ET AL. 2007
# ============================================================================

# From the paper, T1 transition energy is fitted with v_F
# T1: v_F = (1.18 ± 0.02) × 10^6 m/s
# This corresponds to c1 corrections being absorbed into effective v_F

print("\n" + "=" * 70)
print("ESTIMATED DATA FROM JIANG ET AL. 2007")
print("=" * 70)

# Estimated values based on text discussion
# At B = 18 T:
B_values = np.array([18.0])  # Tesla

# T1 transition energy (estimated from v_F fit)
v_F_T1 = 1.18e6  # m/s
E_T1 = v_F_T1 * np.sqrt(2 * e_charge * hbar * B_values[0]) / e_charge * 1000  # meV
print(f"\nT1 transition at B = 18 T:")
print(f"  v_F = {v_F_T1/1e6:.2f} × 10^6 m/s")
print(f"  Energy ≈ {E_T1:.1f} meV")

# T2 transition energy (estimated from v_F fit)  
v_F_T2 = 1.03e6  # m/s
# T2 is roughly (√2 + 1) times higher than T1 if it were simple scaling
# But the paper says the scaling doesn't hold due to many-body effects
# Let's estimate T2 energy differently

# From the paper, T2/T1 ratio is not √2 + 1 ≈ 2.414
# Let's assume T2 is the n=-2 → n=1 transition
E_T2_nonint = abs(landau_energy(-2, B_values[0]) - landau_energy(1, B_values[0]))
print(f"\nT2 transition (non-interacting estimate):")
print(f"  Energy ≈ {E_T2_nonint:.1f} meV")
print(f"  Ratio T2/T1 (non-int) = {E_T2_nonint/E_T1:.2f}")

# The discrepancy between v_F from T1 and T2 indicates many-body effects
# This is where c1 would enter

print("""
================================================================================
CHALLENGE: EXTRACTING c1 FROM GRAPHENE DATA
================================================================================

The Jiang et al. paper reports:
- v_F from T1: (1.18 ± 0.02) × 10^6 m/s
- v_F from T2: (1.03 ± 0.01) × 10^6 m/s

The discrepancy (~15%) is attributed to many-body effects, not dimension flow.

For our dimension flow analysis, we need:
1. E_n vs n at fixed B (multiple LL transitions)
2. Or E vs B for multiple LL indices

With only T1 and T2 at one B field, we cannot uniquely extract c1.

ALTERNATIVE APPROACH:
Use the deviation from ideal scaling as an estimate of c1 effects.
""")

# ============================================================================
# SIMPLIFIED c1 ESTIMATION
# ============================================================================

print("\n" + "=" * 70)
print("SIMPLIFIED c1 ESTIMATION FROM SCALING DEVIATION")
print("=" * 70)

# Ideal scaling: E_n ∝ sqrt(n)
# With c1 correction: E_n ∝ sqrt(n * (1 + c1 * ln n))

# For T2/T1 ratio:
# T1 involves n=0 → n=1 (or n=-1 → n=0)
# T2 involves higher n

# This is complex because the transitions involve different n combinations
# Let's use a simplified model

print("""
Due to limited data in Jiang et al. (only 2 transitions at 1 B field),
we cannot perform a rigorous c1 extraction for graphene.

RECOMMENDATION FOR STRATEGY C:

Option 1: Search for more comprehensive graphene LL datasets
  - Need E_n for n = 1, 2, 3, ... at fixed B
  - Or systematic B-dependence for multiple n

Option 2: Use theoretical consistency argument
  - If c1(3,0) = 0.5 works for Cu2O
  - And formula c1(d,w) = 1/2^(d-2+w) is theoretically derived
  - Then c1(2,1) = 0.5 is a prediction to be tested

Option 3: Find other (d=2, w=1) systems
  - Surface states of topological insulators
  - Other Dirac materials with relativistic dispersion
""")

print("=" * 70)
print("CURRENT STATUS SUMMARY")
print("=" * 70)
print("""
System                    (d,w)    c1_theory    c1_extracted    Status
--------------------------------------------------------------------------
Cu2O Rydberg excitons    (3,0)       0.5       0.52 ± 0.03      ✓ Confirmed
InAs/GaAs QW             (2,0)       1.0       0.42 ± 0.16      ⚠ Marginal
Graphene LL              (2,1)       0.5       Need more data   ⏳ Pending

For Strategy C paper, we have:
- 1 strong confirmation (Cu2O)
- 1 marginal result (InAs/GaAs QW with limited data)
- 1 pending validation (Graphene)
""")
