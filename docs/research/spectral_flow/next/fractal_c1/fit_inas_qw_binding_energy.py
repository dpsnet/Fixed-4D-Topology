#!/usr/bin/env python3
"""
Fit InAs/GaAs QW binding energy data to extract c1 parameter

Uses dimension flow model:
B(L) = B_2D / (1 + (L_0/L)^(1/c1))^2

Where:
- B(L) = binding energy at well thickness L
- B_2D = ideal 2D binding energy = 4 * Rydberg
- L_0 = characteristic crossover thickness
- c1 = dimension flow parameter

For (d=2, w=0), theoretical prediction: c1 = 1.0
"""

import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

# InAs material parameters (from Brübach 2001 thesis)
rydberg_3D = 3.8  # meV, bulk Rydberg energy
epsilon = 12.5  # dielectric constant (GaAs matrix)
bohr_radius_3D = 90  # Å, bulk Bohr radius

# Ideal 2D binding energy (infinite barrier limit)
B_2D_ideal = 4 * rydberg_3D  # 15.2 meV

# Experimental data from Brübach thesis (hh excitons)
# Thickness in monolayers (ML), 1 ML ≈ 3.03 Å for InAs
# Binding energies in meV
thickness_ML = np.array([1.0, 1.2, 1.6])  # ML
binding_energy_meV = np.array([8.0, 10.0, 12.0])  # meV
uncertainty_meV = np.array([1.0, 0.5, 1.0])  # estimated uncertainties

# Convert ML to nm (1 ML InAs ≈ 0.303 nm)
thickness_nm = thickness_ML * 0.303

print("=" * 70)
print("InAs/GaAs QW Binding Energy Analysis")
print("=" * 70)
print(f"\n3D Rydberg energy: {rydberg_3D} meV")
print(f"Ideal 2D binding energy: {B_2D_ideal} meV")
print(f"\nData points:")
for i, (L, B) in enumerate(zip(thickness_ML, binding_energy_meV)):
    print(f"  L = {L} ML ({L*0.303:.3f} nm): B = {B} meV")


def binding_energy_model(L, B_2D, L_0, c1):
    """
    Dimension flow model for binding energy vs thickness
    
    B(L) = B_2D / (1 + (L_0/L)^(1/c1))^2
    
    Parameters:
    -----------
    L : thickness (nm)
    B_2D : ideal 2D binding energy (meV)
    L_0 : crossover thickness (nm)
    c1 : dimension flow parameter
    """
    return B_2D / (1 + (L_0 / L)**(1/c1))**2


def fit_binding_energy():
    """Fit binding energy data to extract c1"""
    
    # Initial guess: B_2D ~ 15 meV, L_0 ~ 0.5 nm, c1 ~ 1.0
    p0 = [15.0, 0.5, 1.0]
    
    # Bounds to ensure physical parameters
    bounds = ([10.0, 0.1, 0.1], [20.0, 2.0, 3.0])
    
    try:
        popt, pcov = curve_fit(
            binding_energy_model, 
            thickness_nm, 
            binding_energy_meV,
            p0=p0,
            sigma=uncertainty_meV,
            bounds=bounds,
            absolute_sigma=True
        )
        
        B_2D_fit, L_0_fit, c1_fit = popt
        B_2D_err, L_0_err, c1_err = np.sqrt(np.diag(pcov))
        
        return popt, pcov, (B_2D_err, L_0_err, c1_err)
    except Exception as e:
        print(f"Fit failed: {e}")
        return None, None, None


def calculate_chi_square(popt):
    """Calculate chi-square for the fit"""
    B_pred = binding_energy_model(thickness_nm, *popt)
    residuals = (binding_energy_meV - B_pred) / uncertainty_meV
    chi2 = np.sum(residuals**2)
    return chi2


