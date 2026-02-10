"""
Double Descent Experiment
==========================

Verify double descent phenomenon with dimension analysis.
"""

import torch
import torch.nn as nn
import numpy as np
from typing import Dict, List
import copy


class DoubleDescentExperiment:
    """
    Experiment to verify double descent with effective dimension.
    
    Tests the hypothesis that double descent occurs at d_eff ≈ n.
    """
    
    def __init__(self, model_fn, width_range: List[int], 
                 train_loader, test_loader, device='cpu'):
        """
        Args:
            model_fn: Function that creates model given width
            width_range: List of widths to test
            train_loader: Training data
            test_loader: Test data
            device: Device
        """
        self.model_fn = model_fn
        self.width_range = width_range
        self.train_loader = train_loader
        self.test_loader = test_loader
        self.device = device
        
        self.results = {
            'widths': [],
            'train_errors': [],
            'test_errors': [],
            'd_effs': [],
            'num_params': [],
        }
    
    def run(self, epochs: int = 100, lr: float = 0.01) -> Dict:
        """Run double descent experiment."""
        from ..core.fisher_information import FisherInformationMatrix
        from ..core.effective_dimension import EffectiveDimensionCalculator
        
        n_samples = len(self.train_loader.dataset)
        print(f"Training set size: {n_samples}")
        
        for width in self.width_range:
            print(f"\nTesting width: {width}")
            
            # Create model
            model = self.model_fn(width).to(self.device)
            total_params = sum(p.numel() for p in model.parameters())
            
            # Train
            train_err, test_err = self._train_model(model, epochs, lr)
            
            # Compute effective dimension
            fisher_calc = FisherInformationMatrix(model, sigma=1.0)
            fisher_diag = fisher_calc.compute_diagonal_fisher(
                self.train_loader, device=self.device)
            eigenvalues = fisher_diag.numpy()
            eigenvalues = np.sort(eigenvalues)[::-1]
            
            dim_calc = EffectiveDimensionCalculator(fisher_calc)
            d_eff = dim_calc.fisher_participation_ratio(eigenvalues)
            
            # Record
            self.results['widths'].append(width)
            self.results['train_errors'].append(train_err)
            self.results['test_errors'].append(test_err)
            self.results['d_effs'].append(d_eff)
            self.results['num_params'].append(total_params)
            
            print(f"  Params: {total_params}, d_eff: {d_eff:.2f}")
            print(f"  Train error: {train_err:.4f}, Test error: {test_err:.4f}")
            
            # Check if we're near interpolation threshold
            if abs(d_eff - n_samples) / n_samples < 0.2:
                print(f"  *** Near interpolation threshold (d_eff ≈ n) ***")
        
        return self.results
    
    def _train_model(self, model, epochs, lr):
        """Train a model and return errors."""
        optimizer = torch.optim.SGD(model.parameters(), lr=lr, momentum=0.9)
        loss_fn = nn.CrossEntropyLoss()
        
        # Training
        for epoch in range(epochs):
            model.train()
            for data, target in self.train_loader:
                data, target = data.to(self.device), target.to(self.device)
                optimizer.zero_grad()
                output = model(data)
                loss = loss_fn(output, target)
                loss.backward()
                optimizer.step()
        
        # Evaluate
        model.eval()
        train_correct, train_total = 0, 0
        test_correct, test_total = 0, 0
        
        with torch.no_grad():
            # Train set
            for data, target in self.train_loader:
                data, target = data.to(self.device), target.to(self.device)
                output = model(data)
                pred = output.argmax(dim=1)
                train_correct += (pred == target).sum().item()
                train_total += target.size(0)
            
            # Test set
            for data, target in self.test_loader:
                data, target = data.to(self.device), target.to(self.device)
                output = model(data)
                pred = output.argmax(dim=1)
                test_correct += (pred == target).sum().item()
                test_total += target.size(0)
        
        train_error = 1 - train_correct / train_total
        test_error = 1 - test_correct / test_total
        
        return train_error, test_error
    
    def plot_results(self, save_path=None):
        """Plot double descent curves."""
        from ..visualization.dimension_plots import plot_double_descent
        
        return plot_double_descent(
            self.results['num_params'],
            self.results['train_errors'],
            self.results['test_errors'],
            self.results['d_effs'],
            save_path=save_path
        )
