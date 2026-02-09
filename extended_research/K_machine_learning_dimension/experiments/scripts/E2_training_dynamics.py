"""
E2: Training Dynamics Tracking
==============================

Track effective dimension evolution during training.
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

from neural_dimension import FisherInformationMatrix, EffectiveDimensionCalculator
from neural_dimension.core.dimension_dynamics import DimensionTracker
from neural_dimension.models import TwoLayerMLP

# Configuration
SEED = 42
BATCH_SIZE = 128
EPOCHS = 50
DEVICE = 'cuda' if torch.cuda.is_available() else 'cpu'
RESULTS_DIR = os.path.join(os.path.dirname(__file__), '..', 'results', 'training_dynamics')


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


def train_with_tracking(model, train_loader, test_loader, epochs, device):
    """Train model while tracking dimension."""
    
    # Setup tracker
    tracker = DimensionTracker(model, compute_frequency=5)  # Every 5 epochs
    
    optimizer = torch.optim.SGD(model.parameters(), lr=0.01, momentum=0.9)
    loss_fn = nn.CrossEntropyLoss()
    
    model.to(device)
    
    for epoch in range(epochs):
        # Training
        model.train()
        for data, target in train_loader:
            data, target = data.to(device), target.to(device)
            
            optimizer.zero_grad()
            output = model(data)
            loss = loss_fn(output, target)
            loss.backward()
            optimizer.step()
        
        # Compute metrics
        metrics = tracker.compute_epoch_metrics(
            epoch, train_loader, test_loader, loss_fn, device
        )
        tracker.update(metrics)
        
        if epoch % 5 == 0:
            print(f"Epoch {epoch}: Train Loss={metrics['train_loss']:.4f}, "
                  f"Test Acc={metrics['test_acc']:.4f if metrics['test_acc'] else 0:.4f}, "
                  f"d_eff={metrics['d_eff_fisher']:.2f if metrics['d_eff_fisher'] else 0:.2f}")
    
    return tracker


def main():
    """Main experiment."""
    torch.manual_seed(SEED)
    np.random.seed(SEED)
    os.makedirs(RESULTS_DIR, exist_ok=True)
    
    print(f"Device: {DEVICE}")
    print(f"Running E2: Training Dynamics Tracking")
    
    train_loader, test_loader = setup_data()
    
    # Create model
    model = TwoLayerMLP(hidden_dim=256)
    
    # Train with tracking
    tracker = train_with_tracking(model, train_loader, test_loader, EPOCHS, DEVICE)
    
    # Get history
    history = tracker.get_history()
    
    # Save results
    with open(os.path.join(RESULTS_DIR, 'E2_history.json'), 'w') as f:
        json.dump(history, f, indent=2)
    
    # Plot
    fig = tracker.plot_dynamics(save_path=os.path.join(RESULTS_DIR, 'E2_dynamics.png'))
    print(f"\nResults saved to {RESULTS_DIR}")
    
    # Fit dynamics model
    fitted_params = tracker.fit_dynamics_model()
    with open(os.path.join(RESULTS_DIR, 'E2_fitted_params.json'), 'w') as f:
        json.dump(fitted_params, f, indent=2)
    
    print("\nFitted dynamics parameters:")
    print(f"  d_eff_init: {fitted_params['d_eff_init']:.2f}")
    print(f"  d_eff_final: {fitted_params['d_eff_final']:.2f}")
    print(f"  d_data_estimate: {fitted_params['d_data_estimate']:.2f}")
    
    print("\nExperiment E2 complete!")


if __name__ == '__main__':
    main()
