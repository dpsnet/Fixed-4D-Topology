# Dimensionics Jupyter Notebooks

Interactive tutorials and demonstrations of the Unified Dimensionics Framework.

## Quick Start

```bash
# Install dependencies
pip install jupyter numpy matplotlib pandas

# Start Jupyter
jupyter notebook

# Or use JupyterLab
jupyter lab
```

## Notebook Index

### 1. Introduction to Dimensionics
**File**: `01_introduction_to_dimensionics.ipynb`

**Topics**:
- Basic dimension representation
- Variational principle for dimension selection
- Master equation solution
- Fusion theorem framework
- Dimension taxonomy

**Audience**: New users, students

**Time**: ~30 minutes

---

### 2. Network Geometry (I Direction)
**File**: `02_network_geometry.ipynb`

**Topics**:
- Large-scale network analysis (2.1M nodes)
- Dimension hierarchy visualization
- Model comparison (BA/WS failure)
- Network Master Equation
- Empirical data exploration

**Audience**: Network scientists, data analysts

**Time**: ~45 minutes

**Key Results**:
- 7 real networks analyzed
- Dimension hierarchy: Infrastructure > Academic > Social/Bio > Communication
- Standard models underestimate by 50-400%

---

### 3. Advanced Topics
**File**: `03_advanced_topics.ipynb`

**Topics**:
- Fusion theorem verification (FE-T1, FG-T4)
- Quantum dimensions (H direction)
- Random fractals (J direction)
- Cross-directional applications
- Framework visualization

**Audience**: Researchers, advanced users

**Time**: ~40 minutes

---

## Running the Notebooks

### Option 1: Local Installation

```bash
# Clone repository
git clone https://github.com/dpsnet/Fixed-4D-Topology.git
cd Fixed-4D-Topology

# Install requirements
pip install -r requirements.txt

# Start Jupyter
cd notebooks
jupyter notebook
```

### Option 2: Google Colab

Open any notebook in Google Colab:

```python
# Mount Google Drive and clone repo
!git clone https://github.com/dpsnet/Fixed-4D-Topology.git
import sys
sys.path.insert(0, '/content/Fixed-4D-Topology/src')
```

### Option 3: Docker

```bash
docker run -p 8888:8888 -v $(pwd):/home/jovyan/work jupyter/scipy-notebook
```

## Dependencies

- Python 3.8+
- NumPy
- Matplotlib
- Pandas (for data visualization)
- Jupyter

Optional:
- SciPy (for optimization)
- NetworkX (for network analysis)

## Data Sources

The notebooks use empirical data from:

1. **Internet AS**: CAIDA AS-Skitter (1.7M nodes)
2. **DBLP**: SNAP collaboration network (317K nodes)
3. **Yeast PPI**: BioGRID (6.8K nodes)
4. **Facebook**: SNAP social network (4K nodes)
5. **Twitter**: SNAP social network (81K nodes)
6. **Power Grid**: IEEE test case (101 nodes)
7. **Email**: SNAP EU-Core (1.1K nodes)

Total: **2,107,149 nodes**

## Examples

### Basic Usage

```python
from unified_framework import (
    Dimension,
    VariationalPrinciple,
    NetworkDimension
)

# Compute optimal dimension
vp = VariationalPrinciple(A=1.0, alpha=0.5, T=0.3)
d_opt = vp.optimal_dimension()
print(f"Optimal dimension: {d_opt:.3f}")

# Analyze network
nd = NetworkDimension()
nd.from_edge_list(edges)
result = nd.box_counting_dimension()
print(f"Network dimension: {result['dimension']:.3f}")
```

### Empirical Data

```python
from unified_framework import EMPIRICAL_NETWORK_DATA

# Access Internet AS data
data = EMPIRICAL_NETWORK_DATA['internet_as']
print(f"Nodes: {data['nodes']:,}")
print(f"Dimension: {data['dimension']}")
```

## Output Examples

### Variational Principle

```
Optimal dimension: d* = 0.617
Minimum free energy: F(d*) = 2.341
```

### Network Analysis

```
Network: Internet AS
Nodes: 1,696,415
Dimension: 4.36
Type: Infrastructure
```

## Troubleshooting

### Module Not Found

```python
import sys
sys.path.insert(0, '../src')  # Adjust path as needed
```

### Large Data

Notebooks 2 and 3 use pre-computed results. For full analysis with raw data, see:
- `extended_research/I_network_geometry/`

### Memory Issues

If running large network analysis:
```python
# Use sampling
result = nd.correlation_dimension(sample_ratio=0.1)
```

## Citation

If you use these notebooks in your research, please cite:

```bibtex
@software{dimensionics2026,
  title={Dimensionics: Unified Framework for Mathematical Theory of Dimension},
  author={A~G Research Team and Fixed-4D-Topology Team},
  year={2026},
  url={https://github.com/dpsnet/Fixed-4D-Topology}
}
```

## Contributing

Contributions welcome! Areas for expansion:
- Additional visualization examples
- More network types
- Quantum dimension simulations
- Random fractal animations

See `CONTRIBUTING.md` for guidelines.

## License

MIT License - See LICENSE file

## Contact

- GitHub Issues: https://github.com/dpsnet/Fixed-4D-Topology/issues
- Email: [project email]

---

**Last Updated**: February 2026  
**Version**: 2.0  
**Status**: Active Development
