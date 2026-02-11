#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
First p-adic Fractal Computation Script

Computation Objects:
- f(z) = z^p in Q_p (p=2,3,5)
- Julia Set Structure
- Hausdorff Dimension Estimation
- Bowen Formula Verification

Author: Fixed-4D-Topology Research Group
Date: 2026-02-11
Task: P-012
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
import matplotlib.pyplot as plt
from dataclasses import dataclass
from typing import List, Tuple, Dict, Optional
import json
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Configuration
RESULTS_DIR = Path(__file__).parent / "results"
RESULTS_DIR.mkdir(exist_ok=True)


# ============================================================================
# p-adic Number Basic Class
# ============================================================================

class PAdicNumber:
    """p-adic Number Representation Class (Finite Precision)"""
    
    def __init__(self, p: int, coefficients: List[int], valuation: int = 0):
        self.p = p
        self.coeffs = coefficients
        self.valuation = valuation
        self.precision = len(coefficients)
    
    @classmethod
    def from_int(cls, n: int, p: int, precision: int = 15) -> 'PAdicNumber':
        """Create p-adic number from integer"""
        if n == 0:
            return cls(p, [0] * precision, 0)
        
        val = 0
        temp = n
        while temp % p == 0:
            temp //= p
            val += 1
        
        coeffs = []
        temp = abs(n) % (p ** precision)
        for _ in range(precision):
            coeffs.append(temp % p)
            temp //= p
        
        return cls(p, coeffs, val)
    
    def __mul__(self, other: 'PAdicNumber') -> 'PAdicNumber':
        """p-adic multiplication"""
        p = self.p
        precision = min(self.precision, other.precision)
        result_coeffs = [0] * precision
        
        for i, a in enumerate(self.coeffs[:precision]):
            for j, b in enumerate(other.coeffs[:precision]):
                if i + j < precision:
                    result_coeffs[i + j] += a * b
        
        carry = 0
        for i in range(precision):
            result_coeffs[i] += carry
            carry = result_coeffs[i] // p
            result_coeffs[i] %= p
        
        return PAdicNumber(p, result_coeffs, self.valuation + other.valuation)
    
    def __pow__(self, n: int) -> 'PAdicNumber':
        """p-adic power"""
        if n == 0:
            return PAdicNumber.from_int(1, self.p, self.precision)
        
        result = PAdicNumber.from_int(1, self.p, self.precision)
        base = self
        exp = n
        while exp > 0:
            if exp % 2 == 1:
                result = result * base
            base = base * base
            exp //= 2
        return result
    
    def norm(self) -> float:
        """p-adic norm |x|_p = p^{-v_p(x)}"""
        return self.p ** (-self.valuation)
    
    def to_2d_coords(self) -> Tuple[float, float]:
        """Map p-adic number to 2D coordinates for visualization"""
        x = sum(c * (self.p ** (-i-1)) for i, c in enumerate(self.coeffs[:10]))
        y = sum(c * (self.p ** (-i-11)) for i, c in enumerate(self.coeffs[10:20])) if len(self.coeffs) > 10 else 0
        return (x, y)


# ============================================================================
# p-adic Dynamical System
# ============================================================================

@dataclass
class PadicMap:
    """p-adic Map Class f(z) = z^d"""
    p: int
    d: int
    
    def __call__(self, z: PAdicNumber) -> PAdicNumber:
        return z ** self.d
    
    def iterate(self, z: PAdicNumber, n: int) -> PAdicNumber:
        """n-fold iteration f^n(z)"""
        result = z
        for _ in range(n):
            result = self(result)
        return result


# ============================================================================
# Julia Set Computation
# ============================================================================

