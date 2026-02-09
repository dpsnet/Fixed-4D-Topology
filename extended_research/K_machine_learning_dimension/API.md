# Neural Dimension Toolkit - API Reference

## Core Modules

### `neural_dimension.core.fisher_information`

#### `FisherInformationMatrix`

```python
class FisherInformationMatrix(model: nn.Module, sigma: float = 1.0)
```

Compute Fisher Information Matrix for neural networks.

**Methods:**

- `compute_empirical_fisher(dataloader, device='cpu') -> torch.Tensor`
  - Compute full Fisher matrix (memory intensive)
  
- `compute_diagonal_fisher(dataloader, device='cpu') -> torch.Tensor`
  - Compute diagonal approximation (efficient)
  
- `compute_spectrum(fisher_matrix=None) -> np.ndarray`
  - Compute eigenvalue spectrum
  
- `get_effective_rank(threshold=0.99) -> int`
  - Compute effective rank
  
- `get_condition_number() -> float`
  - Compute condition number

**Example:**
```python
from neural_dimension import FisherInformationMatrix

fisher_calc = FisherInformationMatrix(model, sigma=1.0)
fisher_diag = fisher_calc.compute_diagonal_fisher(train_loader)
eigenvalues = fisher_calc.compute_spectrum()
```

---

### `neural_dimension.core.effective_dimension`

#### `EffectiveDimensionCalculator`

```python
class EffectiveDimensionCalculator(fisher_calculator: FisherInformationMatrix)
```

Calculate various effective dimension measures.

**Methods:**

- `fisher_effective_dimension(fisher_matrix=None, epsilon=1e-10) -> float`
  - Compute Fisher-based effective dimension
  
- `fisher_participation_ratio(eigenvalues=None) -> float`
  - Compute participation ratio
  
- `von_neumann_dimension(eigenvalues=None) -> float`
  - Compute von Neumann dimension
  
- `capacity_dimension(eigenvalues=None, n_samples=1000) -> float`
  - Compute capacity dimension
  
- `compute_all_dimensions(n_samples=1000) -> dict`
  - Compute all dimension measures at once
  
- `dimension_reduction_ratio() -> float`
  - Compute d_eff / D ratio

**Example:**
```python
from neural_dimension import EffectiveDimensionCalculator

dim_calc = EffectiveDimensionCalculator(fisher_calc)
d_eff = dim_calc.fisher_participation_ratio(eigenvalues)
dimensions = dim_calc.compute_all_dimensions(n_samples=1000)
```

---

### `neural_dimension.core.dimension_dynamics`

#### `DimensionTracker`

```python
class DimensionTracker(model: nn.Module, compute_frequency: int = 1)
```

Track effective dimension evolution during training.

**Methods:**

- `compute_epoch_metrics(epoch, train_loader, test_loader, loss_fn, device) -> dict`
  - Compute all metrics for current epoch
  
- `update(metrics: dict)`
  - Update history with new metrics
  
- `get_history() -> dict`
  - Get full training history
  
- `plot_dynamics(save_path=None) -> Figure`
  - Plot dimension evolution
  
- `fit_dynamics_model() -> dict`
  - Fit theoretical dynamics model

**Example:**
```python
from neural_dimension.core.dimension_dynamics import DimensionTracker

tracker = DimensionTracker(model, compute_frequency=5)

for epoch in range(epochs):
    # ... training ...
    metrics = tracker.compute_epoch_metrics(epoch, train_loader, ...)
    tracker.update(metrics)

history = tracker.get_history()
tracker.plot_dynamics('dynamics.png')
```

---

## Models

### `neural_dimension.models.standard_architectures`

Available models:

- `TwoLayerMLP(hidden_dim=128)`
- `DeepMLP(input_dim, hidden_dims, output_dim, activation='relu')`
- `SimpleConvNet(num_classes=10)`
- `ResNet18(num_classes=10)`
- `VGG19(num_classes=10)`

**Factory function:**
```python
from neural_dimension.models import get_model

model = get_model('mlp2', hidden_dim=256)
model = get_model('resnet18', num_classes=10)
```

---

### `neural_dimension.models.lottery_ticket`

#### `LotteryTicketNetwork`

```python
class LotteryTicketNetwork(model: nn.Module, pruning_ratio: float = 0.2)
```

Implement Lottery Ticket Hypothesis with dimension tracking.

**Methods:**

- `prune_by_magnitude(layerwise=True)`
  - Prune weights by magnitude
  
