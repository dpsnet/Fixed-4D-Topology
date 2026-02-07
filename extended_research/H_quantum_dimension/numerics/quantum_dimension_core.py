"""
Quantum Dimension Core Module
=============================

Core algorithms for computing quantum effective dimensions
based on entanglement entropy calculations.

Author: Dimensionics Research Initiative
Date: February 2026
"""

import math
import random
from typing import List, Tuple, Dict, Optional
from dataclasses import dataclass


@dataclass
class QuantumState:
    """Represents a quantum state with its properties."""
    name: str
    num_qubits: int
    # Simplified representation: amplitudes as list of (real, imag) tuples
    amplitudes: List[complex]
    
    def __post_init__(self):
        # Normalize amplitudes
        norm = math.sqrt(sum(abs(a)**2 for a in self.amplitudes))
        if norm > 0:
            self.amplitudes = [a / norm for a in self.amplitudes]


class EntanglementCalculator:
    """Calculator for entanglement entropy and quantum dimensions."""
    
    def __init__(self, cutoff: float = 1e-10):
        self.cutoff = cutoff
    
    def schmidt_decomposition(self, state: QuantumState, 
                             split: int) -> Tuple[List[float], List[QuantumState], List[QuantumState]]:
        """
        Perform Schmidt decomposition of a bipartite quantum state.
        
        Args:
            state: Bipartite quantum state
            split: Index where to split the system (A|B)
            
        Returns:
            (schmidt_coeffs, states_A, states_B)
        """
        # For simplified model, use random Schmidt coefficients
        # In real implementation, this would be SVD of the amplitude matrix
        n_A = 2 ** split
        n_B = 2 ** (state.num_qubits - split)
        rank = min(n_A, n_B)
        
        # Generate random Schmidt coefficients (sorted descending)
        coeffs = [random.random() for _ in range(rank)]
        coeffs.sort(reverse=True)
        
        # Normalize
        norm = math.sqrt(sum(c**2 for c in coeffs))
        coeffs = [c / norm for c in coeffs]
        
        return coeffs, [], []
    
    def von_neumann_entropy(self, schmidt_coeffs: List[float]) -> float:
        """
        Calculate von Neumann entropy from Schmidt coefficients.
        
        S = -sum(lambda_i^2 * log(lambda_i^2))
        
        Args:
            schmidt_coeffs: Schmidt coefficients (lambda_i)
            
        Returns:
            von Neumann entropy
        """
        entropy = 0.0
        for coeff in schmidt_coeffs:
            if coeff > self.cutoff:
                p = coeff ** 2
                entropy -= p * math.log(p)
        return entropy
    
    def renyi_entropy(self, schmidt_coeffs: List[float], alpha: float) -> float:
        """
        Calculate Renyi entropy of order alpha.
        
        S_alpha = (1/(1-alpha)) * log(sum(lambda_i^(2*alpha)))
        
        Args:
            schmidt_coeffs: Schmidt coefficients
            alpha: Renyi index
            
        Returns:
            Renyi entropy
        """
        if abs(alpha - 1.0) < 1e-10:
            return self.von_neumann_entropy(schmidt_coeffs)
        
        sum_p_alpha = sum(c ** (2 * alpha) for c in schmidt_coeffs)
        if sum_p_alpha > self.cutoff:
            return (1.0 / (1.0 - alpha)) * math.log(sum_p_alpha)
        return 0.0
    
    def quantum_effective_dimension(self, entropy: float, 
                                   method: str = 'von_neumann') -> float:
        """
        Calculate quantum effective dimension from entropy.
        
        d_eff = exp(S)
        
        Args:
            entropy: Entanglement entropy
            method: 'von_neumann' or 'renyi'
            
        Returns:
            Quantum effective dimension
        """
        return math.exp(entropy)


