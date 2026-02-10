#!/usr/bin/env python3
"""
iTEBD (infinite Time-Evolving Block Decimation) for Quantum Dimension Analysis
==============================================================================

Computes effective quantum dimension from entanglement entropy of 1D spin chains.

References:
- Vidal, PRL 98, 070201 (2007)
- Orus, Annals of Physics 349, 117 (2014)
"""

import numpy as np
from typing import Tuple, List, Callable
import json


class MPS:
    """Matrix Product State for infinite 1D spin chain."""
    
    def __init__(self, physical_dim: int, bond_dim: int):
        """
        Initialize MPS.
        
        Args:
            physical_dim: Dimension of physical Hilbert space (e.g., 2 for spin-1/2)
            bond_dim: Bond dimension (maximum entanglement)
        """
        self.d = physical_dim
        self.chi = bond_dim
        
        # Gamma tensors: shape (chi, d, chi)
        # Lambda matrices: diagonal, shape (chi,)
        self.GammaA = np.random.randn(bond_dim, physical_dim, bond_dim) + 1j * np.random.randn(bond_dim, physical_dim, bond_dim)
        self.GammaB = np.random.randn(bond_dim, physical_dim, bond_dim) + 1j * np.random.randn(bond_dim, physical_dim, bond_dim)
        self.LambdaA = np.ones(bond_dim) / np.sqrt(bond_dim)
        self.LambdaB = np.ones(bond_dim) / np.sqrt(bond_dim)
        
        # Normalize
        self._normalize()
    
    def _normalize(self):
        """Normalize MPS."""
        norm = np.linalg.norm(self.LambdaA)
        self.LambdaA /= norm
        self.LambdaB /= norm
    
    def get_entanglement_entropy(self) -> float:
        """
        Compute von Neumann entropy of half-chain.
        
        Returns:
            S_vN = -sum(lambda_i^2 log(lambda_i^2))
        """
        # Use LambdaA as singular values
        probs = self.LambdaA ** 2
        probs = probs[probs > 1e-15]  # Avoid log(0)
        
        S = -np.sum(probs * np.log(probs))
        return S
    
    def compute_effective_dimension(self, system_size: int = None) -> float:
        """
        Compute effective quantum dimension.
        
        Formula: d_eff^Q = 1 + S_vN / log(L)
        
        Args:
            system_size: System size L (for infinite chain, use correlation length)
            
        Returns:
            Effective dimension
        """
        S_vN = self.get_entanglement_entropy()
        
        if system_size is None:
            # Estimate from entanglement spectrum
            # For critical systems: xi ~ exp(S_vN)
            L_eff = int(np.exp(S_vN)) + 1
        else:
            L_eff = system_size
        
        d_eff = 1.0 + S_vN / np.log(L_eff)
        return d_eff