def profile_likelihood_c1(n_points=50):
    """Calculate profile likelihood for c1"""
    c1_values = np.linspace(0.1, 3.0, n_points)
    chi2_values = []
    
    for c1 in c1_values:
        # Fix c1, optimize other parameters
        def model_fixed_c1(L, B_2D, L_0):
            return binding_energy_model(L, B_2D, L_0, c1)
        
        try:
            popt, _ = curve_fit(
                model_fixed_c1,
                thickness_nm,
                binding_energy_meV,
                p0=[15.0, 0.5],
                sigma=uncertainty_meV,
                absolute_sigma=True
            )
            B_pred = model_fixed_c1(thickness_nm, *popt)
            residuals = (binding_energy_meV - B_pred) / uncertainty_meV
            chi2 = np.sum(residuals**2)
            chi2_values.append(chi2)
        except:
            chi2_values.append(np.inf)
    
    return c1_values, np.array(chi2_values)


def plot_results(popt, save_path='inas_qw_analysis.png'):
    """Plot binding energy fit and c1 profile likelihood"""
    
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    # Left panel: Binding energy vs thickness
    ax1 = axes[0]
    
    # Plot data
    ax1.errorbar(thickness_nm, binding_energy_meV, yerr=uncertainty_meV,
                fmt='o', markersize=10, capsize=5, capthick=2,
                label='Experimental data', color='blue', zorder=5)
    
    # Plot fit
    L_fit = np.linspace(0.2, 1.0, 100)
    B_fit = binding_energy_model(L_fit, *popt)
    ax1.plot(L_fit, B_fit, 'r-', linewidth=2, label='Dimension flow fit', zorder=3)
    
    # Plot asymptotes
    ax1.axhline(y=B_2D_ideal, color='gray', linestyle='--', alpha=0.7,
               label=f'Ideal 2D limit: {B_2D_ideal} meV')
    ax1.axhline(y=rydberg_3D, color='gray', linestyle=':', alpha=0.7,
               label=f'3D limit: {rydberg_3D} meV')
    
    ax1.set_xlabel('Well Thickness (nm)', fontsize=12)
    ax1.set_ylabel('Binding Energy (meV)', fontsize=12)
    ax1.set_title('InAs/GaAs QW: Binding Energy vs Thickness', fontsize=13)
    ax1.legend(loc='lower right', fontsize=9)
    ax1.set_xlim(0.2, 1.0)
    ax1.set_ylim(0, 18)
    ax1.grid(True, alpha=0.3)
    
    # Add fit parameters
    B_2D_fit, L_0_fit, c1_fit = popt
    textstr = f'Fit Parameters:\n'
    textstr += f'$B_{{2D}}$ = {B_2D_fit:.1f} meV\n'
    textstr += f'$L_0$ = {L_0_fit:.3f} nm\n'
    textstr += f'$c_1$ = {c1_fit:.3f}'
    ax1.text(0.65, 0.5, textstr, transform=ax1.transAxes, fontsize=10,
            verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
    
    # Right panel: Profile likelihood for c1
    ax2 = axes[1]
    
    c1_values, chi2_values = profile_likelihood_c1()
    chi2_min = np.min(chi2_values)
    delta_chi2 = chi2_values - chi2_min
    
    ax2.plot(c1_values, delta_chi2, 'b-', linewidth=2)
    ax2.axhline(y=1.0, color='red', linestyle='--', alpha=0.7, label='$\\Delta\\chi^2 = 1$ (68% CL)')
    ax2.axhline(y=4.0, color='orange', linestyle='--', alpha=0.7, label='$\\Delta\\chi^2 = 4$ (95% CL)')
    ax2.axvline(x=1.0, color='green', linestyle=':', alpha=0.7, linewidth=2,
               label='Theoretical: $c_1 = 1.0$')
    
    # Mark best fit
    ax2.axvline(x=c1_fit, color='blue', linestyle='-', alpha=0.5)
    ax2.plot(c1_fit, 0, 'bo', markersize=10, zorder=5)
    
    ax2.set_xlabel('$c_1$ Parameter', fontsize=12)
    ax2.set_ylabel('$\\Delta\\chi^2$', fontsize=12)
    ax2.set_title('Profile Likelihood for $c_1$', fontsize=13)
    ax2.legend(loc='upper right', fontsize=9)
    ax2.set_xlim(0.1, 3.0)
    ax2.set_ylim(0, 10)
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=150, bbox_inches='tight')
    print(f"\nPlot saved to: {save_path}")
    
    return fig


