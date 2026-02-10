"""
Dimension Dynamics Tracking
===========================

Track effective dimension evolution during training.
"""

import torch
import torch.nn as nn
import numpy as np
from typing import List, Dict, Optional, Callable
import copy


class DimensionTracker:
    """
    Track effective dimension during neural network training.
    
    Monitors d_eff(t) evolution and correlates with training metrics.
    """
    
    def __init__(self, model: nn.Module, compute_frequency: int = 1):
        """
        Initialize dimension tracker.
        
        Args:
            model: Neural network model to track
            compute_frequency: Compute d_eff every N epochs (1 = every epoch)
        """
        self.model = model
        self.compute_frequency = compute_frequency
        self.history = {
            'epoch': [],
            'train_loss': [],
            'test_loss': [],
            'train_acc': [],
            'test_acc': [],
            'd_eff_fisher': [],
            'd_eff_vn': [],
            'd_eff_pr': [],
            'learning_rate': [],
        }
        self._checkpoints = []
        
    def compute_epoch_metrics(self, 
                             epoch: int,
                             train_loader: torch.utils.data.DataLoader,
                             test_loader: Optional[torch.utils.data.DataLoader] = None,
                             loss_fn: Optional[Callable] = None,
                             device: str = 'cpu') -> Dict:
        """
        Compute all metrics for current epoch.
        
        Args:
            epoch: Current epoch number
            train_loader: Training data loader
            test_loader: Test data loader (optional)
            loss_fn: Loss function (default: MSE)
            device: Computation device
            
        Returns:
            Dictionary of metrics
        """
        if loss_fn is None:
            loss_fn = nn.MSELoss()
        
        self.model.eval()
        self.model.to(device)
        
        # Compute losses and accuracies
        train_loss, train_acc = self._evaluate(train_loader, loss_fn, device)
        test_loss, test_acc = None, None
        if test_loader is not None:
            test_loss, test_acc = self._evaluate(test_loader, loss_fn, device)
        
        metrics = {
            'epoch': epoch,
            'train_loss': train_loss,
            'test_loss': test_loss,
            'train_acc': train_acc,
            'test_acc': test_acc,
        }
        
        # Compute effective dimension (if it's time)
        if epoch % self.compute_frequency == 0:
            from .fisher_information import FisherInformationMatrix
            from .effective_dimension import EffectiveDimensionCalculator
            
            fisher_calc = FisherInformationMatrix(self.model, sigma=1.0)
            
            # Use diagonal approximation for efficiency
            fisher_diag = fisher_calc.compute_diagonal_fisher(train_loader, device=device)
            eigenvalues = fisher_diag.numpy()
            eigenvalues = np.sort(eigenvalues)[::-1]
            
            dim_calc = EffectiveDimensionCalculator(fisher_calc)
            
            metrics['d_eff_fisher'] = dim_calc.fisher_participation_ratio(eigenvalues)
            metrics['d_eff_vn'] = dim_calc.von_neumann_dimension(eigenvalues)
            metrics['d_eff_pr'] = dim_calc.fisher_participation_ratio(eigenvalues)
        else:
            # Use previous value or None
            metrics['d_eff_fisher'] = None
            metrics['d_eff_vn'] = None
            metrics['d_eff_pr'] = None
        
        return metrics
    
    def _evaluate(self, 
                  dataloader: torch.utils.data.DataLoader, 
                  loss_fn: Callable,
                  device: str) -> tuple:
        """Evaluate model on dataset."""
        total_loss = 0.0
        correct = 0
        total = 0
        
        with torch.no_grad():
            for data, target in dataloader:
                data, target = data.to(device), target.to(device)
                output = self.model(data)
                
                # Loss
                loss = loss_fn(output, target)
                total_loss += loss.item() * data.size(0)
                
                # Accuracy (for classification)
                if len(target.shape) == 1:  # Class labels
                    pred = output.argmax(dim=1)
                    correct += (pred == target).sum().item()
                    total += target.size(0)
        
        avg_loss = total_loss / len(dataloader.dataset)
        accuracy = correct / total if total > 0 else None
        
        return avg_loss, accuracy
    
    def update(self, metrics: Dict):
        """Update history with new metrics."""
        for key in self.history.keys():
            if key in metrics:
                self.history[key].append(metrics[key])
            else:
                self.history[key].append(None)
    
    def save_checkpoint(self, epoch: int):
        """Save model checkpoint."""
        checkpoint = {
            'epoch': epoch,
            'model_state': copy.deepcopy(self.model.state_dict()),
            'history': copy.deepcopy(self.history),
        }
        self._checkpoints.append(checkpoint)
    
    def get_history(self) -> Dict:
        """Get full training history."""
        return self.history.copy()
    
    def plot_dynamics(self, save_path: Optional[str] = None):
        """
        Plot dimension evolution.
        
        Args:
            save_path: Path to save figure
        """
        import matplotlib.pyplot as plt
        
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        
        epochs = self.history['epoch']
        
        # Plot 1: Loss curves
        ax = axes[0, 0]
        ax.plot(epochs, self.history['train_loss'], 'b-', label='Train Loss')
        if any(x is not None for x in self.history['test_loss']):
            ax.plot(epochs, self.history['test_loss'], 'r-', label='Test Loss')
        ax.set_xlabel('Epoch')
        ax.set_ylabel('Loss')
        ax.set_title('Training Loss')
        ax.legend()
        ax.grid(True, alpha=0.3)
        ax.set_yscale('log')
        
        # Plot 2: Effective dimension
        ax = axes[0, 1]
        d_effs = [d for d in self.history['d_eff_fisher'] if d is not None]
        d_epochs = [e for e, d in zip(epochs, self.history['d_eff_fisher']) if d is not None]
        ax.plot(d_epochs, d_effs, 'g-o', linewidth=2, markersize=4)
        ax.set_xlabel('Epoch')
        ax.set_ylabel('Effective Dimension')
        ax.set_title('Dimension Evolution')
        ax.grid(True, alpha=0.3)
        
        # Plot 3: Dimension vs Loss
        ax = axes[1, 0]
        valid_indices = [i for i, d in enumerate(self.history['d_eff_fisher']) if d is not None]
        if valid_indices:
            d_effs = [self.history['d_eff_fisher'][i] for i in valid_indices]
            losses = [self.history['train_loss'][i] for i in valid_indices]
            ax.scatter(losses, d_effs, c=valid_indices, cmap='viridis', s=50)
            ax.set_xlabel('Training Loss')
            ax.set_ylabel('Effective Dimension')
            ax.set_title('Dimension vs Loss')
            ax.set_xscale('log')
            ax.grid(True, alpha=0.3)
        
        # Plot 4: Accuracy
        ax = axes[1, 1]
        if any(x is not None for x in self.history['train_acc']):
            ax.plot(epochs, self.history['train_acc'], 'b-', label='Train Acc')
        if any(x is not None for x in self.history['test_acc']):
            ax.plot(epochs, self.history['test_acc'], 'r-', label='Test Acc')
        ax.set_xlabel('Epoch')
        ax.set_ylabel('Accuracy')
        ax.set_title('Training Accuracy')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        return fig
    
    def fit_dynamics_model(self) -> Dict:
        """
        Fit theoretical dynamics model to observed data.
        
        Returns:
            Fitted parameters
        """
        # Extract valid data points
        valid_mask = [d is not None for d in self.history['d_eff_fisher']]
        epochs = np.array([self.history['epoch'][i] for i, m in enumerate(valid_mask) if m])
        d_effs = np.array([self.history['d_eff_fisher'][i] for i, m in enumerate(valid_mask) if m])
        losses = np.array([self.history['train_loss'][i] for i, m in enumerate(valid_mask) if m])
        
        # Fit: d_eff = a - b * ln(loss)
        log_losses = np.log(losses)
        coeffs = np.polyfit(log_losses, d_effs, 1)
        
        # Fit: d_eff = d_data - (d_data - d_init) * exp(-c * epoch)
        # (simplified exponential approach)
        
        return {
            'log_linear_coeffs': coeffs,  # [slope, intercept]
            'd_eff_init': d_effs[0],
            'd_eff_final': d_effs[-1],
            'd_data_estimate': np.mean(d_effs[-5:]),  # Average of last 5
        }


class EarlyStoppingByDimension:
    """
    Early stopping based on effective dimension.
    
    Stop when d_eff approaches d_data (optimal complexity).
    """
    
    def __init__(self, target_d: float, patience: int = 5, tolerance: float = 0.1):
        """
        Args:
            target_d: Target effective dimension (d_data)
            patience: Epochs to wait for improvement
            tolerance: Relative tolerance for "close enough"
        """
        self.target_d = target_d
        self.patience = patience
        self.tolerance = tolerance
        self.counter = 0
        self.best_diff = float('inf')
        
    def __call__(self, d_eff: float) -> bool:
        """
        Check if should stop.
        
        Args:
            d_eff: Current effective dimension
            
        Returns:
            True if should stop
        """
        diff = abs(d_eff - self.target_d) / self.target_d
        
        if diff < self.tolerance:
            self.counter += 1
            if self.counter >= self.patience:
                return True
        else:
            self.counter = 0
        
        if diff < self.best_diff:
            self.best_diff = diff
        
        return False
