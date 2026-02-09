"""
Tests for effective dimension computation.
"""

import torch
import numpy as np
import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'code'))

from neural_dimension.core.effective_dimension import EffectiveDimensionCalculator
from neural_dimension.core.fisher_information import FisherInformationMatrix


class MockFisherCalc:
    """Mock Fisher calculator for testing."""
    def __init__(self, eigenvalues):
        self._eigenvalues = np.array(eigenvalues)
        self._fisher_matrix = torch.eye(len(eigenvalues))
    
    @property
    def eigenvalues(self):
        return self._eigenvalues
    
    @property
    def fisher_matrix(self):
        return self._fisher_matrix


def test_fisher_effective_dimension_identity():
    """Test d_eff = D for identity Fisher matrix."""
    D = 10
    eigenvalues = np.ones(D)  # All equal
    mock_calc = MockFisherCalc(eigenvalues)
    
    dim_calc = EffectiveDimensionCalculator(mock_calc)
    d_eff = dim_calc.fisher_participation_ratio(eigenvalues)
    
    assert np.isclose(d_eff, D, rtol=0.01)


def test_fisher_effective_dimension_rank_one():
    """Test d_eff = 1 for rank-one Fisher matrix."""
    D = 10
    eigenvalues = np.zeros(D)
    eigenvalues[0] = 10.0  # Only one non-zero
    mock_calc = MockFisherCalc(eigenvalues)
    
    dim_calc = EffectiveDimensionCalculator(mock_calc)
    d_eff = dim_calc.fisher_participation_ratio(eigenvalues)
    
    assert np.isclose(d_eff, 1.0, rtol=0.01)


def test_participation_ratio_bounds():
    """Test that 1 <= PR <= D."""
    D = 20
    
    # Random eigenvalues
    eigenvalues = np.random.exponential(scale=1.0, size=D)
    eigenvalues = np.sort(eigenvalues)[::-1]
    
    mock_calc = MockFisherCalc(eigenvalues)
    dim_calc = EffectiveDimensionCalculator(mock_calc)
    pr = dim_calc.fisher_participation_ratio(eigenvalues)
    
    assert 1.0 <= pr <= D


def test_von_neumann_dimension():
    """Test von Neumann dimension computation."""
    # Uniform distribution
    D = 10
    eigenvalues = np.ones(D)
    mock_calc = MockFisherCalc(eigenvalues)
    
    dim_calc = EffectiveDimensionCalculator(mock_calc)
    d_vn = dim_calc.von_neumann_dimension(eigenvalues)
    
    # For uniform, should be D
    assert np.isclose(d_vn, D, rtol=0.01)


def test_dimension_reduction_ratio():
    """Test dimension reduction ratio."""
    D = 100
    # d_eff = 50
    eigenvalues = np.zeros(D)
    eigenvalues[:50] = 2.0
    eigenvalues[50:] = 0.5
    
    mock_calc = MockFisherCalc(eigenvalues)
    mock_calc._fisher_matrix = torch.eye(D)
    dim_calc = EffectiveDimensionCalculator(mock_calc)
    
    # Manually set for test
    from unittest.mock import patch
    with patch.object(dim_calc, 'fisher_effective_dimension', return_value=50.0):
        ratio = dim_calc.dimension_reduction_ratio()
        assert ratio == 0.5


def test_compute_all_dimensions():
    """Test that compute_all_dimensions returns all metrics."""
    D = 10
    eigenvalues = np.random.exponential(scale=1.0, size=D)
    mock_calc = MockFisherCalc(eigenvalues)
    mock_calc._fisher_matrix = torch.eye(D)
    
    dim_calc = EffectiveDimensionCalculator(mock_calc)
    
    with patch.object(dim_calc, 'fisher_participation_ratio', return_value=5.0), \
         patch.object(dim_calc, 'von_neumann_dimension', return_value=4.5), \
         patch.object(dim_calc, 'capacity_dimension', return_value=6.0):
        
        results = dim_calc.compute_all_dimensions(n_samples=100)
        
        assert 'fisher_effective_dimension' in results
        assert 'participation_ratio' in results
        assert 'von_neumann_dimension' in results
        assert 'capacity_dimension' in results
        assert 'total_parameters' in results


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