def main():
    """Main analysis"""
    
    # Perform fit
    print("\n" + "=" * 70)
    print("FIT RESULTS")
    print("=" * 70)
    
    popt, pcov, errors = fit_binding_energy()
    
    if popt is None:
        print("Fit failed!")
        return
    
    B_2D_fit, L_0_fit, c1_fit = popt
    B_2D_err, L_0_err, c1_err = errors
    
    chi2 = calculate_chi_square(popt)
    dof = len(thickness_nm) - 3  # degrees of freedom
    chi2_red = chi2 / dof if dof > 0 else np.inf
    
    print(f"\nFit Parameters:")
    print(f"  B_2D = {B_2D_fit:.2f} ± {B_2D_err:.2f} meV")
    print(f"  L_0  = {L_0_fit:.4f} ± {L_0_err:.4f} nm")
    print(f"  c_1  = {c1_fit:.3f} ± {c1_err:.3f}")
    print(f"\nGoodness of fit:")
    print(f"  χ² = {chi2:.3f}")
    print(f"  dof = {dof}")
    print(f"  χ²/dof = {chi2_red:.3f}")
    
    # Compare with theoretical prediction
    c1_theory = 1.0
    deviation = (c1_fit - c1_theory) / c1_err
    print(f"\nComparison with theory c_1(2,0) = 1.0:")
    print(f"  Measured: {c1_fit:.3f} ± {c1_err:.3f}")
    print(f"  Expected: {c1_theory:.1f}")
    print(f"  Deviation: {deviation:.2f}σ")
    
    # Confidence interval for c1
    c1_values, chi2_values = profile_likelihood_c1()
    chi2_min = np.min(chi2_values)
    delta_chi2 = chi2_values - chi2_min
    
    # Find 68% confidence interval (delta chi2 = 1)
    within_1sigma = c1_values[delta_chi2 <= 1.0]
    if len(within_1sigma) > 0:
        c1_lower = np.min(within_1sigma)
        c1_upper = np.max(within_1sigma)
        print(f"\n68% Confidence Interval: [{c1_lower:.3f}, {c1_upper:.3f}]")
    
    # Predicted binding energies
    print(f"\nPredicted vs Measured:")
    B_pred = binding_energy_model(thickness_nm, *popt)
    for i, (L, B_meas, B_calc) in enumerate(zip(thickness_ML, binding_energy_meV, B_pred)):
        residual = B_meas - B_calc
        print(f"  L = {L} ML: Measured = {B_meas:.1f}, Predicted = {B_calc:.2f}, Residual = {residual:.2f}")
    
    # Create plot
    fig = plot_results(popt)
    
    print("\n" + "=" * 70)
    print("CONCLUSION")
    print("=" * 70)
    if abs(deviation) < 2:
        print(f"✓ Extracted c_1 = {c1_fit:.3f} ± {c1_err:.3f} is CONSISTENT with")
        print(f"  theoretical value c_1(2,0) = 1.0 within {abs(deviation):.1f}σ")
    else:
        print(f"⚠ Extracted c_1 = {c1_fit:.3f} ± {c1_err:.3f} DEVIATES from")
        print(f"  theoretical value c_1(2,0) = 1.0 by {abs(deviation):.1f}σ")
    print("=" * 70)
    
    return popt, errors


if __name__ == "__main__":
    main()
