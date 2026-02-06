# Fixed 4D Topology API Reference

## Core Modules

### Cantor Representation (`cantor_representation`)

```python
from fixed_4d_topology import CantorRepresentation

rep = CantorRepresentation()
result = rep.approximate(alpha=0.5, epsilon=1e-6)
```

#### Classes

**CantorRepresentation**
- `__init__(dimensions=None)`: Initialize with custom dimensions
- `approximate(alpha, epsilon)`: Approximate real number
- `verify_linear_independence()`: Check linear independence
- `analyze_density(n_samples)`: Density analysis
- `compute_optimal_complexity(epsilon)`: Theoretical bound

### Spectral Dimension (`spectral_dimension`)

```python
from fixed_4d_topology import SpectralDimension

spec = SpectralDimension("sierpinski")
d_s = spec.compute_spectral_dimension(t=1e-5)
```

#### Classes

**SpectralDimension**
- `__init__(fractal_type)`: Initialize for fractal type
- `compute_spectral_dimension(t)`: Compute d_s at time t
- `evolve(t_span, d_s_init, n_points)`: Evolve PDE
- `verify_pde(t_test)`: Verify PDE consistency

**HeatKernel**
- `compute_eigenvalues(n_eigen)`: Compute Laplacian eigenvalues
- `return_probability(t)`: Compute p(t)
- `extract_spectral_dimension(t)`: Extract d_s from heat kernel

### Modular Correspondence (`modular_correspondence`)

```python
from fixed_4d_topology import ModularCorrespondence, RamanujanFractal

corr = ModularCorrespondence()
results = corr.ramanujan.verify_correspondence()
```

#### Classes

**ModularCorrespondence**
- `compute_structure_preservation(modular_data, fractal_data)`: Measure preservation
- `construct_correspondence(form_name, fractal_type)`: Build correspondence

**RamanujanFractal**
- `compute_l_function(form_name, s)`: Compute L(f, s)
- `compute_hausdorff_dimension(form_name)`: Predict d_H
- `verify_correspondence()`: Verify predictions

### Fractal Arithmetic (`fractal_arithmetic`)

```python
from fixed_4d_topology import FractalArithmetic, GrothendieckGroup

arith = FractalArithmetic()
d_sum = arith.add_dimensions(d1, d2)
```

#### Classes

**FractalArithmetic**
- `add_dimensions(d1, d2, base)`: Dimension addition ⊕
- `multiply_dimensions(d1, d2, base)`: Dimension multiplication ⊗
- `dimension_to_rational(d, r)`: Convert to ℚ
- `rational_to_dimension(q, r)`: Convert from ℚ

**GrothendieckGroup**
- `log_isomorphism(element)`: Map to ℚ
- `inverse_log_isomorphism(q)`: Map from ℚ
- `group_operation(a, b)`: Group addition
- `verify_isomorphism(n_tests)`: Verify isomorphism

**FractalElement**
- `(positive, negative)`: Create element [N₁/r] - [N₂/r]
- `dimension_value()`: Compute numerical value

## Common Types

### Data Classes

```python
@dataclass
class CantorApproximation:
    target: float
    epsilon: float
    dimensions: List[float]
    coefficients: List[float]
    approximation: float
    error: float
    steps: int
    convergence_rate: float

@dataclass  
class SpectralEvolutionResult:
    t_values: np.ndarray
    d_s_values: np.ndarray
    eigenvalues: np.ndarray
    convergence_achieved: bool
    final_d_s: float

@dataclass
class CorrespondenceResult:
    fractal_name: str
    modular_form: str
    l_value: complex
    d_h_predicted: float
    d_h_computed: float
    error: float
    structure_preservation: float
```

## Constants

```python
# Fractal types
SpectralDimension.FRACTAL_TYPES = {
    "sierpinski": {"d_s_exact": 1.365..., "name": "Sierpinski Gasket"},
    "cantor_dust": {"d_s_exact": 1.261..., "name": "Cantor Dust"},
    "koch": {"d_s_exact": 1.0, "name": "Koch Curve"},
    "menger": {"d_s_exact": 2.727..., "name": "Menger Sponge"},
}

# Cantor dimensions
CantorRepresentation.CANTOR_DIMENSIONS = [
    log(2)/log(3),  # 0.6309...
    log(3)/log(4),  # 0.7924...
    log(4)/log(5),  # 0.8613...
    log(5)/log(6),  # 0.8982...
    log(6)/log(7),  # 0.9208...
]
```

## Error Handling

All functions raise appropriate exceptions:
- `ValueError`: Invalid input parameters
- `RuntimeError`: Computation failures
- `TypeError`: Type mismatches

## Performance Notes

- Numba JIT compilation for hot loops
- Sparse matrix operations for large graphs
- Vectorized NumPy operations where possible

## Thread Safety

Core classes are stateless and thread-safe. Results objects are immutable.
