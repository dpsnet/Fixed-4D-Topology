#!/bin/bash
# Development environment setup script
# Usage: bash setup_dev.sh

echo "========================================"
echo "Setting up Fixed-4D-Topology Dev Environment"
echo "========================================"

# Check Python version
python3 --version

# Create virtual environment (optional but recommended)
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate || . venv/Scripts/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install core dependencies
echo "Installing core dependencies..."
pip install numpy scipy matplotlib pandas

# Install Jupyter
echo "Installing Jupyter..."
pip install jupyter ipython

# Install testing tools
echo "Installing testing tools..."
pip install pytest pytest-cov

# Install optional dependencies
echo "Installing optional dependencies..."
pip install networkx seaborn

# Verify installation
echo ""
echo "Verifying installation..."
python3 << 'EOF'
import sys
try:
    import numpy as np
    print(f"✓ NumPy {np.__version__}")
    
    import scipy
    print(f"✓ SciPy {scipy.__version__}")
    
    import matplotlib
    print(f"✓ Matplotlib {matplotlib.__version__}")
    
    import pandas as pd
    print(f"✓ Pandas {pd.__version__}")
    
    import jupyter
    print(f"✓ Jupyter installed")
    
    import pytest
    print(f"✓ Pytest installed")
    
    print("\n✅ All dependencies installed successfully!")
    sys.exit(0)
except ImportError as e:
    print(f"\n❌ Error: {e}")
    sys.exit(1)
EOF

echo ""
echo "========================================"
echo "Setup complete!"
echo "========================================"
echo ""
echo "To activate the environment:"
echo "  source venv/bin/activate  (Linux/Mac)"
echo "  venv\Scripts\activate     (Windows)"
echo ""
echo "To generate figures:"
echo "  python scripts/generate_figures.py"
echo ""
echo "To run tests:"
echo "  python -m pytest tests/ -v"
