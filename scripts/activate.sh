#!/bin/bash
# Activate script for Dimensionics Framework virtual environment
# Usage: source scripts/activate.sh

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$( cd "$SCRIPT_DIR/.." && pwd )"
VENV_PATH="${PROJECT_ROOT}/venv"

if [ ! -d "$VENV_PATH" ]; then
    echo "Error: Virtual environment not found at $VENV_PATH"
    echo "Run: python setup_env.py"
    return 1
fi

if [ -f "${VENV_PATH}/bin/activate" ]; then
    source "${VENV_PATH}/bin/activate"
    echo "✓ Virtual environment activated"
    echo "  Python: $(which python)"
    echo "  Version: $(python --version)"
    
    # Add src to PYTHONPATH
    export PYTHONPATH="${PROJECT_ROOT}/src:${PYTHONPATH}"
    echo "  PYTHONPATH updated"
else
    echo "Error: Could not find activation script"
    return 1
fi
