"""
Cross-Direction Analyzer
=========================

Unified analysis framework for K-H-I-J directions.
"""

import torch
import torch.nn as nn
import numpy as np
from typing import Dict, List, Optional
import json


class CrossDirectionAnalyzer:
    """
    Analyze effective dimension across K, H, I, J directions.
    
    Provides unified interface for cross-direction comparison and validation.
    """
    
    def __init__(self, config: Optional[Dict] = None):
        """
        Initialize cross-direction analyzer.
        
        Args:
            config: Configuration dictionary
        """
        self.config = config or {}
        self.results = {
            'K': {},  # ML dimension
            'H': {},  # Quantum dimension
            'I': {},  # Network dimension
            'J': {},  # Percolation dimension
        }
    
    def analyze_K(self, model: nn.Module, data_loader, device='cpu') -> Dict:
        """
        Analyze K direction (ML effective dimension).
        
        Args:
            model: Neural network model
            data_loader: Training data
            device: Computation device
            
        Returns:
            K-direction metrics
        """
        from ..core.fisher_information import FisherInformationMatrix
        from ..core.effective_dimension import EffectiveDimensionCalculator
        
        fisher_calc = FisherInformationMatrix(model, sigma=1.0)
        fisher_diag = fisher_calc.compute_diagonal_fisher(data_loader, device=device)
        eigenvalues = fisher_diag.numpy()
        eigenvalues = np.sort(eigenvalues)[::-1]
        
        dim_calc = EffectiveDimensionCalculator(fisher_calc)
        
        results = {
            'd_eff_fisher': dim_calc.fisher_participation_ratio(eigenvalues),
            'd_eff_vn': dim_calc.von_neumann_dimension(eigenvalues),
            'total_params': sum(p.numel() for p in model.parameters()),
        }
        
        self.results['K'] = results
        return results
    
    def analyze_I(self, graph_adj_matrix: np.ndarray) -> Dict:
        """
        Analyze I direction (network spectral dimension).
        
        Args:
            graph_adj_matrix: Adjacency matrix of the graph
            
        Returns:
            I-direction metrics
        """
        # Compute graph Laplacian
        degree = np.sum(graph_adj_matrix, axis=1)
        laplacian = np.diag(degree) - graph_adj_matrix
        
        # Compute eigenvalues
        eigenvalues = np.linalg.eigvalsh(laplacian)
        eigenvalues = np.sort(eigenvalues)[1:]  # Skip zero eigenvalue
        
        # Spectral dimension estimation
        t_values = np.logspace(-3, 0, 50)
        Z_values = []
        
        for t in t_values:
            Z = np.sum(np.exp(-eigenvalues * t))
            Z_values.append(Z)
        
        # Estimate dimension from slope
        log_t = np.log(t_values)
        log_Z = np.log(Z_values)
        
        slope = np.polyfit(log_t[:10], log_Z[:10], 1)[0]
        d_s = -2 * slope
        
        results = {
            'spectral_dimension': float(d_s),
            'n_nodes': graph_adj_matrix.shape[0],
        }
        
        self.results['I'] = results
        return results
    
    def compute_correspondence(self) -> Dict:
        """
        Compute correspondence between directions.
        
        Returns:
            Correlation analysis
        """
        d_K = self.results['K'].get('d_eff_fisher', None)
        d_I = self.results['I'].get('spectral_dimension', None)
        
        correspondence = {
            'dimensions': {'K': d_K, 'I': d_I},
            'ratios': {},
        }
        
        if d_K is not None and d_I is not None and d_I > 0:
            correspondence['ratios']['K/I'] = d_K / d_I
        
        return correspondence
    
    def generate_report(self, save_path: Optional[str] = None) -> str:
        """
        Generate comprehensive analysis report.
        
        Args:
            save_path: Path to save report
            
        Returns:
            Report string
        """
        report = []
        report.append("=" * 60)
        report.append("K-H-I-J Cross-Direction Analysis Report")
        report.append("=" * 60)
        report.append("")
        
        for direction in ['K', 'H', 'I', 'J']:
            if self.results[direction]:
                report.append(f"\n{direction} Direction:")
                report.append("-" * 40)
                for key, value in self.results[direction].items():
                    if isinstance(value, float):
                        report.append(f"  {key}: {value:.4f}")
                    elif isinstance(value, (int, str)):
                        report.append(f"  {key}: {value}")
        
        report_text = "\n".join(report)
        
        if save_path:
            with open(save_path, 'w') as f:
                f.write(report_text)
        
        return report_text
    
    def save_results(self, path: str):
        """Save all results to JSON."""
        with open(path, 'w') as f:
            json.dump(self.results, f, indent=2)
