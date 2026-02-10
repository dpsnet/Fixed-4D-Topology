"""
Lottery Ticket Hypothesis Implementation
========================================

Implementation of the Lottery Ticket Hypothesis with effective dimension analysis.
"""

import torch
import torch.nn as nn
import copy
from typing import Dict, List
import numpy as np


class LotteryTicketNetwork:
    """
    Implements the Lottery Ticket Hypothesis with dimension tracking.
    
    Finds sparse subnetworks (winning tickets) that can train in isolation
    to comparable accuracy as the full network.
    """
    
    def __init__(self, model: nn.Module, pruning_ratio: float = 0.2):
        """
        Initialize Lottery Ticket experiment.
        
        Args:
            model: Base neural network
            pruning_ratio: Fraction of weights to prune each iteration
        """
        self.model = model
        self.pruning_ratio = pruning_ratio
        self.initial_state = copy.deepcopy(model.state_dict())
        self.masks = {}
        self.history = {
            'sparsity': [],
            'train_acc': [],
            'test_acc': [],
            'd_eff': [],
        }
        self._init_masks()
    
    def _init_masks(self):
        """Initialize pruning masks (all ones)."""
        for name, param in self.model.named_parameters():
            if 'weight' in name:
                self.masks[name] = torch.ones_like(param.data)
    
    def reset_to_initial(self):
        """Reset weights to initial random values (keeping mask)."""
        current_state = self.model.state_dict()
        for name, param in self.initial_state.items():
            if name in current_state:
                current_state[name].copy_(param)
        self.apply_mask()
    
    def apply_mask(self):
        """Apply pruning mask to model weights."""
        for name, param in self.model.named_parameters():
            if name in self.masks:
                param.data *= self.masks[name]
    
    def prune_by_magnitude(self, layerwise: bool = True):
        """
        Prune weights by magnitude (Iterative Magnitude Pruning).
        
        Args:
            layerwise: If True, prune each layer separately
        """
        if layerwise:
            for name, param in self.model.named_parameters():
                if name not in self.masks or 'weight' not in name:
                    continue
                
                weight = param.data.abs()
                mask = self.masks[name]
                alive = weight[mask > 0]
                
                if len(alive) == 0:
                    continue
                
                k = int(self.pruning_ratio * len(alive))
                if k == 0:
                    continue
                
                threshold = torch.kthvalue(alive, k).values
                self.masks[name] = (weight > threshold).float() * mask
        else:
            # Global pruning
            all_weights = []
            for name, param in self.model.named_parameters():
                if name in self.masks and 'weight' in name:
                    alive = param.data.abs()[self.masks[name] > 0]
                    all_weights.append(alive)
            
            if len(all_weights) == 0:
                return
            
            all_weights = torch.cat(all_weights)
            k = int(self.pruning_ratio * len(all_weights))
            if k == 0:
                return
            
            threshold = torch.kthvalue(all_weights, k).values
            
            for name, param in self.model.named_parameters():
                if name in self.masks and 'weight' in name:
                    self.masks[name] = (param.data.abs() > threshold).float() * self.masks[name]
        
        self.apply_mask()
    
    def get_sparsity(self) -> float:
        """Compute overall sparsity."""
        total = 0
        zeros = 0
        for name, param in self.model.named_parameters():
            if name in self.masks:
                total += param.numel()
                zeros += (self.masks[name] == 0).sum().item()
        return zeros / total if total > 0 else 0.0
    
    def get_remaining_parameters(self) -> int:
        """Get number of non-zero parameters."""
        total = 0
        for name, param in self.model.named_parameters():
            if name in self.masks:
                total += (self.masks[name] > 0).sum().item()
        return total
    
    def run_imp_experiment(self,
                          train_loader,
                          test_loader,
                          pruning_iterations: int = 10,
                          train_epochs: int = 30,
                          device: str = 'cpu') -> Dict:
        """
        Run Iterative Magnitude Pruning (IMP) experiment.
        """
        from ..core.fisher_information import FisherInformationMatrix
        from ..core.effective_dimension import EffectiveDimensionCalculator
        
        optimizer_fn = lambda params: torch.optim.SGD(params, lr=0.01, momentum=0.9)
        loss_fn = nn.CrossEntropyLoss()
        
        results = {
            'sparsity': [],
            'final_test_acc': [],
            'd_eff': [],
            'remaining_params': [],
        }
        
        for iteration in range(pruning_iterations + 1):
            print(f"IMP Iteration {iteration}/{pruning_iterations}")
            
            self.reset_to_initial()
            
            # Train (simplified)
            self.model.to(device)
            optimizer = optimizer_fn(self.model.parameters())
            
            for epoch in range(train_epochs):
                self.model.train()
                for data, target in train_loader:
                    data, target = data.to(device), target.to(device)
                    optimizer.zero_grad()
                    output = self.model(data)
                    loss = loss_fn(output, target)
                    loss.backward()
                    
                    # Apply mask to gradients
                    for name, param in self.model.named_parameters():
                        if name in self.masks and param.grad is not None:
                            param.grad *= self.masks[name]
                    
                    optimizer.step()
                    self.apply_mask()
            
            # Evaluate
            self.model.eval()
            test_correct = 0
            test_total = 0
            
            with torch.no_grad():
                for data, target in test_loader:
                    data, target = data.to(device), target.to(device)
                    output = self.model(data)
                    pred = output.argmax(dim=1)
                    test_correct += (pred == target).sum().item()
                    test_total += target.size(0)
            
            test_acc = test_correct / test_total
            
            # Compute dimension
            fisher_calc = FisherInformationMatrix(self.model, sigma=1.0)
            fisher_diag = fisher_calc.compute_diagonal_fisher(train_loader, device=device)
            eigenvalues = fisher_diag.numpy()
            eigenvalues = np.sort(eigenvalues)[::-1]
            
            dim_calc = EffectiveDimensionCalculator(fisher_calc)
            d_eff = dim_calc.fisher_participation_ratio(eigenvalues)
            
            # Record
            sparsity = self.get_sparsity()
            remaining = self.get_remaining_parameters()
            
            results['sparsity'].append(sparsity)
            results['final_test_acc'].append(test_acc)
            results['d_eff'].append(d_eff)
            results['remaining_params'].append(remaining)
            
            print(f"  Sparsity: {sparsity:.4f}, Acc: {test_acc:.4f}, d_eff: {d_eff:.2f}")
            
            # Prune for next iteration
            if iteration < pruning_iterations:
                self.prune_by_magnitude(layerwise=True)
        
        return results
