#!/usr/bin/env python3
"""
Simplified iTEBD for Quantum Dimension Analysis (Pure Python)
===============================================================

No external dependencies - uses only standard library and numpy.
"""

import numpy as np
import json
from typing import Tuple, List


class SimpleiTEBD:
    """
    Simplified iTEBD for transverse field Ising model.
    
    Hamiltonian: H = -J * sum(Z_i Z_{i+1}) - h * sum(X_i)
    """
    
    def __init__(self, J: float = 1.0, h: float = 1.0, chi: int = 20, dt: float = 0.05):
        """
        Initialize iTEBD.
        
        Args:
            J: ZZ coupling strength
            h: Transverse field
            chi: Bond dimension
            dt: Time step for imaginary time evolution
        """
        self.J = J
        self.h = h
        self.chi = chi
        self.dt = dt
        
        # Pauli matrices
        self.I = np.array([[1, 0], [0, 1]], dtype=complex)
        self.X = np.array([[0, 1], [1, 0]], dtype=complex)
        self.Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
        self.Z = np.array([[1, 0], [0, -1]], dtype=complex)
        
        # Initialize tensors
        self.GammaA = np.random.randn(chi, 2, chi) + 1j * np.random.randn(chi, 2, chi)
        self.GammaB = np.random.randn(chi, 2, chi) + 1j * np.random.randn(chi, 2, chi)
        self.LambdaA = np.ones(chi) / np.sqrt(chi)
        self.LambdaB = np.ones(chi) / np.sqrt(chi)
        
        # Build evolution gate
        self.gate = self._build_gate()
        
    def _build_gate(self) -> np.ndarray:
        """Build two-site evolution gate."""
        # H = -J * ZZ - h * X
        H = -self.J * np.kron(self.Z, self.Z) - self.h * (np.kron(self.X, self.I) + np.kron(self.I, self.X)) / 2
        
        # Simple matrix exponential using Taylor series
        def matrix_exp_taylor(H, dt, order=10):
            """Compute exp(-dt*H) using Taylor series."""
            result = np.eye(H.shape[0], dtype=complex)
            term = np.eye(H.shape[0], dtype=complex)
            for k in range(1, order):
                term = -dt * H @ term / k
                result += term
            return result
        
        U = matrix_exp_taylor(H, self.dt)
        return U.reshape(2, 2, 2, 2)
    
    def _svd(self, M: np.ndarray, chi: int) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Simple SVD using numpy.
        
        Returns:
            U, S, Vh truncated to chi
        """
        try:
            U, S, Vh = np.linalg.svd(M, full_matrices=False)
        except:
            # Fallback to eigendecomposition if SVD fails
            MM = M @ M.conj().T
            w, v = np.linalg.eigh(MM)
            w = np.maximum(w, 0)  # Ensure non-negative
            S = np.sqrt(w)
            U = v
            Vh = U.conj().T @ M / (S[:, None] + 1e-15)
        
        # Truncate
        chi_new = min(len(S), chi)
        U = U[:, :chi_new]
        S = S[:chi_new]
        Vh = Vh[:chi_new, :]
        
        return U, S, Vh
    
    def step(self):
        """Perform one iTEBD step."""
        # Contract: LambdaB - GammaA - LambdaA - GammaB - LambdaB
        theta = np.tensordot(np.diag(self.LambdaB), self.GammaA, axes=(1, 0))  # (chi, d, chi)
        theta = np.tensordot(theta, np.diag(self.LambdaA), axes=(2, 0))  # (chi, d, chi)
        theta = np.tensordot(theta, self.GammaB, axes=(2, 0))  # (chi, d, chi, d, chi)
        theta = np.tensordot(theta, np.diag(self.LambdaB), axes=(4, 0))  # (chi, d, chi, d, chi)
        
        # Apply gate
        theta = np.tensordot(theta, self.gate, axes=([1, 3], [0, 1]))  # (chi, chi, chi, d, d)
        theta = theta.transpose(0, 3, 1, 4, 2)  # (chi, d, chi, d, chi)
        chi1, d, chi2, d2, chi3 = theta.shape
        theta = theta.reshape(chi1 * d, chi2 * d2 * chi3)
        
        # SVD
        U, S, Vh = self._svd(theta, self.chi)
        
        # Normalize
        norm = np.linalg.norm(S)
        if norm > 0:
            S = S / norm
        
        # Update tensors
        chi_new = len(S)
        self.LambdaA = S
        
        # Reshape U -> GammaA
        self.GammaA = U.reshape(self.chi, 2, chi_new)
        
        # Renormalize
        for i in range(chi_new):
            if S[i] > 1e-15:
                self.GammaA[:, :, i] /= S[i]
        
        # Reshape Vh -> GammaB
        V = Vh.conj().T
        self.GammaB = V.reshape(chi_new, 2, self.chi)
        for i in range(chi_new):
            if S[i] > 1e-15:
                self.GammaB[i, :, :] /= S[i]
        
        self.LambdaB = S
    
    def entanglement_entropy(self) -> float:
        """Compute von Neumann entanglement entropy."""
        probs = self.LambdaA ** 2
        probs = probs[probs > 1e-15]
        if len(probs) == 0:
            return 0.0
        S = -np.sum(probs * np.log(probs))
        return S
    
    def effective_dimension(self, L: int = None) -> float:
        """
        Compute effective quantum dimension.
        
        d_eff = 1 + S / log(L)
        """
        S = self.entanglement_entropy()
        
        if L is None:
            # Estimate from correlation length
            L_eff = max(10, int(np.exp(S)))
        else:
            L_eff = L
        
        d_eff = 1.0 + S / np.log(L_eff)
        return d_eff
    
    def run(self, num_steps: int, measure_every: int = 10) -> dict:
        """
        Run iTEBD evolution.
        
        Args:
            num_steps: Number of steps
            measure_every: Measure every N steps
            
        Returns:
            Dictionary with results
        """
        results = {
            'steps': [],
            'entropy': [],
            'dimension': []
        }
        
        print(f"Running iTEBD: J={self.J}, h={self.h}, chi={self.chi}")
        print(f"Steps: {num_steps}")
        print("-" * 50)
        
        for step in range(num_steps):
            self.step()
            
            if step % measure_every == 0 or step == num_steps - 1:
                S = self.entanglement_entropy()
                d_eff = self.effective_dimension()
                
                results['steps'].append(step)
                results['entropy'].append(float(S))
                results['dimension'].append(float(d_eff))
                
                print(f"Step {step:5d}: S={S:.6f}, d_eff={d_eff:.4f}")
        
        return results


def critical_point_study():
    """
    Study Ising model across critical point h/J = 1.
    Expected: d_eff peaks at criticality.
    """
    print("=" * 60)
    print("Ising Model Critical Point Study")
    print("=" * 60)
    
    J = 1.0
    h_values = np.linspace(0.5, 2.0, 8)
    results = []
    
    for h in h_values:
        print(f"\n>>> h/J = {h/J:.3f}")
        
        itebd = SimpleiTEBD(J=J, h=h, chi=20, dt=0.05)
        history = itebd.run(num_steps=500, measure_every=100)
        
        final_d = history['dimension'][-1]
        final_S = history['entropy'][-1]
        
        results.append({
            'h_over_J': float(h/J),
            'h': float(h),
            'dimension': final_d,
            'entropy': final_S
        })
        
        print(f"Final: d_eff = {final_d:.4f}")
    
    # Save results
    output = {
        'model': 'Transverse Field Ising',
        'J': J,
        'chi': 20,
        'num_steps': 500,
        'results': results
    }
    
    with open('ising_critical_results.json', 'w') as f:
        json.dump(output, f, indent=2)
    
    print("\n" + "=" * 60)
    print("Results saved to ising_critical_results.json")
    print("=" * 60)
    
    # Analysis
    print("\n--- Analysis ---")
    dims = [r['dimension'] for r in results]
    hs = [r['h_over_J'] for r in results]
    
    max_idx = np.argmax(dims)
    print(f"Maximum d_eff = {dims[max_idx]:.4f} at h/J = {hs[max_idx]:.3f}")
    print(f"Expected: h/J = 1.0 (critical point)")
    print(f"Expected d_eff (Ising CFT) = 1.167")
    
    return results


def area_law_verification():
    """
    Verify area law vs volume law for different parameter regimes.
    """
    print("\n" + "=" * 60)
    print("Area Law vs Volume Law Verification")
    print("=" * 60)
    
    # Ferromagnetic phase (h < J): Area law expected
    print("\n1. Ferromagnetic phase (h=0.5, J=1.0):")
    itebd_fm = SimpleiTEBD(J=1.0, h=0.5, chi=30)
    result_fm = itebd_fm.run(num_steps=300, measure_every=50)
    S_fm = result_fm['entropy'][-1]
    print(f"   Entropy: {S_fm:.4f} (should be O(1), area law)")
    
    # Critical point (h = J): Logarithmic correction
    print("\n2. Critical point (h=1.0, J=1.0):")
    itebd_crit = SimpleiTEBD(J=1.0, h=1.0, chi=30)
    result_crit = itebd_crit.run(num_steps=300, measure_every=50)
    S_crit = result_crit['entropy'][-1]
    print(f"   Entropy: {S_crit:.4f} (should be ~log(L), logarithmic)")
    
    # Paramagnetic phase (h > J): Area law
    print("\n3. Paramagnetic phase (h=2.0, J=1.0):")
    itebd_pm = SimpleiTEBD(J=1.0, h=2.0, chi=30)
    result_pm = itebd_pm.run(num_steps=300, measure_every=50)
    S_pm = result_pm['entropy'][-1]
    print(f"   Entropy: {S_pm:.4f} (should be O(1), area law)")
    
    print("\n" + "=" * 60)
    print("Verification complete!")
    print(f"FM: S={S_fm:.4f}, Critical: S={S_crit:.4f}, PM: S={S_pm:.4f}")
    print("=" * 60)


if __name__ == '__main__':
    print("Simple iTEBD Quantum Dimension Simulator")
    print("Pure Python implementation (no scipy required)")
    print("=" * 60)
    
    # Run area law verification
    area_law_verification()
    
    # Run critical point study
    print("\n")
    critical_point_study()
    
    print("\n" + "=" * 60)
    print("All simulations complete!")
    print("=" * 60)
