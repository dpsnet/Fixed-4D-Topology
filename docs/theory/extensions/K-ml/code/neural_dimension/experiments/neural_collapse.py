"""
Neural Collapse Experiment
===========================

Verify neural collapse phenomenon with dimension analysis.
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
from typing import Dict, Tuple


class NeuralCollapseExperiment:
    """
    Experiment to study neural collapse and its dimension interpretation.
    
    Neural collapse refers to the phenomenon where:
    1. Within-class variability collapses (NC1)
    2. Class means form simplex equiangular tight frame (NC2)
    3. Classifier aligns with class means (NC3)
    """
    
    def __init__(self, model: nn.Module, num_classes: int, feature_dim: int):
        """
        Args:
            model: Neural network (classifier)
            num_classes: Number of classes K
            feature_dim: Dimension of last hidden layer
        """
        self.model = model
        self.K = num_classes
        self.d = feature_dim
        
    def compute_nc1(self, dataloader, device='cpu') -> float:
        """
        Compute within-class variability (NC1).
        
        NC1 = (1/K) * tr(Sigma_W * Sigma_B^(-1))
        
        where Sigma_W is within-class covariance, Sigma_B is between-class covariance.
        
        Returns:
            NC1 metric (lower is better)
        """
        self.model.eval()
        self.model.to(device)
        
        # Collect features and labels
        features_by_class = {k: [] for k in range(self.K)}
        
        with torch.no_grad():
            for data, target in dataloader:
                data = data.to(device)
                # Get features (before last linear layer)
                features = self._get_features(data)
                
                for i, label in enumerate(target):
                    features_by_class[label.item()].append(features[i].cpu().numpy())
        
        # Compute class means
        class_means = {}
        for k in range(self.K):
            if len(features_by_class[k]) > 0:
                class_means[k] = np.mean(features_by_class[k], axis=0)
        
        # Global mean
        all_features = np.concatenate([features_by_class[k] for k in range(self.K) 
                                       if len(features_by_class[k]) > 0])
        global_mean = np.mean(all_features, axis=0)
        
        # Within-class covariance
        Sigma_W = np.zeros((self.d, self.d))
        for k in range(self.K):
            if len(features_by_class[k]) > 0:
                centered = features_by_class[k] - class_means[k]
                Sigma_W += np.dot(centered.T, centered)
        Sigma_W /= len(all_features)
        
        # Between-class covariance
        Sigma_B = np.zeros((self.d, self.d))
        for k in range(self.K):
            if k in class_means:
                diff = (class_means[k] - global_mean).reshape(-1, 1)
                Sigma_B += len(features_by_class[k]) * np.dot(diff, diff.T)
        Sigma_B /= len(all_features)
        
        # NC1 = tr(Sigma_W @ Sigma_B^(-1)) / K
        try:
            Sigma_B_inv = np.linalg.inv(Sigma_B + 1e-6 * np.eye(self.d))
            nc1 = np.trace(Sigma_W @ Sigma_B_inv) / self.K
        except np.linalg.LinAlgError:
            nc1 = float('inf')
        
        return float(nc1)
    
    def compute_nc2(self, dataloader, device='cpu') -> float:
        """
        Compute ETF (Equiangular Tight Frame) deviation (NC2).
        
        Returns:
            NC2 metric (lower is better, 0 means perfect ETF)
        """
        self.model.eval()
        self.model.to(device)
        
        # Get classifier weights
        classifier_weight = self.model.fc2.weight.data.cpu().numpy()  # (K, d)
        
        # Normalize
        W = classifier_weight / (np.linalg.norm(classifier_weight, axis=1, keepdims=True) + 1e-10)
        
        # Compute Gram matrix
        G = np.dot(W, W.T)  # (K, K)
        
        # For perfect ETF: G = (K/(K-1)) * I - (1/(K-1)) * 11^T
        # Off-diagonal should be -1/(K-1), diagonal should be 1
        
        ideal_off_diag = -1.0 / (self.K - 1)
        
        off_diag_mask = ~np.eye(self.K, dtype=bool)
        nc2 = np.mean((G[off_diag_mask] - ideal_off_diag) ** 2)
        
        return float(nc2)
    
    def compute_nc3(self, dataloader, device='cpu') -> float:
        """
        Compute self-duality (NC3): alignment between classifier and features.
        
        Returns:
            NC3 metric (higher is better, 1 means perfect alignment)
        """
        self.model.eval()
        self.model.to(device)
        
        # Get classifier weights
        W = self.model.fc2.weight.data.cpu().numpy()  # (K, d)
        
        # Compute class means from data
        class_means = self._compute_class_means(dataloader, device)
        
        # Normalize
        W_norm = W / (np.linalg.norm(W, axis=1, keepdims=True) + 1e-10)
        H_norm = class_means / (np.linalg.norm(class_means, axis=1, keepdims=True) + 1e-10)
        
        # Correlation
        correlations = np.sum(W_norm * H_norm, axis=1)
        nc3 = np.mean(correlations)
        
        return float(nc3)
    
    def compute_effective_dimension(self, dataloader, device='cpu') -> float:
        """
        Compute effective dimension of last hidden layer.
        
        Returns:
            d_eff
        """
        from ..core.fisher_information import FisherInformationMatrix
        from ..core.effective_dimension import EffectiveDimensionCalculator
        
        fisher_calc = FisherInformationMatrix(self.model, sigma=1.0)
        fisher_diag = fisher_calc.compute_diagonal_fisher(dataloader, device=device)
        eigenvalues = fisher_diag.numpy()
        eigenvalues = np.sort(eigenvalues)[::-1]
        
        dim_calc = EffectiveDimensionCalculator(fisher_calc)
        d_eff = dim_calc.fisher_participation_ratio(eigenvalues)
        
        return float(d_eff)
    
    def _get_features(self, x):
        """Extract features before final layer."""
        # Assumes model has structure: fc1 -> relu -> fc2
        x = x.view(x.size(0), -1)
        x = F.relu(self.model.fc1(x))
        return x
    
    def _compute_class_means(self, dataloader, device):
        """Compute class means in feature space."""
        class_features = {k: [] for k in range(self.K)}
        
        with torch.no_grad():
            for data, target in dataloader:
                data = data.to(device)
                features = self._get_features(data)
                
                for i, label in enumerate(target):
                    class_features[label.item()].append(features[i].cpu().numpy())
        
        class_means = np.zeros((self.K, self.d))
        for k in range(self.K):
            if len(class_features[k]) > 0:
                class_means[k] = np.mean(class_features[k], axis=0)
        
        return class_means
    
    def run_experiment(self, train_loader, test_loader, epochs, 
                      optimizer_fn, loss_fn, device='cpu') -> Dict:
        """
        Run training and track NC metrics and dimension.
        
        Returns:
            History of NC1, NC2, NC3, d_eff over training
        """
        history = {
            'epoch': [],
            'nc1': [],
            'nc2': [],
            'nc3': [],
            'd_eff': [],
            'train_acc': [],
            'test_acc': [],
        }
        
        self.model.to(device)
        optimizer = optimizer_fn(self.model.parameters())
        
        for epoch in range(epochs):
            # Training
            self.model.train()
            for data, target in train_loader:
                data, target = data.to(device), target.to(device)
                
                optimizer.zero_grad()
                output = self.model(data)
                loss = loss_fn(output, target)
                loss.backward()
                optimizer.step()
            
            # Evaluation
            if epoch % 10 == 0 or epoch == epochs - 1:
                nc1 = self.compute_nc1(train_loader, device)
                nc2 = self.compute_nc2(train_loader, device)
                nc3 = self.compute_nc3(train_loader, device)
                d_eff = self.compute_effective_dimension(train_loader, device)
                
                train_acc = self._compute_accuracy(train_loader, device)
                test_acc = self._compute_accuracy(test_loader, device)
                
                history['epoch'].append(epoch)
                history['nc1'].append(nc1)
                history['nc2'].append(nc2)
                history['nc3'].append(nc3)
                history['d_eff'].append(d_eff)
                history['train_acc'].append(train_acc)
                history['test_acc'].append(test_acc)
                
                print(f"Epoch {epoch}: NC1={nc1:.4f}, NC2={nc2:.4f}, "
                      f"NC3={nc3:.4f}, d_eff={d_eff:.2f}, "
                      f"Test Acc={test_acc:.4f}")
        
        return history
    
    def _compute_accuracy(self, dataloader, device):
        """Compute accuracy."""
        self.model.eval()
        correct = 0
        total = 0
        
        with torch.no_grad():
            for data, target in dataloader:
                data, target = data.to(device), target.to(device)
                output = self.model(data)
                pred = output.argmax(dim=1)
                correct += (pred == target).sum().item()
                total += target.size(0)
        
        return correct / total
