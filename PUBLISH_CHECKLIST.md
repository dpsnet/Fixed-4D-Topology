# GitHub Release Checklist

## Pre-Release Verification

### Code Quality
- [ ] All tests pass: `pytest tests/ -v`
- [ ] Type checking passes: `mypy src/fixed_4d_topology`
- [ ] Code formatted: `black src tests --check`
- [ ] Linting passes: `flake8 src tests`
- [ ] No TODO markers in code

### Documentation
- [ ] README.md complete and accurate
- [ ] API.md up to date
- [ ] All examples run successfully
- [ ] RELEASE_NOTES.md updated
- [ ] Version numbers consistent

### Repository Structure
- [ ] LICENSE file present
- [ ] CITATION.cff valid
- [ ] .gitignore configured
- [ ] requirements.txt complete
- [ ] pyproject.toml valid

## GitHub Setup

### Repository Creation
```bash
# Create new repository on GitHub
cd Fixed-4D-Topology
git init
git add .
git commit -m "Initial release v1.0.0"
git branch -M main
git remote add origin https://github.com/dpsnet/Fixed-4D-Topology.git
git push -u origin main
```

### Repository Settings
- [ ] Enable Issues
- [ ] Enable Discussions
- [ ] Set up branch protection for main
- [ ] Enable GitHub Pages (for docs)
- [ ] Add topics/tags
- [ ] Set social preview image

### GitHub Actions
- [ ] CI workflow running
- [ ] Tests passing on all Python versions
- [ ] Documentation building

## PyPI Release (Optional)

```bash
# Build package
python -m build

# Upload to PyPI
python -m twine upload dist/*
```

- [ ] Package builds successfully
- [ ] TestPyPI upload works
- [ ] PyPI upload completed

## Documentation Hosting

### Read the Docs
- [ ] Account created
- [ ] Project imported
- [ ] .readthedocs.yml configured
- [ ] Build successful
- [ ] Custom domain configured (optional)

### GitHub Pages
- [ ] docs/_build/html deployed
- [ ] Custom domain configured (optional)

## Post-Release

### Announcements
- [ ] Twitter/X announcement
- [ ] Reddit r/math post
- [ ] Academic mailing lists
- [ ] ResearchGate update

### Zenodo DOI
```bash
# Create release on GitHub
# Zenodo will automatically create DOI
```

- [ ] Release created on GitHub
- [ ] Zenodo webhook triggered
- [ ] DOI obtained and added to README

### Citation Updates
- [ ] CITATION.cff updated with DOI
- [ ] README.md updated with DOI
- [ ] arXiv preprint linked

## Version History

| Version | Date | Description |
|---------|------|-------------|
| 1.0.0 | 2026-02-07 | Initial release with T1-T4 |

---

**Release Manager**: AI Research Engine
**Release Date**: 2026-02-07
