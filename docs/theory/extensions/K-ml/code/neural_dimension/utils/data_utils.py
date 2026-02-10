"""
Data utilities for experiments.
"""

import torch
import numpy as np
from typing import Tuple, Optional
from torch.utils.data import Dataset, DataLoader, TensorDataset, Subset


def create_synthetic_data(n_samples: int,
                         input_dim: int,
                         output_dim: int,
                         noise_std: float = 0.1,
                         seed: Optional[int] = None) -> Tuple[torch.Tensor, torch.Tensor]:
    """
    Create synthetic regression data.
    
    Args:
        n_samples: Number of samples
        input_dim: Input dimension
        output_dim: Output dimension
        noise_std: Noise standard deviation
        seed: Random seed
        
    Returns:
        X, y tensors
    """
    if seed is not None:
        torch.manual_seed(seed)
        np.random.seed(seed)
    
    # Generate random input
    X = torch.randn(n_samples, input_dim)
    
    # Generate random linear transformation
    true_weights = torch.randn(input_dim, output_dim)
    true_bias = torch.randn(output_dim)
    
    # Generate output with noise
    y = X @ true_weights + true_bias + torch.randn(n_samples, output_dim) * noise_std
    
    return X, y


def create_classification_data(n_samples: int,
                              n_features: int,
                              n_classes: int,
                              n_informative: Optional[int] = None,
                              seed: Optional[int] = None) -> Tuple[torch.Tensor, torch.Tensor]:
    """
    Create synthetic classification data.
    
    Args:
        n_samples: Number of samples
        n_features: Number of features
        n_classes: Number of classes
        n_informative: Number of informative features
        seed: Random seed
        
    Returns:
        X, y tensors
    """
    if seed is not None:
        torch.manual_seed(seed)
        np.random.seed(seed)
    
    if n_informative is None:
        n_informative = n_features
    
    # Generate class centers
    centers = torch.randn(n_classes, n_features) * 5
    
    # Assign samples to classes
    samples_per_class = n_samples // n_classes
    X_list = []
    y_list = []
    
    for i in range(n_classes):
        # Generate samples around class center
        X_class = torch.randn(samples_per_class, n_features) + centers[i]
        y_class = torch.full((samples_per_class,), i, dtype=torch.long)
        
        X_list.append(X_class)
        y_list.append(y_class)
    
    X = torch.cat(X_list, dim=0)
    y = torch.cat(y_list, dim=0)
    
    # Shuffle
    perm = torch.randperm(X.shape[0])
    X = X[perm]
    y = y[perm]
    
    return X, y


def split_data(dataset: Dataset,
               train_ratio: float = 0.8,
               val_ratio: float = 0.1,
               seed: int = 42) -> Tuple[Subset, Subset, Subset]:
    """
    Split dataset into train/val/test.
    
    Args:
        dataset: PyTorch dataset
        train_ratio: Training set ratio
        val_ratio: Validation set ratio
        seed: Random seed
        
    Returns:
        train_dataset, val_dataset, test_dataset
    """
    n = len(dataset)
    indices = list(range(n))
    
    # Shuffle
    np.random.seed(seed)
    np.random.shuffle(indices)
    
    # Split
    train_size = int(n * train_ratio)
    val_size = int(n * val_ratio)
    
    train_indices = indices[:train_size]
    val_indices = indices[train_size:train_size + val_size]
    test_indices = indices[train_size + val_size:]
    
    train_dataset = Subset(dataset, train_indices)
    val_dataset = Subset(dataset, val_indices)
    test_dataset = Subset(dataset, test_indices)
    
    return train_dataset, val_dataset, test_dataset


def create_data_loaders(dataset: Dataset,
                       batch_size: int = 128,
                       train_ratio: float = 0.8,
                       val_ratio: float = 0.1,
                       num_workers: int = 0,
                       seed: int = 42) -> Tuple[DataLoader, DataLoader, DataLoader]:
    """
    Create train/val/test data loaders.
    
    Args:
        dataset: PyTorch dataset
        batch_size: Batch size
        train_ratio: Training set ratio
        val_ratio: Validation set ratio
        num_workers: Number of data loading workers
        seed: Random seed
        
    Returns:
        train_loader, val_loader, test_loader
    """
    train_dataset, val_dataset, test_dataset = split_data(
        dataset, train_ratio, val_ratio, seed
    )
    
    train_loader = DataLoader(
        train_dataset, batch_size=batch_size, shuffle=True,
        num_workers=num_workers, pin_memory=True
    )
    val_loader = DataLoader(
        val_dataset, batch_size=batch_size, shuffle=False,
        num_workers=num_workers, pin_memory=True
    )
    test_loader = DataLoader(
        test_dataset, batch_size=batch_size, shuffle=False,
        num_workers=num_workers, pin_memory=True
    )
    
    return train_loader, val_loader, test_loader


def estimate_data_intrinsic_dimension(X: torch.Tensor,
                                     k: int = 10) -> float:
    """
    Estimate intrinsic dimension of data using k-NN distances.
    
    Args:
        X: Data matrix (n_samples, n_features)
        k: Number of nearest neighbors
        
    Returns:
        Estimated intrinsic dimension
    """
    from scipy.spatial.distance import pdist, squareform
    
    # Compute pairwise distances
    distances = squareform(pdist(X.numpy()))
    
    # Get k-th nearest neighbor distance for each point
    knn_distances = np.sort(distances, axis=1)[:, k]
    
    # Estimate dimension using maximum likelihood
    # d ≈ (1 / <log(r/r_k)>) where r_k is k-NN distance
    # Simplified: use correlation dimension estimate
    
    # Sort distances
    sorted_distances = np.sort(knn_distances)
    
    # Linear fit in log-log space
    log_indices = np.log(np.arange(1, len(sorted_distances) + 1))
    log_distances = np.log(sorted_distances + 1e-10)
    
    # Slope gives dimension estimate
    slope = np.polyfit(log_indices, log_distances, 1)[0]
    
    return float(1.0 / slope) if slope != 0 else float(X.shape[1])


def normalize_data(X: torch.Tensor,
                  method: str = 'standard') -> Tuple[torch.Tensor, dict]:
    """
    Normalize data.
    
    Args:
        X: Data tensor
        method: 'standard' (zero mean, unit var) or 'minmax' (0-1)
        
    Returns:
        Normalized data, normalization parameters
    """
    if method == 'standard':
        mean = X.mean(dim=0)
        std = X.std(dim=0) + 1e-8
        X_norm = (X - mean) / std
        params = {'mean': mean, 'std': std, 'method': 'standard'}
        
    elif method == 'minmax':
        min_val = X.min(dim=0)[0]
        max_val = X.max(dim=0)[0]
        range_val = max_val - min_val + 1e-8
        X_norm = (X - min_val) / range_val
        params = {'min': min_val, 'max': max_val, 'method': 'minmax'}
        
    else:
        raise ValueError(f"Unknown normalization method: {method}")
    
    return X_norm, params


def apply_normalization(X: torch.Tensor, params: dict) -> torch.Tensor:
    """
    Apply saved normalization to new data.
    
    Args:
        X: Data tensor
        params: Normalization parameters from normalize_data
        
    Returns:
        Normalized data
    """
    method = params['method']
    
    if method == 'standard':
        return (X - params['mean']) / params['std']
    elif method == 'minmax':
        return (X - params['min']) / (params['max'] - params['min'] + 1e-8)
    else:
        raise ValueError(f"Unknown normalization method: {method}")