class iTEBDSimulator:
    """iTEBD simulator for 1D quantum spin chains."""
    
    def __init__(self, model: str = "ising", J: float = 1.0, h: float = 1.0, 
                 bond_dim: int = 100, dt: float = 0.01):
        """
        Initialize iTEBD simulator.
        
        Args:
            model: "ising", "heisenberg", "xy"
            J: Coupling constant
            h: Transverse field (for Ising)
            bond_dim: Maximum bond dimension
            dt: Imaginary time step
        """
        self.model = model
        self.J = J
        self.h = h
        self.chi = bond_dim
        self.dt = dt
        
        # Initialize MPS (spin-1/2, so d=2)
        self.mps = MPS(physical_dim=2, bond_dim=bond_dim)
        
        # Build Hamiltonian and Trotter gates
        self._build_gates()
    
    def _build_gates(self):
        """Build two-site Trotter-Suzuki gates."""
        # Pauli matrices
        I = np.eye(2)
        X = np.array([[0, 1], [1, 0]])
        Y = np.array([[0, -1j], [1j, 0]])
        Z = np.array([[1, 0], [0, -1]])
        
        if self.model == "ising":
            # H = -J ZZ - h X
            H_local = -self.J * np.kron(Z, Z) - self.h * (np.kron(X, I) + np.kron(I, X)) / 2
        elif self.model == "heisenberg":
            # H = J (XX + YY + ZZ)
            H_local = self.J * (np.kron(X, X) + np.kron(Y, Y) + np.kron(Z, Z))
        elif self.model == "xy":
            # H = J (XX + YY)
            H_local = self.J * (np.kron(X, X) + np.kron(Y, Y))
        else:
            raise ValueError(f"Unknown model: {self.model}")
        
        # Trotter gate: U = exp(-dt * H)
        self.gate = self._matrix_exp(-self.dt * H_local)
        self.gate = self.gate.reshape(2, 2, 2, 2)
    
    def _matrix_exp(self, H: np.ndarray) -> np.ndarray:
        """Compute matrix exponential."""
        from scipy.linalg import expm
        return expm(H)
    
    def _apply_gate(self):
        """Apply one Trotter step."""
        # Get tensors
        GammaA = self.mps.GammaA
        GammaB = self.mps.GammaB
        LambdaA = self.mps.LambdaA
        LambdaB = self.mps.LambdaB
        
        # Contract: LambdaB - GammaA - LambdaA - GammaB - LambdaB
        theta = np.tensordot(np.diag(LambdaB), GammaA, axes=(1, 0))
        theta = np.tensordot(theta, np.diag(LambdaA), axes=(2, 0))
        theta = np.tensordot(theta, GammaB, axes=(2, 0))
        theta = np.tensordot(theta, np.diag(LambdaB), axes=(3, 0))
        # theta: (chi, d, chi, d, chi)
        
        # Apply gate
        theta = np.tensordot(theta, self.gate, axes=([1, 3], [0, 1]))
        # theta: (chi, chi, chi, d, d)
        theta = theta.transpose(0, 3, 1, 4, 2)
        theta = theta.reshape(self.mps.chi * 2, self.mps.chi * 2)
        
        # SVD
        U, S, Vh = np.linalg.svd(theta, full_matrices=False)
        
        # Truncate to bond dimension
        chi_new = min(len(S), self.mps.chi)
        U = U[:, :chi_new]
        S = S[:chi_new]
        Vh = Vh[:chi_new, :]
        
        # Normalize
        S = S / np.linalg.norm(S)
        
        # Update tensors
        self.mps.LambdaA = S
        self.mps.GammaA = U.reshape(self.mps.chi, 2, chi_new) / S[np.newaxis, np.newaxis, :]
        self.mps.GammaB = (Vh.T).reshape(chi_new, 2, self.mps.chi) / S[np.newaxis, np.newaxis, :]
        self.mps.LambdaB = S
    
    def evolve(self, num_steps: int, measure_interval: int = 10) -> dict:
        """
        Perform imaginary time evolution.
        
        Args:
            num_steps: Number of Trotter steps
            measure_interval: Measure every N steps
            
        Returns:
            Dictionary with evolution history
        """
        history = {
            'steps': [],
            'entropy': [],
            'dimension': [],
            'energy': []
        }
        
        print(f"Starting iTEBD evolution: {num_steps} steps")
        
        for step in range(num_steps):
            self._apply_gate()
            
            if step % measure_interval == 0 or step == num_steps - 1:
                S = self.mps.get_entanglement_entropy()
                d_eff = self.mps.compute_effective_dimension()
                
                history['steps'].append(step)
                history['entropy'].append(float(S))
                history['dimension'].append(float(d_eff))
                
                print(f"Step {step:5d}: S = {S:.6f}, d_eff = {d_eff:.4f}")
        
        return history


def run_ising_critical_study():
    """
    Study Ising model across critical point.
    Expected: d_eff peaks at h = J (critical point)
    """
    print("=" * 60)
    print("Ising Model Critical Point Study")
    print("=" * 60)
    
    J = 1.0
    h_values = np.linspace(0.5, 2.0, 16)
    results = []
    
    for h in h_values:
        print(f"\n--- h/J = {h/J:.3f} ---")
        
        sim = iTEBDSimulator(model="ising", J=J, h=h, bond_dim=50, dt=0.01)
        history = sim.evolve(num_steps=1000, measure_interval=100)
        
        final_d = history['dimension'][-1]
        final_S = history['entropy'][-1]
        
        results.append({
            'h_over_J': float(h/J),
            'dimension': final_d,
            'entropy': final_S
        })
        
        print(f"Final: d_eff = {final_d:.4f}, S = {final_S:.4f}")
    
    # Save results
    with open('ising_critical_dimension.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print("\n" + "=" * 60)
    print("Results saved to ising_critical_dimension.json")
    print("=" * 60)
    
    return results


def analyze_phase_transition(results: List[dict]):
    """Analyze critical behavior from results."""
    h_values = [r['h_over_J'] for r in results]
    d_values = [r['dimension'] for r in results]
    
    # Find maximum (critical point)
    max_idx = np.argmax(d_values)
    h_c = h_values[max_idx]
    d_c = d_values[max_idx]
    
    print("\nPhase Transition Analysis:")
    print(f"Critical point: h_c/J ≈ {h_c:.3f}")
    print(f"Maximum dimension: d_eff = {d_c:.4f}")
    print(f"Expected (Ising CFT): d_eff = 1 + c/3 = 1.167")
    print(f"Discrepancy: {abs(d_c - 1.167)/1.167 * 100:.1f}%")


if __name__ == '__main__':
    print("iTEBD Quantum Dimension Simulator")
    print("=" * 60)
    
    # Run critical study
    results = run_ising_critical_study()
    
    # Analyze
    analyze_phase_transition(results)
    
    print("\nSimulation complete!")
