#!/usr/bin/env python3
"""
Constrained fit to InAs/GaAs QW binding energy data

Fix B_2D to theoretical value = 4 * Rydberg = 15.2 meV
Fit only L_0 and c1, giving 1 degree of freedom

Model: B(L) = B_2D / (1 + (L_0/L)^(1/c1))^2
"""

import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

# InAs material parameters
rydberg_3D = 3.8  # meV
B_2D_fixed = 4 * rydberg_3D  # 15.2 meV (fixed)

# Experimental data (hh excitons from Brübach 2001)
thickness_ML = np.array([1.0, 1.2, 1.6])
binding_energy_meV = np.array([8.0, 10.0, 12.0])
uncertainty_meV = np.array([1.0, 0.5, 1.0])
thickness_nm = thickness_ML * 0.303

print("=" * 70)
print("InAs/GaAs QW: CONSTRAINED FIT (B_2D fixed at 15.2 meV)")
print("=" * 70)
print(f"\nFixed parameter:")
print(f"  B_2D = {B_2D_fixed:.1f} meV (theoretical 2D limit)")
print(f"\nData points: {len(thickness_ML)}")
print(f"Free parameters: 2 (L_0, c1)")
print(f"Degrees of freedom: {len(thickness_ML) - 2}")


def binding_energy_constrained(L, L_0, c1):
    """Binding energy model with fixed B_2D"""
    return B_2D_fixed / (1 + (L_0 / L)**(1/c1))**2


def fit_constrained():
    """Fit with B_2D fixed"""
    p0 = [0.5, 1.0]  # L_0 ~ 0.5 nm, c1 ~ 1.0
    bounds = ([0.1, 0.1], [2.0, 5.0])
    
    popt, pcov = curve_fit(
        binding_energy_constrained,
        thickness_nm,
        binding_energy_meV,
        p0=p0,
        sigma=uncertainty_meV,
        bounds=bounds,
        absolute_sigma=True
    )
    
    return popt, pcov


def profile_likelihood_c1_fixed(n_points=100):
    """Profile likelihood with B_2D fixed"""
    c1_values = np.linspace(0.1, 3.0, n_points)
    chi2_values = []
    
    for c1 in c1_values:
        # Fix c1 and B_2D, optimize L_0 only
        def model_fixed(L, L_0):
            return B_2D_fixed / (1 + (L_0 / L)**(1/c1))**2
        
        try:
            popt, _ = curve_fit(
                model_fixed,
                thickness_nm,
                binding_energy_meV,
                p0=[0.5],
                sigma=uncertainty_meV,
                bounds=([0.01], [5.0]),
                absolute_sigma=True
            )
            B_pred = model_fixed(thickness_nm, *popt)
            residuals = (binding_energy_meV - B_pred) / uncertainty_meV
            chi2 = np.sum(residuals**2)
            chi2_values.append(chi2)
        except Exception as e:
            chi2_values.append(np.inf)
    
    return c1_values, np.array(chi2_values)


