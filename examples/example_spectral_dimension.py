"""
Example: Spectral Dimension Evolution (T2)

Demonstrates PDE evolution of spectral dimension on fractals.
"""

import numpy as np
from fixed_4d_topology import SpectralDimension


def main():
    print("=" * 60)
    print("Spectral Dimension Evolution Demo")
    print("=" * 60)
    print()
    
    # Test different fractals
    fractals = ["sierpinski", "cantor_dust"]
    
    for fractal in fractals:
        print(f"\n{fractal.upper()} Gasket")
        print("-" * 40)
        
        spec = SpectralDimension(fractal)
        d_s_exact = spec.fractal_info["d_s_exact"]
        
        print(f"Exact spectral dimension: d_s = {d_s_exact:.6f}")
        
        # Compute at different time scales
        print("\nTime evolution:")
        print(f"{'t':>12} {'d_s(t)':>12} {'Error':>12}")
        print("-" * 40)
        
        for t in [1e-1, 1e-2, 1e-3, 1e-4, 1e-5]:
            d_s = spec.compute_spectral_dimension(t)
            error = abs(d_s - d_s_exact)
            print(f"{t:>12.0e} {d_s:>12.6f} {error:>12.2e}")
        
        # Full evolution
        print("\nFull PDE evolution:")
        result = spec.evolve(t_span=(1e-5, 1.0), n_points=50)
        print(f"Initial d_s: {result.d_s_values[0]:.6f}")
        print(f"Final d_s: {result.d_s_values[-1]:.6f}")
        print(f"Convergence achieved: {'✓' if result.convergence_achieved else '✗'}")
    
    print("\n" + "=" * 60)
    print("Demo complete!")


if __name__ == "__main__":
    main()
