## Theory

### Dimension Flow Model

The effective dimension experienced by a physical system can vary with the characteristic length scale $\ell$. We describe this dimension flow through the spectral dimension $d_s(\ell)$, which evolves from a maximum value $d_{max}$ at small scales to a minimum value $d_{min}$ at large scales. The crossover is governed by the parameter $c_1$ according to:

$$d_{\text{eff}}(\ell) = d_{min} + \frac{d_{max} - d_{min}}{1 + (\ell_0/\ell)^{1/c_1}}$$

where $\ell_0$ is the characteristic length scale of the dimensional crossover. The parameter $c_1$ quantifies the speed of dimension flow: smaller $c_1$ corresponds to a more gradual transition, while larger $c_1$ indicates a sharper crossover.

For a $d$-dimensional space with time treated as an external parameter (non-relativistic regime, $w=0$), information-theoretic considerations yield:

$$c_1(d, w=0) = \frac{1}{2^{d-2}}$$

This formula reflects that information density decreases by a factor of two for each additional spatial dimension relative to the four-dimensional baseline. For three-dimensional systems such as Cu$_2$O, we expect $c_1(3) = 1/2^{3-2} = 0.5$.

### WKB Energy Level Formula

For Rydberg excitons, the principal quantum number $n$ is inversely related to the characteristic length scale: $\ell \sim n^2 a_B$, where $a_B$ is the Bohr radius. Substituting into the dimension flow equation with $d_{max} = 3$ and $d_{min} = 2$, we obtain:

$$d_{\text{eff}}(n) = 2 + \frac{1}{1 + (n/n_0)^{1/c_1}}$$

where $n_0$ is the crossover quantum number.

The quantum defect $\delta(n)$, which describes the deviation from the hydrogenic Rydberg series, can be related to the effective dimension through:

$$\delta(n) = \frac{1}{2}(3 - d_{\text{eff}}(n)) = \frac{0.5}{1 + (n_0/n)^{1/c_1}}$$

This shows that $\delta(n)$ increases from near zero at small $n$ (3D-like behavior) toward 0.5 at large $n$ (2D-like behavior).

Using the WKB approximation for the radial Schrödinger equation with the dimension-dependent potential, the energy levels are given by:

$$E_n = E_g - \frac{R_y}{(n - \delta(n))^2}$$

where $E_g$ is the bandgap energy and $R_y$ is the Rydberg energy. Expanding this expression:

$$E_n = E_g - \frac{R_y}{\left[n - \frac{0.5}{1 + (n_0/n)^{1/c_1}}\right]^2}$$

This formula contains four fitting parameters: $E_g$, $R_y$, $n_0$, and $c_1$, the last being the quantity of primary interest.

### Comparison Models

To validate the dimension flow model, we compare it against two simpler approaches:

**Model I: Standard Rydberg (hydrogenic)**
$$E_n = E_g - \frac{R_y}{n^2}$$
This assumes $\delta = 0$ for all $n$, corresponding to pure 3D Coulomb potential.

**Model II: Constant Quantum Defect**
$$E_n = E_g - \frac{R_y}{(n - \delta_0)^2}$$
Here $\delta_0$ is a constant, representing an energy-independent deviation from the hydrogenic spectrum.

**Model III: Dimension Flow (our approach)**
$$E_n = E_g - \frac{R_y}{(n - \delta(n))^2}$$
with $\delta(n)$ given by the dimension flow equation above.

The quality of fit for each model is assessed using the $\chi^2$ statistic, allowing us to determine whether the dimension flow model provides a significantly better description of the data and to extract the value of $c_1$.
