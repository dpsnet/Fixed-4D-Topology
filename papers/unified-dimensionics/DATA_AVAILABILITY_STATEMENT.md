# Data Availability Statement

## Overview

This manuscript is supported by comprehensive data and software that are publicly available to ensure full reproducibility of our results.

---

## Open Source Repository

**Primary Repository**: https://github.com/dpsnet/Fixed-4D-Topology

**License**: MIT License (permissive open source)

**Contents**:
- Complete Python implementation of the unified framework
- Analysis scripts for network dimension computation
- Jupyter notebook tutorials
- LaTeX source files for the manuscript
- All numerical validation code

---

## Empirical Network Data

Our large-scale empirical study analyzes 7 real-world networks with a total of **2,107,149 nodes**. The data sources are:

### 1. Internet AS Topology
- **Source**: CAIDA (Center for Applied Internet Data Analysis)
- **Dataset**: AS-Skitter
- **Nodes**: 1,696,415
- **Type**: Infrastructure
- **Access**: Public dataset (https://www.caida.org/)
- **Dimension Measured**: 4.36

### 2. DBLP Collaboration Network
- **Source**: SNAP (Stanford Network Analysis Project)
- **Dataset**: DBLP co-authorship
- **Nodes**: 317,080
- **Type**: Academic
- **Access**: Public dataset (https://snap.stanford.edu/)
- **Dimension Measured**: 3.0

### 3. Yeast Protein-Protein Interaction (PPI)
- **Source**: BioGRID (Biological General Repository for Interaction Datasets)
- **Version**: 5.0.254
- **Nodes**: 6,800
- **Type**: Biological
- **Access**: Public dataset (https://thebiogrid.org/)
- **Dimension Measured**: 2.4

### 4. Facebook Social Network
- **Source**: SNAP
- **Dataset**: Facebook combined
- **Nodes**: 4,039
- **Type**: Social
- **Access**: Public dataset
- **Dimension Measured**: 2.57

### 5. Twitter Social Network
- **Source**: SNAP
- **Dataset**: Twitter combined
- **Nodes**: 81,306
- **Type**: Social
- **Access**: Public dataset
- **Dimension Measured**: 2.0

### 6. IEEE Power Grid
- **Source**: IEEE Test Case
- **Nodes**: 101
- **Type**: Infrastructure
- **Access**: Public test case
- **Dimension Measured**: 2.11

### 7. Email EU-Core Network
- **Source**: SNAP
- **Nodes**: 1,133
- **Type**: Communication
- **Access**: Public dataset
- **Dimension Measured**: 1.24

### Data Processing

All data processing scripts are available in the repository:
- `extended_research/I_network_geometry/data/parse_biogrid_yeast.py`
- `extended_research/I_network_geometry/data/parse_power_grid.py`
- `extended_research/I_network_geometry/algorithms/network_data_loader.py`

### Data Format

Processed data is stored in edge-list format:
```
node1 node2
node1 node3
...
```

Due to size constraints, large raw data files (>10MB) are not included in the Git repository but can be downloaded from the original sources listed above.

---

## Software Implementation

### Core Framework

**Module**: `src/unified_framework/`

Key components:
- `core.py`: Dimension and VariationalPrinciple classes
- `network.py`: NetworkDimension and NetworkMasterEquation (I-direction)
- `algebraic.py`: GrothendieckGroup implementation (T4)
- `analytic.py`: SobolevSpace implementation (E)
- `evolution.py`: DimensionFlow and SpectralPDE (B, T2)
- `fusion.py`: Fusion theorem implementations

### Algorithms

**Location**: `extended_research/I_network_geometry/algorithms/`

- `compute_all_dimensions.py`: Batch dimension computation
- `network_data_loader.py`: Data loading utilities
- `analyze_large_network.py`: Large-scale network analysis

### Validation

**Location**: `tests/`

- `test_network_dimension.py`: Unit tests for network analysis
- `test_fusion_theorems.py`: Tests for fusion theorem verification

---

## Reproducibility

### Quick Start

```bash
# Clone repository
git clone https://github.com/dpsnet/Fixed-4D-Topology.git
cd Fixed-4D-Topology

# Install dependencies
pip install numpy scipy matplotlib pandas

# Run tests
python -m pytest tests/test_network_dimension.py -v

# Run example
python examples/example_network_analysis.py
```

### Jupyter Notebooks

Interactive tutorials are provided:
- `notebooks/01_introduction_to_dimensionics.ipynb`
- `notebooks/02_network_geometry.ipynb`
- `notebooks/03_advanced_topics.ipynb`

### Figure Generation

All paper figures can be regenerated:
```bash
python scripts/generate_figures.py --output-dir ./figures/
```

---

## Figure Data

Raw data for all figures is available in:
- `figure_data/figure1_data.json` - Network hierarchy
- `figure_data/figure2_data.json` - Variational principle
- `figure_data/figure3_data.json` - Model comparison

CSV format is also provided for easy import into other tools.

---

## Supplementary Information

Additional materials available:

1. **Extended Proofs**: Detailed proofs of fusion theorems
2. **Additional Numerical Results**: Extended parameter studies
3. **Algorithm Pseudocode**: Detailed algorithm descriptions
4. **Convergence Analysis**: Numerical convergence studies

Location: `papers/unified-dimensionics/Supplementary_Information.md`

---

## Data Citation

When using our empirical data, please cite both our work and the original data sources:

```bibtex
@software{dimensionics2026,
  title={Dimensionics: Unified Framework for Mathematical Theory of Dimension},
  author={[Authors]},
  year={2026},
  url={https://github.com/dpsnet/Fixed-4D-Topology}
}

@dataset{caida_as_skitter,
  title={AS-Skitter Internet Topology Data},
  author={CAIDA},
  year={2024},
  url={https://www.caida.org/}
}

@dataset{snap_networks,
  title={SNAP: Stanford Network Analysis Project},
  author={Leskovec, Jure and Krevl, Andrej},
  year={2014},
  url={https://snap.stanford.edu/}
}

@dataset{biogrid,
  title={BioGRID: Biological General Repository for Interaction Datasets},
  author={Stark, Chris and others},
  year={2006},
  journal={Nucleic Acids Research}
}
```

---

## Data Sharing Policy Compliance

This work complies with:
- **FAIR Principles**: Findable, Accessible, Interoperable, Reusable
- **Open Science**: All code and data publicly available
- **Reproducibility**: Complete documentation and tutorials provided
- **Transparency**: All analysis steps documented

---

## Contact

For questions about data access or reproduction:
- Open an issue on GitHub: https://github.com/dpsnet/Fixed-4D-Topology/issues
- Email: [contact email]

---

**Date**: February 8, 2026  
**Version**: 1.0
