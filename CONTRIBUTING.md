# Contributing to Fixed 4D Topology

Thank you for your interest in contributing to the Fixed 4D Topology project! This document provides guidelines for contributing.

## 🎯 Research Context

This project represents original mathematical research with multiple theory threads:

### Core Theory Threads
- **T1**: Cantor Class Fractal Representation (L1 strict)
- **T2**: Spectral Dimension PDE (L1-L2)
- **T3**: Modular-Fractal Weak Correspondence (L2)
- **T4**: Fractal Arithmetic (L2-L3)

### Extended Research Directions
- **H**: Quantum Dimension (MPS/iTEBD spin chains)
- **I**: Network Geometry (2.1M nodes empirical study)
- **J**: Random Fractals (3D percolation)

### Open Source Paper
📄 **[Dimensionics-Physics](docs/Dimensionics-Physics/paper/)**: Rigorous axiomatic framework for quantum gravity
- 9 axioms (A1-A9), 12 theorems (L1 strict), 11 predictions
- Open source on GitHub, formatted per RMP guidelines
- [Read the PDF](docs/Dimensionics-Physics/paper/Dimensionics_Physics.pdf) | [LaTeX Source](docs/Dimensionics-Physics/paper/Dimensionics_Physics.tex)

Contributions should respect the **layered strictness approach**:
- L1: 100% rigorous proofs required
- L2: Partial results with explicit assumptions
- L3: Heuristic/exploratory with numerical evidence

## 📝 Types of Contributions

### 1. Bug Reports
- Use GitHub Issues
- Include minimal reproducible example
- Specify Python version and OS

### 2. Paper Improvements
The [Dimensionics-Physics paper](docs/Dimensionics-Physics/paper/) welcomes:
- Typos and grammar fixes
- Clarifications of mathematical content
- Additional citations to related work
- Improvements to figures and visualizations
- Suggestions for new predictions or validations

See [paper/CONTRIBUTING.md](docs/Dimensionics-Physics/paper/CONTRIBUTING.md) for paper-specific guidelines.

### 3. Numerical Improvements
- Algorithm optimizations
- Better convergence methods
- Additional test cases
- Validation of predictions (P1-P11)

### 4. Documentation
- Clarifications of mathematical content
- Additional examples
- Tutorial notebooks
- Translations (if applicable)

### 5. New Theory Extensions
- Must follow strictness guidelines
- Requires explicit documentation of assumptions
- Needs numerical verification

## 🚀 Development Setup

```bash
# Clone repository
git clone https://github.com/yourusername/Fixed-4D-Topology.git
cd Fixed-4D-Topology

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e ".[dev]"

# Run tests
pytest tests/
```

## 🧪 Testing Guidelines

- All code must have corresponding tests
- Tests should verify both correctness and convergence
- Numerical tests should include tolerance specifications

```python
# Example test pattern
def test_feature():
    """Test description with mathematical context."""
    result = compute_something()
    expected = known_value
    assert abs(result - expected) < 1e-10
```

## 📐 Code Style

- Follow PEP 8
- Use black for formatting: `black src tests`
- Type hints required for public APIs
- Document mathematical foundations in docstrings

```python
def compute_dimension(
    t: float,
    fractal_type: str = "sierpinski"
) -> float:
    """
    Compute spectral dimension at time t.
    
    Based on heat kernel asymptotics:
    p(t, x, x) ~ C / t^(d_s/2)
    
    Args:
        t: Time parameter
        fractal_type: Type of fractal structure
        
    Returns:
        Spectral dimension d_s(t)
    """
    # Implementation
```

## 📚 Mathematical Content Guidelines

### When Adding Theorems

1. **L1 (Strict) Requirements**:
   - Complete proof required
   - All assumptions explicitly stated
   - References to relevant literature

2. **L2 (Progressive) Requirements**:
   - Partial results clearly labeled
   - Missing steps identified
   - Conjectures distinguished from theorems

3. **L3 (Heuristic) Requirements**:
   - Explicitly marked as exploratory
   - Numerical evidence required
   - Clear statement of what would make it rigorous

### Revision Principle

> "宁可删除，不伪造成立" (Rather delete than fake validity)

- If a proof has gaps, mark it as conjecture
- Never claim strictness without full proof
- Document known limitations explicitly

## 🔬 Pull Request Process

1. **Before Submitting**:
   - Run full test suite: `pytest tests/`
   - Check type hints: `mypy src/`
   - Format code: `black src tests`
   - Update documentation if needed

2. **PR Description**:
   - Mathematical context
   - Strictness level (L1/L2/L3)
   - Numerical verification results
   - Breaking changes (if any)

3. **Review Process**:
   - Mathematical correctness review
   - Code quality review
   - Documentation review

## 📖 Documentation Structure

```
docs/
├── Dimensionics-Physics/          # ⭐ Open source paper (RMP format)
│   └── paper/                     # Complete LaTeX source + PDF
│       ├── Dimensionics_Physics.tex
│       ├── Dimensionics_Physics.pdf
│       ├── chapters/              # 9 core chapters
│       ├── appendices/            # 2 appendices
│       └── figures/               # 7 PDF figures
├── ag-integration/                # A~G unified framework docs
│   ├── UNIFIED_FRAMEWORK_INDEX.md
│   ├── SURVEY_PAPER_FULL.md
│   └── INTEGRATION_WITH_FIXED_4D_TOPOLOGY.md
├── T1-cantor-representation/      # T1 theory paper
├── T2-spectral-dimension-pde/     # T2 theory paper
├── T3-modular-fractal-correspondence/  # T3 theory paper
├── T4-fractal-arithmetic/         # T4 theory paper
├── API.md                         # API reference
├── THEORY_GUIDE.md                # Mathematical background
└── examples/                      # Tutorial examples
```

## 🐛 Issue Templates

### Bug Report Template

```markdown
**Component**: (T1/T2/T3/T4/Core)
**Strictness Level**: (if applicable)

**Description**:
Clear description of the issue.

**Reproduction**:
Minimal code to reproduce.

**Expected Behavior**:
What should happen.

**Actual Behavior**:
What actually happens.

**Environment**:
- Python version:
- NumPy version:
- OS:
```

### Feature Request Template

```markdown
**Theory Thread**: (T1/T2/T3/T4/New)
**Strictness Target**: (L1/L2/L3)

**Description**:
What feature or theory extension?

**Mathematical Foundation**:
Key theorems or conjectures.

**Proposed Implementation**:
High-level approach.

**Verification Plan**:
How to verify correctness?
```

## 📜 License

By contributing, you agree that your contributions will be licensed under the MIT License (code) and CC BY 4.0 (mathematical content).

## 🙏 Acknowledgments

Contributors will be acknowledged in:
- RELEASE_NOTES.md for significant contributions
- Code comments for specific algorithms
- Documentation for theory extensions

---

**Questions?** Open an issue with the `question` label.
