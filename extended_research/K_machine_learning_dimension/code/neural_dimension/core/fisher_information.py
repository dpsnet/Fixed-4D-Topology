"""
Fisher Information Matrix Computation
=====================================

Compute the Fisher Information Matrix for neural networks.
"""

import torch
import torch.nn as nn
import numpy as np
from typing import Optional, Tuple, List


class FisherInformationMatrix:
    """
    Compute and manipulate the Fisher Information Matrix for neural networks.
    
    The Fisher Information Matrix is defined as:
    F_ij = E[∂log p(y|x,θ)/∂θ_i * ∂log p(y|x,θ)/∂θ_j]
    
    For neural networks with Gaussian output noise, this reduces to:
    F_ij = (1/N) * Σ_n (∂ℓ_n/∂θ_i)(∂ℓ_n/∂θ_j)
    
    where ℓ_n is the loss for sample n.
    """
    
    def __init__(self, model: nn.Module, sigma: float = 1.0):
        """
        Initialize Fisher Information calculator.
        
        Args:
            model: PyTorch neural network model
            sigma: Standard deviation of output noise (default: 1.0)
        """
        self.model = model
        self.sigma = sigma
        self._fisher_matrix: Optional[torch.Tensor] = None
        self._eigenvalues: Optional[np.ndarray] = None
        self._eigenvectors: Optional[np.ndarray] = None
        
    def compute_empirical_fisher(self, 
                                 dataloader: torch.utils.data.DataLoader,
                                 device: str = 'cpu') -> torch.Tensor:
        """
        Compute empirical Fisher Information Matrix.
        
        Args:
            dataloader: DataLoader with training data
            device: Computation device ('cpu' or 'cuda')
            
        Returns:
            Fisher Information Matrix (D x D) where D is number of parameters
        """
        self.model.to(device)
        self.model.eval()
        
        # Collect all parameters
        params = [p for p in self.model.parameters() if p.requires_grad]
        param_shapes = [p.shape for p in params]
        param_numel = [p.numel() for p in params]
        D = sum(param_numel)
        
        # Initialize Fisher matrix
        fisher = torch.zeros(D, D, device=device)
        n_samples = 0
        
        for batch_idx, (data, target) in enumerate(dataloader):
            data, target = data.to(device), target.to(device)
            batch_size = data.size(0)
            
            # Compute per-sample gradients
            for i in range(batch_size):
                self.model.zero_grad()
                output = self.model(data[i:i+1])
                
                # Negative log-likelihood for Gaussian
                loss = 0.5 * ((output - target[i:i+1]) ** 2).sum() / (self.sigma ** 2)
                loss.backward()
                
                # Collect gradients
                grad = []
                for p in params:
                    if p.grad is not None:
                        grad.append(p.grad.view(-1))
                    else:
                        grad.append(torch.zeros(p.numel(), device=device))
                grad = torch.cat(grad)
                
                # Outer product
                fisher += torch.outer(grad, grad)
                n_samples += 1
                
        fisher = fisher / n_samples
        self._fisher_matrix = fisher.cpu()
        
        return self._fisher_matrix
    
    def compute_diagonal_fisher(self,
                               dataloader: torch.utils.data.DataLoader,
                               device: str = 'cpu') -> torch.Tensor:
        """
        Compute diagonal approximation of Fisher (more efficient).
        
        Args:
            dataloader: DataLoader with training data
            device: Computation device
            
        Returns:
            Diagonal Fisher (vector of length D)
        """
        self.model.to(device)
        self.model.eval()
        
        params = [p for p in self.model.parameters() if p.requires_grad]
        D = sum(p.numel() for p in params)
        
        fisher_diag = torch.zeros(D, device=device)
        n_samples = 0
        
        for data, target in dataloader:
            data, target = data.to(device), target.to(device)
            
            for i in range(data.size(0)):
                self.model.zero_grad()
                output = self.model(data[i:i+1])
                loss = 0.5 * ((output - target[i:i+1]) ** 2).sum() / (self.sigma ** 2)
                loss.backward()
                
                grad = []
                for p in params:
                    if p.grad is not None:
                        grad.append(p.grad.view(-1))
                    else:
                        grad.append(torch.zeros(p.numel(), device=device))
                grad = torch.cat(grad)
                
                fisher_diag += grad ** 2
                n_samples += 1
        
        fisher_diag = fisher_diag / n_samples
        return fisher_diag.cpu()
    
    def compute_spectrum(self, fisher_matrix: Optional[torch.Tensor] = None) -> np.ndarray:
        """
        Compute eigenvalue spectrum of Fisher matrix.
        
        Args:
            fisher_matrix: Pre-computed Fisher matrix (if None, uses stored)
            
        Returns:
            Eigenvalues in descending order
        """
        if fisher_matrix is None:
            fisher_matrix = self._fisher_matrix
            
        if fisher_matrix is None:
            raise ValueError("Fisher matrix not computed. Call compute_empirical_fisher first.")
        
        # Convert to numpy for eigenvalue computation
        F_np = fisher_matrix.detach().cpu().numpy()
        
        # Compute eigenvalues (for symmetric matrix)
        eigenvalues = np.linalg.eigvalsh(F_np)
        eigenvalues = np.sort(eigenvalues)[::-1]  # Descending
        
        self._eigenvalues = eigenvalues
        return eigenvalues
    
    def get_effective_rank(self, threshold: float = 0.99) -> int:
        """
        Compute effective rank (number of eigenvalues needed for threshold variance).
        
        Args:
            threshold: Cumulative variance threshold (default: 0.99)
            
        Returns:
            Effective rank
        """
        if self._eigenvalues is None:
            self.compute_spectrum()
        
        eigenvalues = self._eigenvalues
        cumsum = np.cumsum(eigenvalues) / np.sum(eigenvalues)
        
        effective_rank = np.searchsorted(cumsum, threshold) + 1
        return int(effective_rank)
    
    def get_condition_number(self) -> float:
        """Compute condition number (max eigenvalue / min non-zero eigenvalue)."""
        if self._eigenvalues is None:
            self.compute_spectrum()
        
        eigenvalues = self._eigenvalues
        non_zero = eigenvalues[eigenvalues > 1e-10]
        
        if len(non_zero) == 0:
            return float('inf')
        
        return non_zero[0] / non_zero[-1]
    
    @property
    def fisher_matrix(self) -> Optional[torch.Tensor]:
        """Get computed Fisher matrix."""
        return self._fisher_matrix
    
    @property
    def eigenvalues(self) -> Optional[np.ndarray]:
        """Get computed eigenvalues."""
        return self._eigenvalues
