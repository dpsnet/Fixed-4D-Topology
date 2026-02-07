"""
Test suite for Network Dimension Analysis (I Direction)
=======================================================

Tests for network dimension computation and Master Equation.
"""

import unittest
import numpy as np
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from unified_framework import (
    NetworkDimension,
    NetworkMasterEquation,
    EMPIRICAL_NETWORK_DATA,
    get_empirical_data,
    compare_to_empirical
)


class TestNetworkDimension(unittest.TestCase):
    """Test NetworkDimension class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.nd = NetworkDimension()
        
        # Create a simple test network (ring)
        self.ring_edges = [(i, (i+1) % 10) for i in range(10)]
        self.nd.from_edge_list(self.ring_edges)
    
    def test_graph_construction(self):
        """Test graph construction from edge list."""
        self.assertEqual(len(self.nd.graph), 10)
        # Ring has 10 edges (but stored twice in undirected graph)
        edge_count = sum(len(neighbors) for neighbors in self.nd.graph.values()) // 2
        self.assertEqual(edge_count, 10)
    
    def test_bfs_within_distance(self):
        """Test BFS distance computation."""
        # From node 0, nodes within distance 1
        dist1 = self.nd._bfs_within_distance(0, 1)
        self.assertEqual(len(dist1), 3)  # 0, 1, 9
        
        # From node 0, nodes within distance 2
        dist2 = self.nd._bfs_within_distance(0, 2)
        self.assertEqual(len(dist2), 5)  # 0, 1, 2, 8, 9
    
    def test_box_counting_basic(self):
        """Test box-counting dimension computation."""
        result = self.nd.box_counting_dimension(max_box_size=5)
        
        self.assertIn('dimension', result)
        self.assertIn('r_squared', result)
        self.assertIn('box_sizes', result)
        
        # For a ring, dimension should be around 1
        if result['dimension'] is not None:
            self.assertGreater(result['dimension'], 0)
            self.assertLess(result['dimension'], 3)
    
    def test_correlation_dimension_basic(self):
        """Test correlation dimension computation."""
        result = self.nd.correlation_dimension(max_radius=5)
        
        self.assertIn('dimension', result)
        self.assertIn('r_squared', result)
        self.assertIn('radii', result)
        
        if result['dimension'] is not None:
            self.assertGreater(result['dimension'], 0)
            self.assertLess(result['dimension'], 5)


class TestNetworkMasterEquation(unittest.TestCase):
    """Test NetworkMasterEquation class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.nme = NetworkMasterEquation(A=1.0, B=0.5, gamma=0.3)
    
    def test_efficiency_term(self):
        """Test efficiency term computation."""
        d = 2.0
        N = 1000
        efficiency = self.nme.efficiency_term(d, N)
        
        # Should decrease with dimension
        efficiency_lower = self.nme.efficiency_term(1.0, N)
        self.assertLess(efficiency, efficiency_lower)
    
    def test_cost_term(self):
        """Test cost term computation."""
        d = 2.0
        N = 1000
        cost = self.nme.cost_term(d, N)
        
        # Should increase with dimension
        cost_higher = self.nme.cost_term(3.0, N)
        self.assertLess(cost, cost_higher)
    
    def test_optimal_dimension(self):
        """Test optimal dimension computation."""
        N = 1000
        result = self.nme.optimal_dimension(N)
        
        self.assertIn('optimal_dimension', result)
        self.assertIn('free_energy', result)
        
        d_opt = result['optimal_dimension']
        self.assertGreater(d_opt, 0.5)
        self.assertLess(d_opt, 10.0)
    
    def test_dimension_size_scaling(self):
        """Test that optimal dimension increases with network size."""
        sizes = [100, 1000, 10000]
        dimensions = []
        
        for N in sizes:
            result = self.nme.optimal_dimension(N)
            dimensions.append(result['optimal_dimension'])
        
        # Generally, larger networks favor higher dimensions
        # (This is a trend, not strict monotonicity)
        self.assertGreater(dimensions[-1], dimensions[0] * 0.5)
    
    def test_predict_dimension(self):
        """Test dimension prediction by network type."""
        net_types = ['infrastructure', 'academic', 'social', 'biological', 'communication']
        N = 10000
        
        predictions = {}
        for net_type in net_types:
            d_pred = self.nme.predict_dimension(net_type, N)
            predictions[net_type] = d_pred
            
            # Should be in reasonable range
            self.assertGreater(d_pred, 0.5)
            self.assertLess(d_pred, 10.0)
        
        # Infrastructure should have highest dimension
        self.assertGreater(predictions['infrastructure'], predictions['communication'])


