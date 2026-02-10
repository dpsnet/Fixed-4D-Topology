# T2: Master Equation & Spectral PDE

## Overview

**Theory**: Master equation governing dimension flow and spectral PDE theory.

## Key Results

- **Master Equation**: d_eff = argmin[E - T·S + Λ]
- **Spectral Formula**: d_s(t) = n - (R/3)t + O(t²)
- **Flow Behavior**: UV → d=2, IR → d=4

## Documents

| Type | Location | Status |
|------|----------|--------|
| **Main Paper** | [papers/T2-spectral-dimension-pde/](../../../papers/T2-spectral-dimension-pde/) | ✅ Complete |

## Code ([code/](code/))

| File | Description |
|------|-------------|
| `stability_analysis.py` | Stability analysis of solutions |
| `piecewise_flow_solver.py` | Piecewise flow equation solver |
| `modified_master_solver.py` | Modified equation solver |
| `phase_transition_analysis.py` | Phase transition study |
| `cosmological_simulations.py` | Cosmology applications |
| `black_hole_physics.py` | Black hole thermodynamics |
| `gravitational_waves_pbh.py` | GW from primordial BHs |
| `gw_predictions_paper.py` | GW predictions |
| `reversed_flow_solver.py` | Reverse flow analysis |

## Key Formulas

```
Master Equation: d_eff = argmin[E(d) - T·S(d) + Λ(d)]
Spectral: d_s(t) = n - (R/3)t + O(t²)
```

## Status

🟢 Complete - Foundation for all bridges
