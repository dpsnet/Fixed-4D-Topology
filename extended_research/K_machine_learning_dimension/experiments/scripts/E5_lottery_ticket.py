"""
E5: Lottery Ticket Hypothesis
==============================

Verify lottery ticket hypothesis with dimension analysis.
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

from neural_dimension.models import SimpleConvNet
from neural_dimension.models.lottery_ticket import LotteryTicketNetwork

# Configuration
SEED = 42
BATCH_SIZE = 128
PRUNING_ITERATIONS = 5
TRAIN_EPOCHS = 30
DEVICE = 'cuda' if torch.cuda.is_available() else 'cpu'
RESULTS_DIR = os.path.join(os.path.dirname(__file__), '..', 'results', 'lottery_ticket')


def setup_data():
    """Setup CIFAR-10 dataset."""
    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
    ])
    
    train_dataset = torchvision.datasets.CIFAR10(
        root='./data', train=True, download=True, transform=transform)
    test_dataset = torchvision.datasets.CIFAR10(
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
    print(f"Running E5: Lottery Ticket Hypothesis")
    
    train_loader, test_loader = setup_data()
    
    # Create model
    model = SimpleConvNet(num_classes=10)
    print(f"Total parameters: {sum(p.numel() for p in model.parameters()):,}")
    
    # Create lottery ticket experiment
    lth = LotteryTicketNetwork(model, pruning_ratio=0.2)
    
    # Run IMP experiment
    print("\n=== Running Iterative Magnitude Pruning ===")
    results = lth.run_imp_experiment(
        train_loader, test_loader,
        pruning_iterations=PRUNING_ITERATIONS,
        train_epochs=TRAIN_EPOCHS,
        device=DEVICE
    )
    
    # Save results
    with open(os.path.join(RESULTS_DIR, 'E5_imp_results.json'), 'w') as f:
        json.dump(results, f, indent=2)
    
    # Plot
    import matplotlib.pyplot as plt
    
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    
    sparsity = results['sparsity']
    
    # Test accuracy vs sparsity
    axes[0].plot(sparsity, results['final_test_acc'], 'b-o', linewidth=2, markersize=8)
    axes[0].set_xlabel('Sparsity', fontsize=12)
    axes[0].set_ylabel('Test Accuracy', fontsize=12)
    axes[0].set_title('Lottery Ticket: Accuracy vs Sparsity', fontsize=14)
    axes[0].grid(True, alpha=0.3)
    
    # Effective dimension vs sparsity
    axes[1].plot(sparsity, results['d_eff'], 'r-s', linewidth=2, markersize=8)
    axes[1].set_xlabel('Sparsity', fontsize=12)
    axes[1].set_ylabel('Effective Dimension', fontsize=12)
    axes[1].set_title('Dimension vs Sparsity', fontsize=14)
    axes[1].grid(True, alpha=0.3)
    
    # Remaining parameters vs sparsity
    axes[2].plot(sparsity, results['remaining_params'], 'g-^', linewidth=2, markersize=8)
    axes[2].set_xlabel('Sparsity', fontsize=12)
    axes[2].set_ylabel('Remaining Parameters', fontsize=12)
    axes[2].set_title('Parameters vs Sparsity', fontsize=14)
    axes[2].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(os.path.join(RESULTS_DIR, 'E5_lottery_ticket.png'), dpi=300)
    
    print(f"\nResults saved to {RESULTS_DIR}")
    print("\nIMP Summary:")
    for i, (s, acc, d_eff, rem) in enumerate(zip(sparsity, 
                                                   results['final_test_acc'],
                                                   results['d_eff'],
                                                   results['remaining_params'])):
        print(f"  Iter {i}: Sparsity={s:.2f}, Acc={acc:.4f}, "
              f"d_eff={d_eff:.2f}, Params={rem:,}")
    
    print("\nExperiment E5 complete!")


if __name__ == '__main__':
    main()
