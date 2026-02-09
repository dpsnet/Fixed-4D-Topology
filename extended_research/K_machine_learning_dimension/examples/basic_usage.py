"""
Basic Usage Example
===================

Demonstrate basic usage of neural_dimension package.
"""

import torch
import torch.nn as nn
import torchvision
import torchvision.transforms as transforms
from torch.utils.data import DataLoader
import numpy as np

# Import neural_dimension
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'code'))

from neural_dimension import FisherInformationMatrix, EffectiveDimensionCalculator
from neural_dimension.models import TwoLayerMLP


def main():
    print("=" * 60)
    print("K Direction: Basic Usage Example")
    print("=" * 60)
    
    # 1. Setup data
    print("\n1. Loading MNIST dataset...")
    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.1307,), (0.3081,))
    ])
    
    train_dataset = torchvision.datasets.MNIST(
        root='./data', train=True, download=True, transform=transform
    )
    
    # Use subset for quick demo
    train_subset = torch.utils.data.Subset(train_dataset, range(1000))
    train_loader = DataLoader(train_subset, batch_size=128, shuffle=True)
    print(f"   Dataset size: {len(train_subset)}")
    
    # 2. Create model
    print("\n2. Creating model...")
    model = TwoLayerMLP(hidden_dim=128)
    total_params = sum(p.numel() for p in model.parameters())
    print(f"   Model: TwoLayerMLP")
    print(f"   Total parameters: {total_params:,}")
    
    # 3. Compute Fisher Information
    print("\n3. Computing Fisher Information Matrix...")
    fisher_calc = FisherInformationMatrix(model, sigma=1.0)
    fisher_diag = fisher_calc.compute_diagonal_fisher(train_loader, device='cpu')
    print(f"   Fisher matrix computed")
    
    # 4. Compute effective dimension
    print("\n4. Computing effective dimension...")
    eigenvalues = fisher_diag.numpy()
    eigenvalues = eigenvalues[eigenvalues > 1e-10]  # Remove zeros
    eigenvalues = np.sort(eigenvalues)[::-1]
    
    dim_calc = EffectiveDimensionCalculator(fisher_calc)
    d_eff = dim_calc.fisher_participation_ratio(eigenvalues)
    
    print(f"   Effective dimension: {d_eff:.2f}")
    print(f"   Total parameters: {total_params}")
    print(f"   Dimension reduction: {(1 - d_eff/total_params)*100:.1f}%")
    
    # 5. Additional metrics
    print("\n5. Additional metrics...")
    d_vn = dim_calc.von_neumann_dimension(eigenvalues)
    print(f"   von Neumann dimension: {d_vn:.2f}")
    
    # 6. Summary
    print("\n" + "=" * 60)
    print("Summary")
    print("=" * 60)
    print(f"Model has {total_params:,} parameters")
    print(f"But only {d_eff:.1f} effective dimensions")
    print(f"Compression ratio: {d_eff/total_params:.3f}")
    print("\nThis shows neural networks have significant redundancy!")
    print("=" * 60)


if __name__ == '__main__':
    main()
