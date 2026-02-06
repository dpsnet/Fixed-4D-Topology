#!/bin/bash
# Test package build locally

set -e

echo "Testing package build..."

# Clean
echo "Cleaning..."
rm -rf build/ dist/ *.egg-info src/*.egg-info

# Build
echo "Building package..."
python -m build

# Check
echo "Checking distribution..."
python -m twine check dist/*

# Show results
echo ""
echo "Build successful!"
echo ""
ls -lh dist/
echo ""

# Optional: Install locally and test
echo "Installing locally..."
pip install dist/*.whl --force-reinstall

echo ""
echo "Running verification..."
fixed4d-verify --verbose

echo ""
echo "✓ Build test passed!"