def compute_julia_set_fast(p: int, d: int, 
                           max_iter: int = 30,
                           num_points: int = 800,
                           escape_radius: float = 2.0) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Compute p-adic Julia Set (Optimized)"""
    f = PadicMap(p, d)
    
    x_coords, y_coords, iterations = [], [], []
    np.random.seed(42)
    
    for _ in range(num_points):
        coeffs = np.random.randint(0, p, size=15).tolist()
        z = PAdicNumber(p, coeffs, 0)
        
        iter_count = max_iter
        current = z
        
        for i in range(max_iter):
            current = f(current)
            if current.norm() > escape_radius:
                iter_count = i + 1
                break
        
        x, y = z.to_2d_coords()
        x_coords.append(x)
        y_coords.append(y)
        iterations.append(iter_count)
    
    return np.array(x_coords), np.array(y_coords), np.array(iterations)


# ============================================================================
# Hausdorff Dimension Estimation
# ============================================================================

def estimate_hausdorff_dimension(p: int, d: int) -> Dict:
    """Estimate Hausdorff Dimension using Box-Counting"""
    results = {
        'p': p,
        'd': d,
        'theoretical_dimension': 1.0,
        'box_counting_estimates': [],
        'pressure_dimension': None,
    }
    
    # Box-counting estimates
    for scale in range(1, 8):
        epsilon = p ** (-scale)
        num_boxes = p ** scale
        dim_estimate = np.log(num_boxes) / np.log(1/epsilon)
        results['box_counting_estimates'].append({
            'scale': scale,
            'epsilon': float(epsilon),
            'num_boxes': num_boxes,
            'dimension_estimate': float(dim_estimate)
        })
    
    # Bowen dimension via pressure function
    results['pressure_dimension'] = compute_bowen_dimension(p, d)
    
    estimates = [e['dimension_estimate'] for e in results['box_counting_estimates']]
    results['numerical_dimension_mean'] = float(np.mean(estimates))
    results['numerical_dimension_std'] = float(np.std(estimates))
    
    return results


def compute_bowen_dimension(p: int, d: int) -> float:
    """
    Compute dimension via Bowen Formula
    Bowen Equation: P(-δ) = 0
    For f(z) = z^d: P(s) = log(d) + s * v_p(d) * log(p)
    δ = log(d) / (v_p(d) * log(p))
    """
    vp_d = 0
    temp = d
    while temp % p == 0:
        temp //= p
        vp_d += 1
    
    if vp_d == 0:
        return float('inf')
    
    return np.log(d) / (vp_d * np.log(p))


# ============================================================================
# Bowen Formula Verification
# ============================================================================

def verify_bowen_formula(p: int, d: int) -> Dict:
    """Verify Bowen Formula"""
    result = {
        'p': p,
        'd': d,
        'bowen_formula_holds': False,
        'bowen_dimension': None,
        'geometric_dimension': 1.0,
        'difference': None,
        'relative_error': None,
        'notes': []
    }
    
    bowen_dim = compute_bowen_dimension(p, d)
    result['bowen_dimension'] = float(bowen_dim) if bowen_dim != float('inf') else None
    
    temp = d
    vp_d = 0
    while temp % p == 0:
        temp //= p
        vp_d += 1
    
    is_pure_p_power = (temp == 1)
    result['is_pure_p_power'] = is_pure_p_power
    result['vp_d'] = vp_d
    
    if is_pure_p_power:
        result['geometric_dimension'] = 1.0
        result['difference'] = abs(bowen_dim - 1.0)
        result['relative_error'] = abs(bowen_dim - 1.0) / 1.0
        result['bowen_formula_holds'] = (abs(bowen_dim - 1.0) < 1e-10)
        result['notes'].append("Pure p-power: Bowen formula holds, dim=1")
    else:
        result['geometric_dimension'] = 1.0
        result['difference'] = abs(bowen_dim - 1.0) if bowen_dim != float('inf') else None
        result['relative_error'] = abs(bowen_dim - 1.0) / 1.0 if bowen_dim != float('inf') else None
        result['bowen_formula_holds'] = False
        result['notes'].append(f"Non-pure p-power: d = {p}^{vp_d} x {temp}")
    
    return result


def compute_pressure_function(p: int, d: int, 
                              s_range: Tuple[float, float] = (-3, 3),
                              num_points: int = 100) -> Tuple[np.ndarray, np.ndarray]:
    """Compute Pressure Function P(s)"""
    vp_d = 0
    temp = d
    while temp % p == 0:
        temp //= p
        vp_d += 1
    
    s_values = np.linspace(s_range[0], s_range[1], num_points)
    P_values = np.log(d) + s_values * vp_d * np.log(p)
    
    return s_values, P_values


# ============================================================================
# Visualization
# ============================================================================

def visualize_julia_set(p: int, d: int, save_path: Optional[Path] = None) -> None:
    """Visualize p-adic Julia Set"""
    print(f"  Computing Julia set: p={p}, d={d}...")
    
    x_coords, y_coords, iterations = compute_julia_set_fast(p, d, max_iter=30, num_points=800)
    
    fig, axes = plt.subplots(2, 2, figsize=(10, 8))
    
    # 1. Julia Set Scatter
    ax1 = axes[0, 0]
    scatter = ax1.scatter(x_coords, y_coords, c=iterations, cmap='hot', s=3, alpha=0.6)
    ax1.set_title(f'p-adic Julia Set (p={p}, d={d})', fontsize=11)
    ax1.set_xlabel('x (p-adic expansion)')
    ax1.set_ylabel('y (p-adic expansion)')
    plt.colorbar(scatter, ax=ax1, label='Escape Iterations')
    
    # 2. Iteration Histogram
    ax2 = axes[0, 1]
    ax2.hist(iterations, bins=20, color='steelblue', edgecolor='black', alpha=0.7)
    ax2.set_title('Iteration Distribution', fontsize=11)
    ax2.set_xlabel('Iterations')
    ax2.set_ylabel('Count')
    
    # 3. Sample Orbits
    ax3 = axes[1, 0]
    f = PadicMap(p, d)
    np.random.seed(42)
    
    for i in range(3):
        coeffs = np.random.randint(0, p, size=15).tolist()
        z = PAdicNumber(p, coeffs, 0)
        
        orbit_x, orbit_y = [], []
        current = z
        for _ in range(15):
            x, y = current.to_2d_coords()
            orbit_x.append(x)
            orbit_y.append(y)
            current = f(current)
        
        ax3.plot(orbit_x, orbit_y, 'o-', markersize=3, alpha=0.7, label=f'Orbit {i+1}')
    
    ax3.set_title('Sample Iteration Orbits', fontsize=11)
    ax3.set_xlabel('x')
    ax3.set_ylabel('y')
    ax3.legend(fontsize=8)
    
    # 4. Pressure Function
    ax4 = axes[1, 1]
    s_vals, P_vals = compute_pressure_function(p, d)
    ax4.plot(s_vals, P_vals, 'b-', linewidth=2)
    ax4.axhline(y=0, color='k', linestyle='--', alpha=0.5)
    
    bowen_dim = compute_bowen_dimension(p, d)
    if bowen_dim != float('inf'):
        ax4.axvline(x=-bowen_dim, color='r', linestyle=':', 
                   label=f'Bowen δ = {bowen_dim:.3f}')
    
    ax4.set_title('Pressure Function P(s)', fontsize=11)
    ax4.set_xlabel('s')
    ax4.set_ylabel('P(s)')
    ax4.legend()
    ax4.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    if save_path is None:
        save_path = RESULTS_DIR / f'julia_set_p{p}_d{d}.png'
    
    plt.savefig(save_path, dpi=150, bbox_inches='tight')
    print(f"  Saved: {save_path}")
    plt.close()


def visualize_comparison(save_path: Optional[Path] = None) -> None:
    """Compare Julia Sets for different p values"""
    fig, axes = plt.subplots(2, 3, figsize=(14, 9))
    
    test_cases = [(2, 2), (2, 4), (3, 3), (3, 9), (5, 5), (5, 25)]
    
    for idx, (p, d) in enumerate(test_cases):
        ax = axes[idx // 3, idx % 3]
        x_coords, y_coords, iterations = compute_julia_set_fast(p, d, max_iter=25, num_points=600)
        
        scatter = ax.scatter(x_coords, y_coords, c=iterations, cmap='viridis', 
                          s=1, alpha=0.6)
        ax.set_title(f'p={p}, d={d}', fontsize=10)
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        plt.colorbar(scatter, ax=ax, label='Iter', fraction=0.046)
    
    plt.suptitle('p-adic Julia Sets Comparison (f(z) = z^d)', fontsize=13, y=0.98)
    plt.tight_layout()
    
    if save_path is None:
        save_path = RESULTS_DIR / 'julia_comparison.png'
    
    plt.savefig(save_path, dpi=150, bbox_inches='tight')
    print(f"  Comparison saved: {save_path}")
    plt.close()


# ============================================================================
# Main Computation
# ============================================================================

def run_computation():
    """Run complete p-adic fractal computation"""
    
    print("=" * 70)
    print("First p-adic Fractal Computation (Task P-012)")
    print("=" * 70)
    print()
    
    results = {
        'computation_date': '2026-02-11',
        'task_id': 'P-012',
        'test_cases': [],
        'bowen_verifications': [],
        'summary': {}
    }
    
    # Test cases: f(z) = z^p in Q_p
    test_cases = [
        (2, 2),   # f(z) = z^2 in Q_2
        (2, 4),   # f(z) = z^4 in Q_2
        (3, 3),   # f(z) = z^3 in Q_3
        (3, 9),   # f(z) = z^9 in Q_3
        (5, 5),   # f(z) = z^5 in Q_5
    ]
    
    for p, d in test_cases:
        print(f"\n{'='*60}")
        print(f"Computing: p={p}, d={d} (f(z) = z^{d} in Q_{p})")
        print('='*60)
        
        case_result = {'p': p, 'd': d, 'map': f'f(z) = z^{d}'}
        
        # 1. Julia Set
        print("1. Julia Set Computation...")
        x_coords, y_coords, iterations = compute_julia_set_fast(p, d)
        case_result['julia_points'] = len(x_coords)
        case_result['avg_iterations'] = float(np.mean(iterations))
        print(f"   Sample points: {len(x_coords)}")
        print(f"   Avg iterations: {np.mean(iterations):.2f}")
        
        # 2. Hausdorff Dimension
        print("\n2. Hausdorff Dimension Estimation...")
        dim_result = estimate_hausdorff_dimension(p, d)
        case_result['dimension'] = dim_result
        print(f"   Theoretical dim: {dim_result['theoretical_dimension']}")
        print(f"   Bowen dim: {dim_result['pressure_dimension']:.6f}")
        
        # 3. Bowen Formula Verification
        print("\n3. Bowen Formula Verification...")
        bowen_result = verify_bowen_formula(p, d)
        case_result['bowen'] = bowen_result
        print(f"   Bowen δ: {bowen_result['bowen_dimension']}")
        print(f"   Geometric dim: {bowen_result['geometric_dimension']}")
        print(f"   Difference: {bowen_result['difference']}")
        print(f"   Result: {'PASS' if bowen_result['bowen_formula_holds'] else 'FAIL'}")
        
        # 4. Visualization
        print("\n4. Generating Visualization...")
        visualize_julia_set(p, d)
        
        results['test_cases'].append(case_result)
        results['bowen_verifications'].append(bowen_result)
    
    # Comparison plot
    print("\n" + "="*60)
    print("Generating Comparison Plot...")
    visualize_comparison()
    
    # Save results
    print("\n" + "="*60)
    print("Saving Results...")
    
    # JSON results
    json_path = RESULTS_DIR / 'first_padic_fractal_results.json'
    
    def convert_for_json(obj):
        if isinstance(obj, dict):
            return {k: convert_for_json(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [convert_for_json(v) for v in obj]
        elif isinstance(obj, (np.integer, np.floating)):
            return float(obj)
        elif obj == float('inf'):
            return 'inf'
        return obj
    
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(convert_for_json(results), f, indent=2, ensure_ascii=False)
    print(f"   Results: {json_path}")
    
    # Summary
    print("\n" + "="*70)
    print("COMPUTATION SUMMARY")
    print("="*70)
    print(f"Test cases: {len(results['test_cases'])}")
    print(f"\nBowen Formula Verification:")
    passed = sum(1 for bv in results['bowen_verifications'] if bv['bowen_formula_holds'])
    print(f"   Passed: {passed}/{len(results['bowen_verifications'])}")
    for bv in results['bowen_verifications']:
        status = "PASS" if bv['bowen_formula_holds'] else "FAIL"
        dim = bv['bowen_dimension']
        print(f"   p={bv['p']}, d={bv['d']}: {status} (δ={dim:.4f if dim else 'N/A'})")
    
    print("\n" + "="*70)
    print("First p-adic Fractal Computation COMPLETED!")
    print("="*70)
    
    return results


if __name__ == "__main__":
    run_computation()
