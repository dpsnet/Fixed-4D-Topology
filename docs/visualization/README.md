# Visualization Data Files

This directory contains data files for generating figures in the Unified Dimensionics Framework paper.

## Files

| File | Description | Format |
|------|-------------|--------|
| `figure1_dimension_evolution.csv` | Dimension evolution in cosmological time | CSV/JSON |
| `figure2_redshift_scaling.csv` | Dimension vs redshift (CMB observables) | CSV/JSON |
| `figure3_ising_critical.csv` | Effective dimension at Ising critical point | CSV/JSON |
| `figure4_percolation.csv` | Percolation transition data | CSV/JSON |
| `figure5_network_dimension.csv` | Network dimension scaling | CSV/JSON |
| `figure6_fusion_diagram.json` | Fusion theorem relationships (TikZ) | JSON |
| `figure7_phase_diagram.csv` | Phase diagram in (d, T) space | CSV/JSON |
| `figure8_numerical_validation.csv` | Numerical validation results | CSV/JSON |

## Usage

### With LaTeX pgfplots

```latex
\usepackage{pgfplots}
\pgfplotsset{compat=1.17}

\begin{figure}
\centering
\begin{tikzpicture}
\begin{axis}[
    xlabel={Time (Gyr)},
    ylabel={Dimension},
    grid=major,
]
\addplot table {figure1_dimension_evolution.csv};
\end{axis}
\end{tikzpicture}
\end{figure}
```

### With Python/Matplotlib

```python
import matplotlib.pyplot as plt
import pandas as pd

data = pd.read_csv('figure1_dimension_evolution.csv')
plt.plot(data['t'], data['cosmological'])
plt.xlabel('Time (Gyr)')
plt.ylabel('Dimension')
plt.show()
```

## Regenerating Data

```bash
python3 generate_figures.py
```

All data is generated using pure Python (no numpy/scipy dependencies).

## Data Format

Each CSV file includes headers. JSON files contain the same data in structured format.

## Version

- Generated: February 8, 2026
- Framework version: v3.0
