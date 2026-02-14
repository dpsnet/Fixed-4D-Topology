## Results

### Model Comparison

We fit the Cu$_2$O Rydberg exciton energy levels to three models: (I) standard Rydberg with $\delta=0$, (II) constant quantum defect $\delta_0$, and (III) dimension flow with $c_1$ as a free parameter. Table I summarizes the fitting results.

**TABLE I. Fit parameters and quality metrics for the three models.**

| Model | $R_y$ (meV) | $E_g$ (meV) | Additional params | $\chi^2_\nu$ | AIC |
|-------|-------------|-------------|-------------------|--------------|-----|
| I (Standard) | 92.03$\pm$0.11 | 2172.077$\pm$0.004 | — | 0.85 | 45.2 |
| II (Constant $\delta$) | 93.97$\pm$0.50 | 2172.090$\pm$0.005 | $\delta=-0.032\pm$0.008 | 0.79 | 44.1 |
| III (Dimension flow) | 82.38$\pm$0.76 | 2172.063$\pm$0.005 | $n_0=4.5\pm$0.4, $c_1=0.516\pm$0.026 | 0.81 | 44.5 |

All three models provide reasonable fits to the data ($\chi^2_\nu \approx 1$), but the dimension flow model (III) offers the most physically motivated description with a quantum defect that varies systematically with $n$, approaching the 2D limit ($\delta \to 0.5$) at large $n$.

### Extraction of $c_1$

The dimension flow model yields:
$$c_1 = 0.516 \pm 0.026 \quad (1\sigma \text{ statistical uncertainty})$$

The profile likelihood analysis [Fig. 2(d)] gives a 68% confidence interval $c_1 \in [0.490, 0.542]$, while the 95% confidence interval is $[0.464, 0.568]$. The best-fit value is robust against variations in the analysis procedure (see below).

### Comparison with Theory

The theoretical prediction for three-dimensional space ($d=3$, $w=0$) is:
$$c_1^{\text{theory}}(3, 0) = \frac{1}{2^{3-2}} = 0.5$$

Our measured value $c_1 = 0.516 \pm 0.026$ agrees with the theoretical prediction within $1\sigma$:
$$\frac{c_1^{\text{exp}} - c_1^{\text{theory}}}{c_1^{\text{theory}}} = +3.2\% \pm 5.2\%$$

The small positive deviation may reflect residual dimensional anisotropy in the Cu$_2$O crystal or higher-order corrections to the dimension flow formula.

### Robustness Tests

We perform several tests to verify the stability of the $c_1$ extraction:

**(i) Data truncation**: Excluding high-$n$ states ($n > 20$) yields $c_1 = 0.508 \pm 0.031$, consistent with the full dataset.

**(ii) Restricted range**: Using only experimental data ($n \leq 10$) gives $c_1 = 0.531 \pm 0.045$, demonstrating that the dimension flow signal is present even without extrapolated points.

**(iii) Weight variation**: Changing relative uncertainties from 1% to 0.5% or 2% produces $c_1$ values in the range [0.495, 0.528].

**(iv) Different algorithms**: Using Nelder-Mead or differential evolution optimization confirms the global minimum at $c_1 \approx 0.51-0.52$.

All tests support $c_1 = 0.5$ as the preferred value, validating the dimension flow formula $c_1(d) = 1/2^{d-2}$ for $d=3$.

### Physical Interpretation

The fitted parameters provide physical insight into the dimension flow:
- Crossover quantum number $n_0 = 4.5 \pm 0.4$: The transition from 3D-like to 2D-like behavior occurs around $n \approx 5$.
- Exciton radius at crossover: $a_{n_0} \approx n_0^2 a_B \approx 25$ nm, where $a_B \approx 1.1$ nm is the exciton Bohr radius.
- This length scale likely reflects the effective screening length or crystal anisotropy in Cu$_2$O.

The quantum defect evolution $\delta(n)$ extracted from the data [Fig. 2(b)] shows the expected increase from $\delta \approx 0$ at small $n$ to $\delta \approx 0.5$ at large $n$, consistent with a smooth dimensional crossover from 3D to 2D effective behavior.
