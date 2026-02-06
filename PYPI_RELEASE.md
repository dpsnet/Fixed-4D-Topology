# PyPI Release Guide

## Package Information

- **Package Name**: `fixed-4d-topology`
- **Version**: 1.0.1
- **PyPI URL**: https://pypi.org/project/fixed-4d-topology/
- **TestPyPI URL**: https://test.pypi.org/project/fixed-4d-topology/

## Release Steps

### 1. Pre-release Checklist

- [ ] All tests pass: `pytest tests/`
- [ ] Version updated in:
  - `src/fixed_4d_topology/__init__.py`
  - `pyproject.toml`
  - `setup.cfg`
- [ ] CHANGELOG.md updated
- [ ] Documentation updated

### 2. Test on TestPyPI (Recommended First)

```bash
./publish_pypi.sh test
```

This will:
1. Clean previous builds
2. Run tests
3. Build package
4. Check distribution
5. Upload to TestPyPI

**Install from TestPyPI**:
```bash
pip install --index-url https://test.pypi.org/simple/ fixed-4d-topology==1.0.1
```

### 3. Release to Production PyPI

```bash
./publish_pypi.sh prod
```

**Install from PyPI**:
```bash
pip install fixed-4d-topology
```

## Manual Release (if needed)

### Build Package
```bash
python -m build
```

### Check Package
```bash
python -m twine check dist/*
```

### Upload to TestPyPI
```bash
python -m twine upload --repository testpypi dist/*
```

### Upload to PyPI
```bash
python -m twine upload dist/*
```

## Package Contents

```
fixed_4d_topology/
├── __init__.py                 # Package initialization
├── cantor_representation.py    # T1: Cantor class fractal representation
├── spectral_dimension.py       # T2: Spectral dimension evolution PDE
├── modular_correspondence.py   # T3: Modular-fractal weak correspondence
├── fractal_arithmetic.py       # T4: Fractal arithmetic & Grothendieck group
├── cli.py                      # Command-line interface
└── py.typed                    # Type information marker
```

## Dependencies

### Required
- numpy>=1.21.0
- scipy>=1.7.0
- sympy>=1.9
- matplotlib>=3.4.0
- numba>=0.56.0
- pandas>=1.3.0

### Optional (dev)
- pytest>=6.2.0
- pytest-cov>=3.0.0
- black>=21.0.0
- flake8>=4.0.0
- mypy>=0.910

## Usage Example

```python
from fixed_4d_topology import (
    CantorRepresentation,
    SpectralDimension,
    ModularCorrespondence,
    FractalArithmetic
)

# T1: Cantor representation
rep = CantorRepresentation()
result = rep.approximate(alpha=0.5, epsilon=1e-6)

# T2: Spectral dimension
spec = SpectralDimension("sierpinski")
d_s = spec.compute_spectral_dimension(t=1e-5)

# T3: Modular correspondence
corr = ModularCorrespondence()
results = corr.ramanujan.verify_correspondence()

# T4: Fractal arithmetic
arith = FractalArithmetic()
d_sum = arith.add_dimensions(d1, d2)
```

## CLI Usage

```bash
# Verify installation
fixed4d-verify

# Verbose output
fixed4d-verify --verbose

# Show version
fixed4d-verify --version
```

## Troubleshooting

### Build Issues
- Ensure `build` and `twine` are installed: `pip install build twine`
- Clean previous builds: `rm -rf build dist *.egg-info`

### Upload Issues
- Check credentials: `python -m twine check dist/*`
- For TestPyPI, use `--repository testpypi`
- Ensure version number is unique

### Installation Issues
- Check Python version: `python --version` (requires >=3.8)
- Check dependencies: `pip install -r requirements.txt`

## Post-Release

After releasing to PyPI:

1. **Tag the release**:
   ```bash
   git tag -a v1.0.1 -m "PyPI release v1.0.1"
   git push origin v1.0.1
   ```

2. **Create GitHub Release**:
   - Go to https://github.com/dpsnet/Fixed-4D-Topology/releases
   - Create new release from tag
   - Add release notes

3. **Update documentation**:
   - Update README.md with PyPI badges
   - Update installation instructions

4. **Announce**:
   - Twitter/X
   - Reddit r/Python, r/math
   - ResearchGate

## Links

- **PyPI**: https://pypi.org/project/fixed-4d-topology/
- **TestPyPI**: https://test.pypi.org/project/fixed-4d-topology/
- **GitHub**: https://github.com/dpsnet/Fixed-4D-Topology
- **Documentation**: https://github.com/dpsnet/Fixed-4D-Topology/tree/main/docs
- **Issues**: https://github.com/dpsnet/Fixed-4D-Topology/issues

---

**Last Updated**: February 2026
