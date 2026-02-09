"""
E6: Generalization Bound Verification
======================================

Verify the dimension-dependent generalization bound.
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

from neural_dimension import FisherInformationMatrix, EffectiveDimensionCalculator
from neural_dimension.models import TwoLayerMLP

# Configuration
SEED = 42
BATCH_SIZE = 128
EPOCHS = 50
DEVICE = 'cuda' if torch.cuda.is_available() else 'cpu'
RESULTS_DIR = os.path.join(os.path.dirname(__file__), '..', 'results', 'generalization')


def setup_data(n_train):
    """Setup MNIST with subset of size n_train."""
    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.1307,), (0.3081,))
    ])
    
    train_full = torchvision.datasets.MNIST(
        root='./data', train=True, download=True, transform=transform)
    test_dataset = torchvision.datasets.MNIST(
        root='./data', train=False, download=True, transform=transform)
    
    # Use subset
    train_subset = Subset(train_full, range(min(n_train, len(train_full))))
    
    train_loader = DataLoader(train_subset, batch_size=BATCH_SIZE, shuffle=True)
    test_loader = DataLoader(test_dataset, batch_size=BATCH_SIZE, shuffle=False)
    
    return train_loader, test_loader


def train_and_evaluate(model, train_loader, test_loader, epochs, device):
    """Train model and return train/test error."""
    optimizer = torch.optim.SGD(model.parameters(), lr=0.01, momentum=0.9)
    loss_fn = nn.CrossEntropyLoss()
    
    model.to(device)
    
    for epoch in range(epochs):
        model.train()
        for data, target in train_loader:
            data, target = data.to(device), target.to(device)
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
        for data, target in train_loader:
            data, target = data.to(device), target.to(device)
            output = model(data)
            pred = output.argmax(dim=1)
            train_correct += (pred == target).sum().item()
            train_total += target.size(0)
        
        for data, target in test_loader:
            data, target = data.to(device), target.to(device)
            output = model(data)
            pred = output.argmax(dim=1)
            test_correct += (pred == target).sum().item()
            test_total += target.size(0)
    
    train_error = 1 - train_correct / train_total
    test_error = 1 - test_correct / test_total
    
    return train_error, test_error


def main():
    """Main experiment."""
    torch.manual_seed(SEED)
    np.random.seed(SEED)
    os.makedirs(RESULTS_DIR, exist_ok=True)
    
    print(f"Device: {DEVICE}")
    print(f"Running E6: Generalization Bound Verification")
    
    # Different sample sizes
    sample_sizes = [500, 1000, 2000, 5000, 10000]
    
    results = {
        'n_samples': [],
        'train_errors': [],
        'test_errors': [],
        'gen_errors': [],
        'd_effs': [],
        'theoretical_bounds': [],
    }
    
    for n in sample_sizes:
        print(f"\n--- Training with n={n} samples ---")
        
        train_loader, test_loader = setup_data(n)
        
        # Create and train model
        model = TwoLayerMLP(hidden_dim=256)
        train_err, test_err = train_and_evaluate(model, train_loader, test_loader, EPOCHS, DEVICE)
        gen_err = abs(test_err - train_err)
        
        # Compute effective dimension
        fisher_calc = FisherInformationMatrix(model, sigma=1.0)
        fisher_diag = fisher_calc.compute_diagonal_fisher(train_loader, device=DEVICE)
        eigenvalues = fisher_diag.numpy()
        eigenvalues = np.sort(eigenvalues)[::-1]
        
        dim_calc = EffectiveDimensionCalculator(fisher_calc)
        d_eff = dim_calc.fisher_participation_ratio(eigenvalues)
        
        # Theoretical bound
        delta = 0.05
        theoretical_bound = np.sqrt((d_eff * np.log(n / d_eff) + np.log(1/delta)) / (2 * n))
        
        results['n_samples'].append(n)
        results['train_errors'].append(train_err)
        results['test_errors'].append(test_err)
        results['gen_errors'].append(gen_err)
        results['d_effs'].append(d_eff)
        results['theoretical_bounds'].append(theoretical_bound)
        
        print(f"  Train error: {train_err:.4f}")
        print(f"  Test error: {test_err:.4f}")
        print(f"  Gen error: {gen_err:.4f}")
        print(f"  d_eff: {d_eff:.2f}")
        print(f"  Theoretical bound: {theoretical_bound:.4f}")
        print(f"  Ratio (gen/bound): {gen_err/theoretical_bound:.2f}")
    
    # Save results
    with open(os.path.join(RESULTS_DIR, 'E6_results.json'), 'w') as f:
        json.dump(results, f, indent=2)
    
    # Plot
    import matplotlib.pyplot as plt
    
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    
    n_samples = results['n_samples']
    gen_errors = results['gen_errors']
    theoretical = results['theoretical_bounds']
    d_effs = results['d_effs']
    
    # Gen error vs theoretical bound
    axes[0].scatter(theoretical, gen_errors, s=100, c=n_samples, cmap='viridis')
    max_val = max(max(theoretical), max(gen_errors))
    axes[0].plot([0, max_val], [0, max_val], 'k--', label='y=x')
    axes[0].set_xlabel('Theoretical Bound', fontsize=12)
    axes[0].set_ylabel('Actual Generalization Error', fontsize=12)
    axes[0].set_title('Bound Verification', fontsize=14)
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)
    
    # d_eff/n vs gen error (log-log)
    ratios = [d/n for d, n in zip(d_effs, n_samples)]
    axes[1].loglog(ratios, gen_errors, 'b-o', label='Actual', linewidth=2, markersize=8)
    
    # Theoretical scaling
    x_range = np.logspace(np.log10(min(ratios)), np.log10(max(ratios)), 100)
    y_theory = np.sqrt(x_range)  # sqrt(d_eff/n) scaling
    axes[1].loglog(x_range, y_theory, 'r--', label='Theory: sqrt(d_eff/n)', linewidth=2)
    
    axes[1].set_xlabel('d_eff / n', fontsize=12)
    axes[1].set_ylabel('Generalization Error', fontsize=12)
    axes[1].set_title('Scaling Verification', fontsize=14)
    axes[1].legend()
    axes[1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(os.path.join(RESULTS_DIR, 'E6_generalization.png'), dpi=300)
    
    print(f"\nResults saved to {RESULTS_DIR}")
    print("\nExperiment E6 complete!")


if __name__ == '__main__':
    main()
