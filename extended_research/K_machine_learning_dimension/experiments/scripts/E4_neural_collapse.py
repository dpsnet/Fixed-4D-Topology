"""
E4: Neural Collapse Analysis
=============================

Analyze neural collapse with effective dimension tracking.
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

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'code'))

from neural_dimension.models import TwoLayerMLP
from neural_dimension.experiments import NeuralCollapseExperiment

# Configuration
SEED = 42
BATCH_SIZE = 128
EPOCHS = 200
DEVICE = 'cuda' if torch.cuda.is_available() else 'cpu'
RESULTS_DIR = os.path.join(os.path.dirname(__file__), '..', 'results', 'neural_collapse')
NUM_CLASSES = 10
FEATURE_DIM = 256


def setup_data():
    """Setup MNIST dataset."""
    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.1307,), (0.3081,))
    ])
    
    train_dataset = torchvision.datasets.MNIST(
        root='./data', train=True, download=True, transform=transform)
    test_dataset = torchvision.datasets.MNIST(
        root='./data', train=False, download=True, transform=transform)
    
    train_loader = DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True)
    test_loader = DataLoader(test_dataset, batch_size=BATCH_SIZE, shuffle=False)
    
    return train_loader, test_loader


def main():
    """Main experiment."""
    torch.manual_seed(SEED)
    np.random.seed(SEED)
    os.makedirs(RESULTS_DIR, exist_ok=True)
    
    print(f"Device: {DEVICE}")
    print(f"Running E4: Neural Collapse Analysis")
    
    train_loader, test_loader = setup_data()
    
    # Create model
    model = TwoLayerMLP(hidden_dim=FEATURE_DIM)
    
    # Create experiment
    experiment = NeuralCollapseExperiment(model, NUM_CLASSES, FEATURE_DIM)
    
    # Run
    optimizer_fn = lambda p: torch.optim.SGD(p, lr=0.01, momentum=0.9)
    loss_fn = nn.CrossEntropyLoss()
    
    history = experiment.run_experiment(
        train_loader, test_loader, EPOCHS, optimizer_fn, loss_fn, DEVICE
    )
    
    # Save results
    with open(os.path.join(RESULTS_DIR, 'E4_history.json'), 'w') as f:
        json.dump(history, f, indent=2)
    
    # Plot
    import matplotlib.pyplot as plt
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    epochs = history['epoch']
    
    # NC1
    axes[0, 0].plot(epochs, history['nc1'], 'b-o')
    axes[0, 0].set_xlabel('Epoch')
    axes[0, 0].set_ylabel('NC1 (Within-class variability)')
    axes[0, 0].set_title('NC1 Evolution')
    axes[0, 0].grid(True, alpha=0.3)
    
    # NC2
    axes[0, 1].plot(epochs, history['nc2'], 'r-s')
    axes[0, 1].set_xlabel('Epoch')
    axes[0, 1].set_ylabel('NC2 (ETF deviation)')
    axes[0, 1].set_title('NC2 Evolution')
    axes[0, 1].grid(True, alpha=0.3)
    
    # NC3
    axes[1, 0].plot(epochs, history['nc3'], 'g-^')
    axes[1, 0].set_xlabel('Epoch')
    axes[1, 0].set_ylabel('NC3 (Self-duality)')
    axes[1, 0].set_title('NC3 Evolution')
    axes[1, 0].grid(True, alpha=0.3)
    
    # d_eff
    axes[1, 1].plot(epochs, history['d_eff'], 'm-d')
    axes[1, 1].axhline(y=NUM_CLASSES-1, color='k', linestyle='--', 
                       label=f'K-1 = {NUM_CLASSES-1}')
    axes[1, 1].set_xlabel('Epoch')
    axes[1, 1].set_ylabel('Effective Dimension')
    axes[1, 1].set_title('Dimension Evolution')
    axes[1, 1].legend()
    axes[1, 1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(os.path.join(RESULTS_DIR, 'E4_neural_collapse.png'), dpi=300)
    
    print(f"\nResults saved to {RESULTS_DIR}")
    print(f"\nFinal values:")
    print(f"  NC1: {history['nc1'][-1]:.4f}")
    print(f"  NC2: {history['nc2'][-1]:.4f}")
    print(f"  NC3: {history['nc3'][-1]:.4f}")
    print(f"  d_eff: {history['d_eff'][-1]:.2f}")
    print(f"  Test Acc: {history['test_acc'][-1]:.4f}")
    
    print("\nExperiment E4 complete!")


if __name__ == '__main__':
    main()
