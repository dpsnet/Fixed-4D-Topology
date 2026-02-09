"""
E3: Double Descent Verification
================================

Verify double descent phenomenon with dimension analysis.
"""

import os
import sys
import json
import torch
import torch.nn as nn
import torchvision
import torchvision.transforms as transforms
from torch.utils.data import DataLoader, Subset
import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'code'))

from neural_dimension.models import TwoLayerMLP
from neural_dimension.experiments import DoubleDescentExperiment

# Configuration
SEED = 42
BATCH_SIZE = 128
EPOCHS = 100
DEVICE = 'cuda' if torch.cuda.is_available() else 'cpu'
RESULTS_DIR = os.path.join(os.path.dirname(__file__), '..', 'results', 'double_descent')


def setup_data(n_train=5000):
    """Setup CIFAR-10 with subset."""
    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
    ])
    
    train_full = torchvision.datasets.CIFAR10(
        root='./data', train=True, download=True, transform=transform)
    test_dataset = torchvision.datasets.CIFAR10(
        root='./data', train=False, download=True, transform=transform)
    
    # Use subset for faster training
    train_subset = Subset(train_full, range(n_train))
    
    train_loader = DataLoader(train_subset, batch_size=BATCH_SIZE, shuffle=True)
    test_loader = DataLoader(test_dataset, batch_size=BATCH_SIZE, shuffle=False)
    
    return train_loader, test_loader


def main():
    """Main experiment."""
    torch.manual_seed(SEED)
    np.random.seed(SEED)
    os.makedirs(RESULTS_DIR, exist_ok=True)
    
    print(f"Device: {DEVICE}")
    print(f"Running E3: Double Descent Verification")
    
    train_loader, test_loader = setup_data(n_train=5000)
    
    # Width range to test
    width_range = [32, 64, 128, 256, 512, 1024, 2048]
    
    # Create model factory
    def model_fn(width):
        return TwoLayerMLP(hidden_dim=width)
    
    # Run experiment
    experiment = DoubleDescentExperiment(
        model_fn, width_range, train_loader, test_loader, DEVICE
    )
    
    results = experiment.run(epochs=EPOCHS, lr=0.01)
    
    # Save results
    with open(os.path.join(RESULTS_DIR, 'E3_results.json'), 'w') as f:
        json.dump(results, f, indent=2)
    
    # Plot
    experiment.plot_results(save_path=os.path.join(RESULTS_DIR, 'E3_double_descent.png'))
    
    print(f"\nResults saved to {RESULTS_DIR}")
    print("\nKey findings:")
    n_samples = 5000
    for i, (w, d_eff, test_err) in enumerate(zip(results['widths'], 
                                                  results['d_effs'], 
                                                  results['test_errors'])):
        marker = " ***" if abs(d_eff - n_samples) / n_samples < 0.3 else ""
        print(f"  Width {w:4d}: d_eff={d_eff:7.1f}, test_err={test_err:.4f}{marker}")
    
    print("\nExperiment E3 complete!")


if __name__ == '__main__':
    main()
