"""
Tests for Fisher Information Matrix computation.
"""

import torch
import torch.nn as nn
import numpy as np
import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'code'))

from neural_dimension.core.fisher_information import FisherInformationMatrix


class SimpleModel(nn.Module):
    """Simple model for testing."""
    def __init__(self, input_dim=10, hidden_dim=20, output_dim=2):
        super().__init__()
        self.fc1 = nn.Linear(input_dim, hidden_dim)
        self.fc2 = nn.Linear(hidden_dim, output_dim)
    
    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = self.fc2(x)
        return x


def test_fisher_initialization():
    """Test FisherInformationMatrix initialization."""
    model = SimpleModel()
    fisher_calc = FisherInformationMatrix(model, sigma=1.0)
    
    assert fisher_calc.model is model
    assert fisher_calc.sigma == 1.0
    assert fisher_calc.fisher_matrix is None


def test_diagonal_fisher_shape():
    """Test diagonal Fisher computation returns correct shape."""
    model = SimpleModel()
    fisher_calc = FisherInformationMatrix(model, sigma=1.0)
    
    # Create dummy data
    X = torch.randn(50, 10)
    y = torch.randint(0, 2, (50,))
    dataset = torch.utils.data.TensorDataset(X, y)
    loader = torch.utils.data.DataLoader(dataset, batch_size=10)
    
    fisher_diag = fisher_calc.compute_diagonal_fisher(loader, device='cpu')
    
    # Should be vector of length D (total parameters)
    total_params = sum(p.numel() for p in model.parameters())
    assert fisher_diag.shape[0] == total_params
    assert fisher_diag.dim() == 1


def test_fisher_positive():
    """Test Fisher information is non-negative."""
    model = SimpleModel()
    fisher_calc = FisherInformationMatrix(model, sigma=1.0)
    
    X = torch.randn(50, 10)
    y = torch.randint(0, 2, (50,))
    dataset = torch.utils.data.TensorDataset(X, y)
    loader = torch.utils.data.DataLoader(dataset, batch_size=10)
    
    fisher_diag = fisher_calc.compute_diagonal_fisher(loader, device='cpu')
    
    assert torch.all(fisher_diag >= 0)


def test_eigenvalue_spectrum():
    """Test eigenvalue spectrum computation."""
    model = SimpleModel(input_dim=5, hidden_dim=10, output_dim=2)
    fisher_calc = FisherInformationMatrix(model, sigma=1.0)
    
    # Create a simple Fisher matrix for testing
    D = sum(p.numel() for p in model.parameters())
    fisher_matrix = torch.eye(D) * 2.0  # Simple diagonal matrix
    fisher_calc._fisher_matrix = fisher_matrix
    
    eigenvalues = fisher_calc.compute_spectrum()
    
    assert eigenvalues.shape[0] == D
    assert np.all(eigenvalues >= 0)  # PSD matrix
    assert np.allclose(eigenvalues, 2.0)  # All should be 2.0


def test_effective_rank():
    """Test effective rank computation."""
    model = SimpleModel(input_dim=5, hidden_dim=10, output_dim=2)
    fisher_calc = FisherInformationMatrix(model, sigma=1.0)
    
    # Create Fisher matrix with 3 significant eigenvalues
    D = sum(p.numel() for p in model.parameters())
    eigenvalues = np.zeros(D)
    eigenvalues[:3] = [10.0, 5.0, 2.0]
    eigenvalues[3:] = 0.01  # Small noise
    
    fisher_calc._eigenvalues = eigenvalues
    
    rank_99 = fisher_calc.get_effective_rank(0.99)
    
    # Should capture first 3 eigenvalues
    assert rank_99 >= 3


def test_condition_number():
    """Test condition number computation."""
    model = SimpleModel(input_dim=5, hidden_dim=10, output_dim=2)
    fisher_calc = FisherInformationMatrix(model, sigma=1.0)
    
    # Well-conditioned matrix
    D = sum(p.numel() for p in model.parameters())
    eigenvalues = np.ones(D)
    eigenvalues[0] = 10.0  # Max
    eigenvalues[-1] = 0.1  # Min
    
    fisher_calc._eigenvalues = eigenvalues
    
    cond = fisher_calc.get_condition_number()
    
    assert cond == 100.0  # 10.0 / 0.1


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
