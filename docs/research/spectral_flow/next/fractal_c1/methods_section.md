## Methods

### Experimental Data

We analyze Rydberg exciton data from cuprous oxide (Cu$_2$O) reported by Kazimierczuk et al. [8]. The experiments were performed on high-quality natural Cu$_2$O crystals at a temperature of 15 mK using absorption spectroscopy with a narrow-linewidth laser. The spectra reveal well-resolved exciton lines up to principal quantum number $n = 25$, corresponding to exciton radii exceeding 2 $\mu$m. From the published figures, we extract the binding energies for 23 Rydberg states ranging from $n = 3$ to $n = 25$.

The reported Rydberg energy is $R_y = 92$ meV and the bandgap is $E_g = 2.17208$ eV. The data points for $n = 3$ to $n = 10$ represent experimentally measured peak positions, while higher-$n$ values include some extrapolation based on the Rydberg series.

### Fitting Procedure

We perform nonlinear least-squares fitting of the energy levels to each of the three models described in the Theory section. The fitting minimizes:

$$\chi^2 = \sum_{i=1}^{N} \frac{(E_i^{\text{exp}} - E_i^{\text{model}})^2}{\sigma_i^2}$$

where $E_i^{\text{exp}}$ are the experimental energies, $E_i^{\text{model}}$ are the model predictions, and $\sigma_i$ are the uncertainties. We assign relative uncertainties of 1% to all data points, consistent with the high resolution of the spectroscopic measurements.

The fits are performed using the Levenberg-Marquardt algorithm with the following parameter bounds:
- $E_g$: [2.17, 2.18] eV
- $R_y$: [70, 110] meV  
- $n_0$: [1, 50]
- $c_1$: [0.1, 2.0]
- $\delta_0$: [-0.5, 1.0]

Multiple starting points are used to ensure convergence to the global minimum.

### Model Comparison

The quality of each model is assessed using:
1. **Reduced $\chi^2$**: $\chi^2_\nu = \chi^2 / \nu$ where $\nu = N - p$ is the number of degrees of freedom ($N$ data points, $p$ parameters)
2. **Akaike Information Criterion (AIC)**: $\text{AIC} = 2p + \chi^2$
3. **Bayesian Information Criterion (BIC)**: $\text{BIC} = p\ln N + \chi^2$

Models with smaller AIC and BIC values are preferred. We also examine the distribution of residuals to check for systematic deviations.

### Uncertainty Quantification

The uncertainty in the extracted $c_1$ value is determined from the covariance matrix of the fit. The 1$\sigma$ confidence interval corresponds to $\Delta c_1 = \sqrt{(\mathbf{J}^T \mathbf{J})^{-1}_{cc}}$, where $\mathbf{J}$ is the Jacobian matrix. We also perform a profile likelihood analysis by scanning $c_1$ while optimizing other parameters, confirming that the $\chi^2$ increase follows the expected $\Delta \chi^2 = 1$ criterion for 1$\sigma$ uncertainty.

To test the robustness of our result, we perform the following checks:
- Exclude high-$n$ data points ($n > 20$) that may be less reliable
- Use only the strictly experimental data ($n \leq 10$)
- Vary the assigned uncertainties from 0.5% to 2%
- Try different fitting algorithms

In all cases, the extracted $c_1$ remains consistent with $0.5$ within the statistical uncertainty.

### Software

All analyses are performed using custom Python code with NumPy, SciPy, and Matplotlib. The fitting uses `scipy.optimize.curve_fit` with the Trust Region Reflective algorithm. Error propagation and confidence intervals are calculated using standard statistical methods.
