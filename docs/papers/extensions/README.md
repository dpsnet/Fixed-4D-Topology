# Extension Papers (H-K)

4 papers extending the core theory to quantum systems, networks, fractals, and machine learning.

## H: Quantum Dimension

**Topic**: Quantum entanglement and dimension using iTEBD

**Directory**: [extended_research/H_quantum_dimension/](../../extended_research/H_quantum_dimension/)

**Key Results**:
- iTEBD simulations with N=200 sites
- Quantum dimension scaling analysis
- Connection to Bridge C (unitary equivalence)

**Files**:
- PDF: `paper/paper.pdf`
- TeX: `paper/paper.tex`
- Theory: `theory/quantum_dimension_theory.md`

**Bridge Connection**: 
- Validates Bridge C: H_NN = U·L·U†
- Quantum-classical correspondence

---

## I: Network Geometry

**Topic**: Spectral dimension in complex networks

**Directory**: [extended_research/I_network_geometry/](../../extended_research/I_network_geometry/)

**Key Results**:
- 2.1M nodes analyzed across 7 networks
- Network spectral dimension formula
- Small-world and scale-free properties

**Files**:
- PDF: `paper/paper.pdf`
- TeX: `paper/paper.tex`
- Data: Network datasets in `data/`

**Bridge Connection**:
- Validates Bridge B: w_i ∝ 1/|λ_i|
- Network Laplacian analysis

---

## J: Random Fractals

**Topic**: Percolation and random fractal structures

**Directory**: [extended_research/J_random_fractals/](../../extended_research/J_random_fractals/)

**Key Results**:
- 3D percolation analysis
- Critical exponent verification
- Random Cantor sets

**Files**:
- PDF: `paper/paper.pdf`
- TeX: `paper/paper.tex`
- Simulations: Percolation code

**Bridge Connection**:
- Validates Bridge A: C* formula
- Critical behavior analysis

---

## K: Machine Learning

**Topic**: Effective dimension of neural networks

**Directory**: [extended_research/K_machine_learning_dimension/](../../extended_research/K_machine_learning_dimension/)

**Key Results**:
- d_eff/N = 20-28% across architectures
- Fisher information approach
- Generalization bounds

**Files**:
- Main: `paper/neurips_submission/main.pdf` (6 pages)
- Supplementary: `paper/neurips_submission/supplementary_materials.pdf` (3 pages)
- Code: Neural network analysis scripts

**Venue**: NeurIPS 2026 Submission

**Bridge Connection**:
- Applications of Bridge B
- Network weight formulas in practice

---

## Summary

| Paper | Data Scale | Bridge | Status |
|-------|-----------|--------|--------|
| H | N=200 sites | C | ✅ Complete |
| I | 2.1M nodes | B | ✅ Complete |
| J | 3D percolation | A | ✅ Complete |
| K | Multiple NN architectures | B | ✅ Complete |

All extension papers complete with tex+pdf ✅