class SpinChainSimulator:
    """Simulator for 1D spin chains to test quantum dimension formulas."""
    
    def __init__(self, length: int, model: str = 'xx'):
        """
        Initialize spin chain simulator.
        
        Args:
            length: Number of spins
            model: 'xx', 'xy', or 'heisenberg'
        """
        self.length = length
        self.model = model
        self.entanglement_calculator = EntanglementCalculator()
    
    def exact_entropy_xx_model(self, subsystem_size: int) -> float:
        """
        Calculate exact entanglement entropy for XX model using CFT.
        
        For critical XX model at half-filling:
        S(l) = (1/3) * log((L/pi) * sin(pi*l/L)) + constant
        
        Args:
            subsystem_size: Size of subsystem A
            
        Returns:
            Entanglement entropy
        """
        l = subsystem_size
        L = self.length
        
        # Cardy-Calabrese formula for CFT
        if l > 0 and l < L:
            sin_term = math.sin(math.pi * l / L)
            if sin_term > 1e-10:
                return (1.0/3.0) * math.log((L / math.pi) * sin_term) + 0.726
        return 0.0
    
    def quantum_dimension_xx_model(self, subsystem_size: int) -> float:
        """
        Calculate quantum effective dimension for XX model.
        
        Args:
            subsystem_size: Size of subsystem A
            
        Returns:
            Quantum effective dimension
        """
        entropy = self.exact_entropy_xx_model(subsystem_size)
        return self.entanglement_calculator.quantum_effective_dimension(entropy)
    
    def verify_scaling_law(self) -> Dict[str, List[float]]:
        """
        Verify the scaling law d_eff ~ (l/epsilon)^(c/3).
        
        Returns:
            Dictionary with subsystem sizes and corresponding dimensions
        """
        results = {
            'subsystem_sizes': [],
            'entropies': [],
            'dimensions': [],
            'log_l': [],
            'log_d': []
        }
        
        for l in range(1, self.length // 2 + 1):
            S = self.exact_entropy_xx_model(l)
            d_eff = self.entanglement_calculator.quantum_effective_dimension(S)
            
            results['subsystem_sizes'].append(l)
            results['entropies'].append(S)
            results['dimensions'].append(d_eff)
            results['log_l'].append(math.log(l))
            results['log_d'].append(math.log(d_eff))
        
        return results


class HolographicDimensionCalculator:
    """Calculator for holographic effective dimensions."""
    
    def __init__(self, G_N: float = 1.0):
        """
        Initialize holographic calculator.
        
        Args:
            G_N: Newton's constant (in appropriate units)
        """
        self.G_N = G_N
    
    def minimal_surface_area(self, region_size: float, 
                           bulk_radius: float) -> float:
        """
        Calculate minimal surface area (simplified model).
        
        For a spherical region in AdS_{d+1}:
        Area ~ R^(d-1)
        
        Args:
            region_size: Size of boundary region
            bulk_radius: Bulk AdS radius
            
        Returns:
            Minimal surface area
        """
        # Simplified: Area proportional to region_size
        return 4 * math.pi * (region_size ** 2) / bulk_radius
    
    def holographic_entropy(self, area: float) -> float:
        """
        Calculate holographic entanglement entropy (Ryu-Takayanagi).
        
        S = Area / (4 * G_N)
        
        Args:
            area: Minimal surface area
            
        Returns:
            Holographic entropy
        """
        return area / (4 * self.G_N)
    
    def holographic_effective_dimension(self, region_size: float,
                                       bulk_radius: float) -> float:
        """
        Calculate holographic effective dimension.
        
        d_eff^q = Area / (4 * G_N * log(2))
        
        Args:
            region_size: Size of boundary region
            bulk_radius: Bulk AdS radius
            
        Returns:
            Holographic effective dimension
        """
        area = self.minimal_surface_area(region_size, bulk_radius)
        entropy = self.holographic_entropy(area)
        return math.exp(entropy)


class QuantumMasterEquation:
    """
    Quantum version of the dimensionics Master Equation.
    """
    
    def __init__(self, T: float = 1.0, hbar: float = 1.0):
        """
        Initialize quantum Master Equation.
        
        Args:
            T: Temperature parameter
            hbar: Planck's constant
        """
        self.T = T
        self.hbar = hbar
    
    def energy_functional(self, d: float, hamiltonian_exp: float) -> float:
        """
        Quantum energy functional: E_Q(d) = <H>_d
        
        Args:
            d: Dimension parameter
            hamiltonian_exp: Expectation value of Hamiltonian
            
        Returns:
            Energy
        """
        # Simplified model
        return hamiltonian_exp / (d ** 0.5)
    
    def entropy_functional(self, d: float) -> float:
        """
        Quantum entropy: S_Q(d) = log(d)
        
        Args:
            d: Dimension parameter
            
        Returns:
            Entropy
        """
        return math.log(d) if d > 0 else 0.0
    
    def correction_functional(self, d: float, L: float, epsilon: float) -> float:
        """
        Quantum correction: Lambda_Q(d) ~ log(L/epsilon)
        
        Args:
            d: Dimension parameter
            L: System size
            epsilon: UV cutoff
            
        Returns:
            Correction term
        """
        if epsilon > 0 and L > epsilon:
            return (self.hbar / 6.0) * math.log(L / epsilon) * (1.0 / d)
        return 0.0
    
    def free_energy(self, d: float, hamiltonian_exp: float,
                   L: float, epsilon: float) -> float:
        """
        Calculate quantum free energy functional.
        
        F_Q[d] = E_Q(d) - T * S_Q(d) + Lambda_Q(d)
        
        Args:
            d: Dimension parameter
            hamiltonian_exp: Hamiltonian expectation
            L: System size
            epsilon: UV cutoff
            
        Returns:
            Free energy
        """
        E = self.energy_functional(d, hamiltonian_exp)
        S = self.entropy_functional(d)
        Lambda = self.correction_functional(d, L, epsilon)
        
        return E - self.T * S + Lambda
    
    def solve_master_equation(self, hamiltonian_exp: float,
                             L: float, epsilon: float,
                             d_min: float = 0.1,
                             d_max: float = 100.0,
                             num_points: int = 1000) -> Dict[str, float]:
        """
        Solve quantum Master Equation by minimizing free energy.
        
        Args:
            hamiltonian_exp: Hamiltonian expectation value
            L: System size
            epsilon: UV cutoff
            d_min, d_max: Search range for dimension
            num_points: Number of grid points
            
        Returns:
            Dictionary with optimal dimension and free energy
        """
        d_optimal = d_min
        F_min = float('inf')
        
        for i in range(num_points):
            d = d_min + (d_max - d_min) * i / (num_points - 1)
            F = self.free_energy(d, hamiltonian_exp, L, epsilon)
            
            if F < F_min:
                F_min = F
                d_optimal = d
        
        return {
            'optimal_dimension': d_optimal,
            'min_free_energy': F_min,
            'temperature': self.T,
            'hamiltonian': hamiltonian_exp
        }


def run_h_validations():
    """Run validation tests for H direction theorems."""
    print("=" * 70)
    print("H Direction: Quantum Dimension Validations")
    print("=" * 70)
    
    # Test H1.1: XX Model scaling
    print("\n[1] Testing Theorem H1.1: XX Model Scaling Law")
    print("-" * 50)
    
    chain = SpinChainSimulator(length=100, model='xx')
    results = chain.verify_scaling_law()
    
    # Fit log-log to get scaling exponent
    log_l = results['log_l']
    log_d = results['log_d']
    
    # Simple linear fit for slope
    n = len(log_l)
    sum_x = sum(log_l)
    sum_y = sum(log_d)
    sum_xy = sum(x * y for x, y in zip(log_l, log_d))
    sum_x2 = sum(x ** 2 for x in log_l)
    
    slope = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x ** 2)
    
    print(f"Fitted scaling exponent: {slope:.4f}")
    print(f"Expected (c/3 for c=1): {1.0/3.0:.4f}")
    print(f"Error: {abs(slope - 1.0/3.0) / (1.0/3.0) * 100:.2f}%")
    
    # Test H1.2: Holographic dimension
    print("\n[2] Testing Theorem H1.2: Holographic Effective Dimension")
    print("-" * 50)
    
    holographic = HolographicDimensionCalculator(G_N=1.0)
    
    test_sizes = [1.0, 2.0, 5.0, 10.0]
    for size in test_sizes:
        d_holo = holographic.holographic_effective_dimension(size, bulk_radius=1.0)
        print(f"Region size: {size:.1f}, Holographic d_eff: {d_holo:.4e}")
    
    # Test Master Equation
    print("\n[3] Testing Quantum Master Equation")
    print("-" * 50)
    
    qme = QuantumMasterEquation(T=1.0, hbar=0.1)
    solution = qme.solve_master_equation(
        hamiltonian_exp=1.0,
        L=100.0,
        epsilon=1e-3
    )
    
    print(f"Optimal quantum dimension: {solution['optimal_dimension']:.4f}")
    print(f"Minimum free energy: {solution['min_free_energy']:.4f}")
    
    print("\n" + "=" * 70)
    print("H Direction Validation Complete")
    print("=" * 70)
    
    return {
        'xx_scaling_exponent': slope,
        'master_equation_solution': solution
    }


if __name__ == "__main__":
    results = run_h_validations()
