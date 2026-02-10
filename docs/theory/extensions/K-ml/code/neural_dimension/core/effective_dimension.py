"""
Effective Dimension Computation
===============================

Compute various definitions of effective dimension for neural networks.
"""

import torch
import numpy as np
from typing import Optional, Union
from .fisher_information import FisherInformationMatrix


class EffectiveDimensionCalculator:
    """
    Calculate effective dimension of neural networks using multiple methods.
    
    The effective dimension measures the "true" degrees of freedom in a model,
    accounting for parameter redundancy and correlations.
    """
    
    def __init__(self, fisher_calculator: FisherInformationMatrix):
        """
        Initialize with a FisherInformationMatrix calculator.
        
        Args:
            fisher_calculator: FisherInformationMatrix instance
        """
        self.fisher = fisher_calculator
        
    def fisher_effective_dimension(self, 
                                   fisher_matrix: Optional[torch.Tensor] = None,
                                   epsilon: float = 1e-10) -> float:
        """
        Compute effective dimension using Fisher Information.
        
        d_eff = (tr F)^2 / tr(F^2)
        
        This measures the participation ratio of eigenvalues.
        
        Args:
            fisher_matrix: Fisher matrix (if None, use stored)
            epsilon: Regularization for numerical stability
            
        Returns:
            Effective dimension (float, 1 <= d_eff <= D)
        """
        if fisher_matrix is None:
            fisher_matrix = self.fisher.fisher_matrix
            
        if fisher_matrix is None:
            raise ValueError("Fisher matrix not computed.")
        
        # Add regularization
        F = fisher_matrix + epsilon * torch.eye(fisher_matrix.shape[0])
        
        trace_F = torch.trace(F)
        trace_F2 = torch.trace(F @ F)
        
        d_eff = (trace_F ** 2) / trace_F2
        
        return float(d_eff)
    
    def fisher_participation_ratio(self, eigenvalues: Optional[np.ndarray] = None) -> float:
        """
        Compute participation ratio of Fisher eigenvalues.
        
        PR = (Σ λ_i)^2 / Σ λ_i^2
        
        This is equivalent to fisher_effective_dimension but uses pre-computed eigenvalues.
        
        Args:
            eigenvalues: Eigenvalues of Fisher matrix
            
        Returns:
            Participation ratio
        """
        if eigenvalues is None:
            eigenvalues = self.fisher.eigenvalues
            
        if eigenvalues is None:
            eigenvalues = self.fisher.compute_spectrum()
        
        # Only positive eigenvalues
        lambda_pos = eigenvalues[eigenvalues > 0]
        
        if len(lambda_pos) == 0:
            return 1.0
        
        pr = (np.sum(lambda_pos) ** 2) / np.sum(lambda_pos ** 2)
        return float(pr)
    
    def von_neumann_dimension(self, eigenvalues: Optional[np.ndarray] = None) -> float:
        """
        Compute von Neumann-style effective dimension.
        
        d_vn = exp(-Σ p_i log p_i)
        
        where p_i = λ_i / Σ λ_j
        
        Args:
            eigenvalues: Eigenvalues of Fisher matrix
            
        Returns:
            von Neumann dimension
        """
        if eigenvalues is None:
            eigenvalues = self.fisher.eigenvalues
            
        if eigenvalues is None:
            eigenvalues = self.fisher.compute_spectrum()
        
        lambda_pos = eigenvalues[eigenvalues > 0]
        
        if len(lambda_pos) == 0:
            return 1.0
        
        # Normalize
        p = lambda_pos / np.sum(lambda_pos)
        
        # Entropy
        entropy = -np.sum(p * np.log(p + 1e-15))
        
        d_vn = np.exp(entropy)
        return float(d_vn)
    
    def capacity_dimension(self, 
                          eigenvalues: Optional[np.ndarray] = None,
                          n_samples: int = 1000) -> float:
        """
        Compute capacity dimension (related to model capacity).
        
        d_cap = tr(F) / λ_max
        
        Args:
            eigenvalues: Eigenvalues of Fisher matrix
            n_samples: Number of training samples
            
        Returns:
            Capacity dimension
        """
        if eigenvalues is None:
            eigenvalues = self.fisher.eigenvalues
            
        if eigenvalues is None:
            eigenvalues = self.fisher.compute_spectrum()
        
        lambda_max = eigenvalues[0]
        trace = np.sum(eigenvalues)
        
        d_cap = trace / (lambda_max + 1e-15)
        return float(d_cap)
    
    def compute_all_dimensions(self, n_samples: int = 1000) -> dict:
        """
        Compute all effective dimension measures.
        
        Args:
            n_samples: Number of training samples (for capacity dimension)
            
        Returns:
            Dictionary with all dimension measures
        """
        # Ensure eigenvalues are computed
        eigenvalues = self.fisher.compute_spectrum()
        fisher_matrix = self.fisher.fisher_matrix
        
        results = {
            'fisher_effective_dimension': self.fisher_effective_dimension(fisher_matrix),
            'participation_ratio': self.fisher_participation_ratio(eigenvalues),
            'von_neumann_dimension': self.von_neumann_dimension(eigenvalues),
            'capacity_dimension': self.capacity_dimension(eigenvalues, n_samples),
            'effective_rank_99': self.fisher.get_effective_rank(0.99),
            'effective_rank_95': self.fisher.get_effective_rank(0.95),
            'condition_number': self.fisher.get_condition_number(),
            'total_parameters': len(eigenvalues),
            'non_zero_eigenvalues': int(np.sum(eigenvalues > 1e-10)),
        }
        
        return results
    
    def dimension_reduction_ratio(self) -> float:
        """
        Compute ratio of effective dimension to total parameters.
        
        Returns:
            Reduction ratio (1.0 means no reduction, <1.0 means redundancy)
        """
        d_eff = self.fisher_effective_dimension()
        total_params = self.fisher.fisher_matrix.shape[0]
        
        return d_eff / total_params