def main():
    # Perform constrained fit
    popt, pcov = fit_constrained()
    L_0_fit, c1_fit = popt
    L_0_err, c1_err = np.sqrt(np.diag(pcov))
    
    # Calculate chi-square
    B_pred = binding_energy_constrained(thickness_nm, *popt)
    residuals = (binding_energy_meV - B_pred) / uncertainty_meV
    chi2 = np.sum(residuals**2)
    dof = len(thickness_nm) - 2
    chi2_red = chi2 / dof if dof > 0 else np.inf
    
    print(f"\n{'='*70}")
    print("FIT RESULTS")
    print(f"{'='*70}")
    print(f"  L_0 = {L_0_fit:.4f} ± {L_0_err:.4f} nm")
    print(f"  c_1 = {c1_fit:.3f} ± {c1_err:.3f}")
    print(f"\nGoodness of fit:")
    print(f"  χ² = {chi2:.3f}")
    print(f"  dof = {dof}")
    print(f"  χ²/dof = {chi2_red:.3f}")
    print(f"  p-value = {1 - chi2/dof if dof > 0 else 'N/A'}")  # Rough estimate
    
    # Compare with theory
    c1_theory = 1.0
    deviation = (c1_fit - c1_theory) / c1_err
    print(f"\nComparison with theory c_1(2,0) = 1.0:")
    print(f"  Measured: {c1_fit:.3f} ± {c1_err:.3f}")
    print(f"  Expected: {c1_theory:.1f}")
    print(f"  Deviation: {deviation:.2f}σ")
    
    # Profile likelihood for confidence interval
    c1_values, chi2_values = profile_likelihood_c1_fixed()
    chi2_min = np.min(chi2_values)
    delta_chi2 = chi2_values - chi2_min
    
    # Find confidence intervals
    within_68 = c1_values[delta_chi2 <= 1.0]
    within_95 = c1_values[delta_chi2 <= 4.0]
    
    if len(within_68) > 0:
        print(f"\nConfidence Intervals (Profile Likelihood):")
        print(f"  68% CL: [{np.min(within_68):.3f}, {np.max(within_68):.3f}]")
    if len(within_95) > 0:
        print(f"  95% CL: [{np.min(within_95):.3f}, {np.max(within_95):.3f}]")
    
    # Model predictions
    print(f"\nPredicted vs Measured:")
    for L_ML, L_nm, B_meas, B_calc in zip(thickness_ML, thickness_nm, binding_energy_meV, B_pred):
        residual = B_meas - B_calc
        print(f"  L = {L_ML} ML ({L_nm:.3f} nm): "
              f"Measured = {B_meas:.1f} ± {uncertainty_meV[list(thickness_ML).index(L_ML)]:.1f}, "
              f"Predicted = {B_calc:.2f}, "
              f"Pull = {residual/uncertainty_meV[list(thickness_ML).index(L_ML)]:.2f}σ")
    
    # Plot
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    # Left: Binding energy fit
    ax1 = axes[0]
    ax1.errorbar(thickness_nm, binding_energy_meV, yerr=uncertainty_meV,
                fmt='o', markersize=12, capsize=5, capthick=2,
                label='Experimental (Brübach 2001)', color='blue', zorder=5)
    
    L_fit = np.linspace(0.2, 1.0, 100)
    B_fit = binding_energy_constrained(L_fit, *popt)
    ax1.plot(L_fit, B_fit, 'r-', linewidth=2, label='Constrained fit', zorder=3)
    
    ax1.axhline(y=B_2D_fixed, color='green', linestyle='--', alpha=0.7,
               label=f'Theoretical 2D limit: {B_2D_fixed:.1f} meV')
    ax1.axhline(y=rydberg_3D, color='gray', linestyle=':', alpha=0.7,
               label=f'3D limit: {rydberg_3D} meV')
    
    ax1.set_xlabel('Well Thickness (nm)', fontsize=12)
    ax1.set_ylabel('Binding Energy (meV)', fontsize=12)
    ax1.set_title('InAs/GaAs QW: Constrained Fit', fontsize=13)
    ax1.legend(loc='lower right', fontsize=9)
    ax1.set_xlim(0.2, 1.0)
    ax1.set_ylim(0, 18)
    ax1.grid(True, alpha=0.3)
    
    textstr = f'Fit Results (B$_{{2D}}$ fixed):\n'
    textstr += f'$L_0$ = {L_0_fit:.3f} ± {L_0_err:.3f} nm\n'
    textstr += f'$c_1$ = {c1_fit:.3f} ± {c1_err:.3f}\n'
    textstr += f'$\\chi^2$/dof = {chi2_red:.2f}'
    ax1.text(0.65, 0.5, textstr, transform=ax1.transAxes, fontsize=10,
            verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
    
    # Right: Profile likelihood
    ax2 = axes[1]
    ax2.plot(c1_values, delta_chi2, 'b-', linewidth=2)
    ax2.axhline(y=1.0, color='red', linestyle='--', alpha=0.7, label='$\\Delta\\chi^2 = 1$ (68% CL)')
    ax2.axhline(y=4.0, color='orange', linestyle='--', alpha=0.7, label='$\\Delta\\chi^2 = 4$ (95% CL)')
    ax2.axvline(x=1.0, color='green', linestyle=':', alpha=0.7, linewidth=2,
               label='Theory: $c_1 = 1.0$')
    ax2.plot(c1_fit, 0, 'bo', markersize=10, zorder=5)
    ax2.axvline(x=c1_fit, color='blue', linestyle='-', alpha=0.3)
    
    # Shade confidence regions
    if len(within_68) > 0:
        ax2.axvspan(np.min(within_68), np.max(within_68), alpha=0.2, color='red')
    
    ax2.set_xlabel('$c_1$ Parameter', fontsize=12)
    ax2.set_ylabel('$\\Delta\\chi^2$', fontsize=12)
    ax2.set_title('Profile Likelihood for $c_1$ (constrained fit)', fontsize=13)
    ax2.legend(loc='upper right', fontsize=9)
    ax2.set_xlim(0.1, 3.0)
    ax2.set_ylim(0, 8)
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('inas_qw_constrained_fit.png', dpi=150, bbox_inches='tight')
    print(f"\nPlot saved to: inas_qw_constrained_fit.png")
    
    # Final conclusion
    print(f"\n{'='*70}")
    print("CONCLUSION")
    print(f"{'='*70}")
    
    if abs(deviation) < 2:
        verdict = "✓ CONSISTENT"
    else:
        verdict = "⚠ MARGINAL"
    
    print(f"{verdict} with c_1(2,0) = 1.0:")
    print(f"  Extracted c_1 = {c1_fit:.3f} ± {c1_err:.3f}")
    print(f"  Expected c_1(2,0) = 1.0")
    print(f"  Deviation: {abs(deviation):.1f}σ")
    
    if len(within_68) > 0 and c1_theory >= np.min(within_68) and c1_theory <= np.max(within_68):
        print(f"  Theory value within 68% confidence interval: ✓")
    elif len(within_95) > 0 and c1_theory >= np.min(within_95) and c1_theory <= np.max(within_95):
        print(f"  Theory value within 95% confidence interval: ✓")
    else:
        print(f"  Theory value outside confidence intervals")
    
    print(f"{'='*70}")
    
    return c1_fit, c1_err


if __name__ == "__main__":
    main()
