# Supplementary Information

## Effective Dimensions of Complex Networks: A Large-Scale Empirical Study

---

## S1. Detailed Network Statistics

### S1.1 Internet AS Topology
| Metric | Value |
|--------|-------|
| Nodes | 1,696,415 |
| Edges | 11,095,298 |
| Average degree | 13.08 |
| Max degree | 25,956 |
| Clustering coefficient | 0.286 |
| Power-law exponent | ~2.1 |
| Assortativity | -0.19 |

### S1.2 DBLP Academic Collaboration
| Metric | Value |
|--------|-------|
| Nodes | 317,080 |
| Edges | 1,049,866 |
| Average degree | 6.62 |
| Max degree | 2,188 |
| Clustering coefficient | 0.270 |
| Largest component | 85% |

### S1.3 Yeast PPI Network
| Metric | Value |
|--------|-------|
| Nodes | 7,203 |
| Edges | 179,936 |
| Average degree | 49.96 |
| Max degree | 3,613 |
| Clustering coefficient | 0.370 |
| Network density | 0.0069 |

### S1.4 Facebook Social Network
| Metric | Value |
|--------|-------|
| Nodes | 4,039 |
| Edges | 88,234 |
| Average degree | 43.69 |
| Max degree | 1,045 |
| Clustering coefficient | 0.601 |
| Assortativity | 0.226 |

### S1.5 Twitter Social Network
| Metric | Value |
|--------|-------|
| Nodes | 81,306 |
| Edges | 2,420,766 |
| Average degree | 59.55 |
| Max degree | 3,372 |
| Clustering coefficient | ~0.5 |

### S1.6 IEEE Power Grid
| Metric | Value |
|--------|-------|
| Nodes | 101 |
| Edges | 124 |
| Average degree | 2.46 |
| Max degree | 16 |
| Clustering coefficient | 0.141 |
| Diameter | ~10 |

### S1.7 Email Communication Network
| Metric | Value |
|--------|-------|
| Nodes | 1,005 |
| Edges | 16,385 |
| Average degree | 32.61 |
| Max degree | 212 |
| Clustering coefficient | 0.493 |
| Assortativity | 0.236 |

---

## S2. Dimension Measurement Details

### S2.1 Box-Counting Method
For each network, we used the greedy box-covering algorithm:

1. **Algorithm**: Given box size $l_B$, cover the network with minimum number of boxes
2. **Implementation**: Greedy coloring algorithm with random node selection
3. **Parameters**: 
   - Maximum box size: 5-10 (depending on network size)
   - Number of samples: 100-500 (for large networks)
   - Repetitions: 10 for statistical averaging

### S2.2 Dimension Calculation
Dimension is calculated via linear regression:
$$d_B = -\frac{\Delta \log N_B}{\Delta \log l_B}$$

where $N_B$ is the number of boxes and $l_B$ is the box size.

### S2.3 Fitting Quality
| Network | R² | Notes |
|---------|-----|-------|
| Internet AS | 0.85 | Sampling-based estimate |
| DBLP | 0.70 | Sampling-based estimate |
| Yeast PPI | 0.998 | Excellent fit (lb=1,2,3) |
| Facebook | 0.94 | Good fit |
| Twitter | 0.70 | Sampling-based estimate |
| Power Grid | 0.95 | Excellent fit |
| Email | 0.92 | Good fit |

---

## S3. Sampling Methods for Large Networks

### S3.1 Sampling Strategy
For networks with >50,000 nodes:
1. Select high-degree nodes (50% of sample)
2. Add random nodes (50% of sample)
3. Extract induced subgraph
4. Scale up estimates

### S3.2 Validation
Sampling accuracy was validated on smaller networks where full computation is feasible.

---

## S4. Computational Details

### S4.1 Hardware
- CPU: Standard x86_64 processor
- RAM: 32 GB
- Storage: 2 TB SSD

### S4.2 Software
- Python 3.x (standard library only)
- No external dependencies (numpy, scipy, networkx)
- Pure Python implementation for portability

### S4.3 Runtime
| Network | Processing Time |
|---------|-----------------|
| Internet AS | ~5 minutes (sampling) |
| DBLP | ~3 minutes (sampling) |
| Yeast PPI | ~2 minutes (full) |
| Facebook | ~10 seconds |
| Others | <1 minute each |

---

## S5. Comparison with Other Studies

### S5.1 Literature Comparison
| Network | This Study | Literature | Agreement |
|---------|-----------|------------|-----------|
| Facebook | 2.57 | ~2.5-3.0 | Good |
| Power Grid | 2.11 | ~2.0 | Excellent |
| Yeast PPI | 2.4 | ~1.5-2.0 (estimated) | Higher than expected |

### S5.2 Methodological Differences
Previous studies often used:
- Smaller samples
- Different dimension definitions
- Model networks rather than real data

Our study provides the first comprehensive empirical analysis.

---

## S6. Robustness Checks

### S6.1 Parameter Sensitivity
Dimension estimates are robust to:
- Box size range selection
- Sampling random seed
- Number of samples (for large networks)

### S6.2 Alternative Methods
Preliminary results using correlation dimension show consistent trends, though absolute values differ.

---

*Supplementary Information for: "Effective Dimensions of Complex Networks: A Large-Scale Empirical Study"*
*Last Updated: 2026-02-07*
