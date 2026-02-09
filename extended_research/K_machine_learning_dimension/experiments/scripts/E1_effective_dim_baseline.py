"""
E1: Effective Dimension Baseline Measurement
=============================================

Measure effective dimensions of standard architectures.
"""

import os
import sys
import json
import torch
import torch.nn as nn
import torchvision
import torchvision.transforms as transforms
from torch.utils.data import DataLoader
import numpy as np

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'code'))

from neural_dimension import FisherInformationMatrix, EffectiveDimensionCalculator
from neural_dimension.models import TwoLayerMLP, SimpleConvNet

# Configuration
SEED = 42
BATCH_SIZE = 128
DEVICE = 'cuda' if torch.cuda.is_available() else 'cpu'
RESULTS_DIR = os.path.join(os.path.dirname(__file__), '..', 'results', 'effective_dim')


def setup_data(dataset_name='MNIST'):
    """Setup dataset."""
    if dataset_name == 'MNIST':
        transform = transforms.Compose([
            transforms.ToTensor(),
            transforms.Normalize((0.1307,), (0.3081,))
        ])
        train_dataset = torchvision.datasets.MNIST(
            root='./data', train=True, download=True, transform=transform)
        test_dataset = torchvision.datasets.MNIST(
            root='./data', train=False, download=True, transform=transform)
    else:
        raise ValueError(f"Unknown dataset: {dataset_name}")
    
    train_loader = DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True)
    test_loader = DataLoader(test_dataset, batch_size=BATCH_SIZE, shuffle=False)
    
    return train_loader, test_loader


def measure_model(model, train_loader, model_name):
    """Measure effective dimension of a model."""
    print(f"\nMeasuring: {model_name}")
    
    model = model.to(DEVICE)
    total_params = sum(p.numel() for p in model.parameters())
    print(f"Total parameters: {total_params:,}")
    
    # Compute Fisher Information
    print("Computing Fisher Information...")
    fisher_calc = FisherInformationMatrix(model, sigma=1.0)
    fisher_diag = fisher_calc.compute_diagonal_fisher(train_loader, device=DEVICE)
    
    # Compute eigenvalues
    eigenvalues = fisher_diag.numpy()
    eigenvalues = np.sort(eigenvalues)[::-1]
    
    # Compute effective dimension
    dim_calc = EffectiveDimensionCalculator(fisher_calc)
    d_eff_pr = dim_calc.fisher_participation_ratio(eigenvalues)
    
    results = {
        'model_name': model_name,
        'total_parameters': int(total_params),
        'fisher_effective_dimension': float(d_eff_pr),
        'reduction_ratio': float(d_eff_pr / total_params),
    }
    
    print(f"  d_eff: {d_eff_pr:.2f}, Ratio: {d_eff_pr/total_params:.4f}")
    
    return results, eigenvalues


def main():
    """Main experiment."""
    torch.manual_seed(SEED)
    np.random.seed(SEED)
    os.makedirs(RESULTS_DIR, exist_ok=True)
    
    print(f"Device: {DEVICE}")
    
    # Experiments
    train_loader, _ = setup_data('MNIST')
    
    models = [
        ('MLP_128', TwoLayerMLP(hidden_dim=128)),
        ('MLP_512', TwoLayerMLP(hidden_dim=512)),
    ]
    
    all_results = {}
    for name, model in models:
        results, eigenvalues = measure_model(model, train_loader, name)
        all_results[name] = results
        
        # Save
        with open(os.path.join(RESULTS_DIR, f'{name}.json'), 'w') as f:
            json.dump(results, f, indent=2)
        np.save(os.path.join(RESULTS_DIR, f'{name}_eigenvalues.npy'), eigenvalues)
    
    # Summary
    with open(os.path.join(RESULTS_DIR, 'E1_summary.json'), 'w') as f:
        json.dump(all_results, f, indent=2)
    
    print("\nExperiment E1 complete!")


if __name__ == '__main__':
    main()