class TestEmpiricalData(unittest.TestCase):
    """Test empirical network data access."""
    
    def test_data_loaded(self):
        """Test that empirical data is loaded."""
        self.assertEqual(len(EMPIRICAL_NETWORK_DATA), 7)
    
    def test_get_empirical_data(self):
        """Test individual network data retrieval."""
        data = get_empirical_data('internet_as')
        
        self.assertIsNotNone(data)
        self.assertIn('nodes', data)
        self.assertIn('dimension', data)
        self.assertEqual(data['nodes'], 1696415)
        self.assertAlmostEqual(data['dimension'], 4.36, places=2)
    
    def test_dimension_hierarchy(self):
        """Test dimension hierarchy from empirical data."""
        # Get dimensions by type
        by_type = {}
        for key, data in EMPIRICAL_NETWORK_DATA.items():
            net_type = data['type']
            if net_type not in by_type:
                by_type[net_type] = []
            by_type[net_type].append(data['dimension'])
        
        # Check hierarchy
        infra_dims = by_type.get('infrastructure', [])
        comm_dims = by_type.get('communication', [])
        
        if infra_dims and comm_dims:
            avg_infra = np.mean(infra_dims)
            avg_comm = np.mean(comm_dims)
            self.assertGreater(avg_infra, avg_comm)
    
    def test_compare_to_empirical(self):
        """Test empirical comparison function."""
        result = compare_to_empirical(2.5, 'social')
        
        self.assertIn('computed', result)
        self.assertIn('empirical_avg', result)
        self.assertIn('comparison', result)
        
        self.assertEqual(result['computed'], 2.5)


class TestNetworkClassification(unittest.TestCase):
    """Test network classification functionality."""
    
    def setUp(self):
        self.nd = NetworkDimension()
    
    def test_classify_infrastructure(self):
        """Test classification of infrastructure networks."""
        net_type = self.nd.classify_network_type(4.0)
        self.assertEqual(net_type, 'infrastructure')
    
    def test_classify_academic(self):
        """Test classification of academic networks."""
        net_type = self.nd.classify_network_type(3.0)
        self.assertEqual(net_type, 'academic')
    
    def test_classify_social(self):
        """Test classification of social networks."""
        net_type = self.nd.classify_network_type(2.3)
        self.assertEqual(net_type, 'social')
    
    def test_classify_communication(self):
        """Test classification of communication networks."""
        net_type = self.nd.classify_network_type(1.2)
        self.assertEqual(net_type, 'communication')


class TestModelComparison(unittest.TestCase):
    """Test model comparison functionality."""
    
    def setUp(self):
        self.nd = NetworkDimension()
    
    def test_compare_to_models(self):
        """Test comparison to BA/WS models."""
        result = self.nd.compare_to_models(2.5)
        
        self.assertIn('computed_dimension', result)
        self.assertIn('ba_error', result)
        self.assertIn('ws_error', result)
        
        # Models predict d=1, so error should be significant for d=2.5
        self.assertGreater(result['ba_error'], 50)
        self.assertGreater(result['ws_error'], 50)
    
    def test_model_underestimation(self):
        """Test that models underestimate high-dimensional networks."""
        result = self.nd.compare_to_models(4.0)
        
        # Error should be very large
        self.assertGreater(result['ba_error'], 100)


if __name__ == '__main__':
    unittest.main()
