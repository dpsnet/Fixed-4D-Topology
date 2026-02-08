# Virtual Environment Guide
## Dimensionics Framework

---

## Quick Start

### Option 1: Automated Setup (Recommended)

```bash
# Basic setup (includes numpy, scipy, matplotlib, jupyter)
python setup_env.py

# Development setup (includes all dev tools)
python setup_env.py --dev

# Minimal setup (only core scientific libraries)
python setup_env.py --minimal
```

### Option 2: Manual Setup

```bash
# Create virtual environment
python3 -m venv venv

# Activate (Linux/macOS)
source venv/bin/activate

# Activate (Windows)
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

---

## Activation

### Using Helper Scripts

**Linux/macOS:**
```bash
source scripts/activate.sh
```

**Windows:**
```cmd
scripts\activate.bat
```

### Manual Activation

**Linux/macOS:**
```bash
source venv/bin/activate
```

**Windows (CMD):**
```cmd
venv\Scripts\activate.bat
```

**Windows (PowerShell):**
```powershell
venv\Scripts\Activate.ps1
```

### Deactivation

```bash
deactivate
```

---

## Jupyter Notebook Setup

### Automatic Kernel Installation

The setup script automatically installs a Jupyter kernel:

```bash
python setup_env.py
jupyter notebook
# Select kernel: "Python (Dimensionics)"
```

### Manual Kernel Installation

```bash
# Activate environment
source venv/bin/activate

# Install kernel
python -m ipykernel install --user --name=dimensionics --display-name "Python (Dimensionics)"

# Launch Jupyter
jupyter notebook
```

### Verify Kernel

```bash
jupyter kernelspec list
```

---

## Dependency Management

### Install New Packages

```bash
# Activate environment first
source venv/bin/activate

# Install package
pip install package_name

# Update requirements.txt
pip freeze > requirements.txt
```

### Update All Packages

```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

### Development Dependencies

```bash
# Install dev tools
pip install -r requirements-dev.txt
```

---

## Troubleshooting

### Issue: "No module named 'venv'"

**Ubuntu/Debian:**
```bash
sudo apt-get install python3-venv
```

**RHEL/CentOS/Fedora:**
```bash
sudo yum install python3-virtualenv
```

**macOS:**
```bash
brew install python3  # venv included
```

### Issue: Permission Denied (Linux/macOS)

Make scripts executable:
```bash
chmod +x scripts/activate.sh
chmod +x setup_env.py
```

### Issue: Command Not Found (Windows)

Run as Administrator or use:
```cmd
py setup_env.py
```

### Issue: Jupyter Kernel Not Found

```bash
# Reinstall kernel
python -m ipykernel install --user --name=dimensionics --force

# Verify
jupyter kernelspec list
```

### Issue: Module Import Errors

Ensure `src` is in PYTHONPATH:
```bash
# In activated environment
export PYTHONPATH="${PWD}/src:${PYTHONPATH}"
```

Or use the helper script which sets this automatically:
```bash
source scripts/activate.sh
```

---

## Environment Configuration

### Custom Environment Path

```bash
python setup_env.py --path /path/to/custom/env
```

### Force Recreation

```bash
# Remove existing and create new
python setup_env.py --force
```

### Minimal Installation

For servers or CI/CD:
```bash
python setup_env.py --minimal
```

---

## IDE Integration

### VS Code

1. Open project in VS Code
2. Press `Ctrl+Shift+P` (or `Cmd+Shift+P` on macOS)
3. Type "Python: Select Interpreter"
4. Choose `./venv/bin/python` (or `venv\Scripts\python.exe` on Windows)

Settings (`.vscode/settings.json`):
```json
{
    "python.defaultInterpreterPath": "./venv/bin/python",
    "python.analysis.extraPaths": ["./src"],
    "jupyter.askForKernelRestart": false
}
```

### PyCharm

1. File → Settings → Project → Python Interpreter
2. Click gear icon → Add
3. Select "Existing environment"
4. Navigate to `venv/bin/python`

---

## Docker Alternative

If you prefer Docker:

```dockerfile
FROM python:3.10-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
ENV PYTHONPATH=/app/src

CMD ["jupyter", "notebook", "--ip=0.0.0.0", "--allow-root"]
```

Build and run:
```bash
docker build -t dimensionics .
docker run -p 8888:8888 -v $(pwd):/app dimensionics
```

---

## CI/CD Configuration

### GitHub Actions

```yaml
name: Test
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
      - name: Run tests
        run: pytest
```

---

## Best Practices

1. **Always activate** environment before working
2. **Never commit** the `venv/` directory (it's in `.gitignore`)
3. **Update requirements.txt** after installing new packages
4. **Use helper scripts** to ensure PYTHONPATH is set correctly
5. **Test imports** after setup:
   ```bash
   python -c "from unified_framework import Dimension; print('OK')"
   ```

---

## Environment Variables

Optional environment variables:

```bash
# Disable compiled extensions (for debugging)
export PYTHONDONTWRITEBYTECODE=1

# Enable development mode
export DIMENSIONICS_DEBUG=1

# Custom data directory
export DIMENSIONICS_DATA_DIR=/path/to/data
```

---

**Last Updated**: February 8, 2026