- `reset_to_initial()`
  - Reset to initial weights (keeping mask)
  
- `run_imp_experiment(train_loader, test_loader, pruning_iterations, train_epochs, device) -> dict`
  - Run Iterative Magnitude Pruning experiment

**Example:**
```python
from neural_dimension.models.lottery_ticket import LotteryTicketNetwork

lth = LotteryTicketNetwork(model, pruning_ratio=0.2)
results = lth.run_imp_experiment(train_loader, test_loader, 
                                 pruning_iterations=10, train_epochs=30)
```

---

## Experiments

### `neural_dimension.experiments.double_descent`

#### `DoubleDescentExperiment`

```python
class DoubleDescentExperiment(model_fn, width_range, train_loader, test_loader, device)
```

Verify double descent with dimension analysis.

**Methods:**

- `run(epochs=100, lr=0.01) -> dict`
  - Run width sweep experiment
  
- `plot_results(save_path=None) -> Figure`
  - Plot double descent curves

---

### `neural_dimension.experiments.neural_collapse`

#### `NeuralCollapseExperiment`

```python
class NeuralCollapseExperiment(model, num_classes, feature_dim)
```

Analyze neural collapse with dimension tracking.

**Methods:**

- `compute_nc1(dataloader, device) -> float`
  - Within-class variability
  
- `compute_nc2(dataloader, device) -> float`
  - ETF deviation
  
- `compute_nc3(dataloader, device) -> float`
  - Self-duality
  
- `compute_effective_dimension(dataloader, device) -> float`
  - Effective dimension
  
- `run_experiment(train_loader, test_loader, epochs, optimizer_fn, loss_fn, device) -> dict`
  - Full NC experiment

---

## Visualization

### `neural_dimension.visualization.dimension_plots`

**Functions:**

- `plot_eigenvalue_spectrum(eigenvalues, title, figsize, save_path)`
- `plot_effective_dimension_comparison(results, figsize, save_path)`
- `plot_dimension_evolution(epochs, dimensions, train_loss, test_loss, figsize, save_path)`
- `plot_generalization_vs_dimension(n_samples, d_effs, gen_errors, theoretical_curve, figsize, save_path)`
- `plot_double_descent(model_complexities, train_errors, test_errors, d_effs, figsize, save_path)`

---

## Integration

### `neural_dimension.integration.cross_analyzer`

#### `CrossDirectionAnalyzer`

```python
class CrossDirectionAnalyzer(config=None)
```

Unified analysis for K-H-I-J directions.

**Methods:**

- `analyze_K(model, data_loader, device) -> dict`
- `analyze_I(graph_adj_matrix) -> dict`
- `compute_correspondence() -> dict`
- `generate_report(save_path=None) -> str`
- `save_results(path)`

---

## Utilities

### `neural_dimension.utils.config`

#### `Config`

```python
@dataclass
class Config:
    model_name: str = "TwoLayerMLP"
    hidden_dims: list = None
    epochs: int = 100
    batch_size: int = 128
    learning_rate: float = 0.01
    # ... more fields
```

**Methods:**

- `save(path)` - Save to YAML or JSON
- `load(path) -> Config` - Load from file
- `update(**kwargs)` - Update fields

**Example:**
```python
from neural_dimension.utils.config import Config

config = Config(model_name='ResNet18', epochs=200)
config.save('experiment_config.yaml')

loaded_config = Config.load('experiment_config.yaml')
```

---

### `neural_dimension.utils.logging_utils`

**Functions:**

- `setup_logger(name, level, log_file, format_string) -> Logger`
- `get_logger(name) -> Logger`

---

## Command Line

### Run all experiments:
```bash
python experiments/scripts/run_all_experiments.py --experiments all --verbose
```

### Run specific experiments:
```bash
python experiments/scripts/run_all_experiments.py --experiments E1 E2
```

### Individual experiments:
```bash
python experiments/scripts/E1_effective_dim_baseline.py
python experiments/scripts/E2_training_dynamics.py
# ... etc
```

---

## Configuration File Example

```yaml
# config.yaml
model_name: "TwoLayerMLP"
hidden_dims: [256, 128]
activation: "relu"

epochs: 100
batch_size: 128
learning_rate: 0.01
optimizer: "SGD"

dataset: "MNIST"
n_train: 5000

fisher_sigma: 1.0
fisher_approximation: "diagonal"

seed: 42
device: "auto"
output_dir: "./results"
```

---

## Version

**Current Version**: 0.1.0

**Compatibility**: Python 3.8+, PyTorch 1.10+
