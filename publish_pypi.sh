#!/bin/bash
# PyPI Release Script for Fixed 4D Topology
# Usage: ./publish_pypi.sh [test|prod]

set -e

VERSION="1.0.1"
PACKAGE_NAME="fixed-4d-topology"

echo "========================================"
echo "PyPI Release Script"
echo "========================================"
echo "Package: $PACKAGE_NAME"
echo "Version: $VERSION"
echo ""

# Check arguments
if [ $# -eq 0 ]; then
    echo "Usage: ./publish_pypi.sh [test|prod]"
    echo ""
    echo "Options:"
    echo "  test  - Upload to TestPyPI (recommended first)"
    echo "  prod  - Upload to production PyPI"
    echo ""
    exit 1
fi

TARGET=$1

# Clean previous builds
echo "Step 1: Cleaning previous builds..."
rm -rf build/ dist/ *.egg-info
rm -rf src/*.egg-info
find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
find . -type f -name "*.pyc" -delete 2>/dev/null || true
echo "✓ Cleaned"
echo ""

# Run tests (if pytest is available)
echo "Step 2: Running tests..."
if python -m pytest --version > /dev/null 2>&1; then
    python -m pytest tests/ -q --tb=short
    if [ $? -ne 0 ]; then
        echo "✗ Tests failed! Aborting."
        exit 1
    fi
    echo "✓ Tests passed"
else
    echo "⚠ pytest not available, skipping tests"
    echo "  (run 'pip install pytest' to enable testing)"
fi
echo ""

# Build package
echo "Step 3: Building package..."
python -m build
if [ $? -ne 0 ]; then
    echo "✗ Build failed!"
    exit 1
fi
echo "✓ Build successful"
echo ""

# Check distribution
echo "Step 4: Checking distribution..."
python -m twine check dist/*
if [ $? -ne 0 ]; then
    echo "✗ Distribution check failed!"
    exit 1
fi
echo "✓ Distribution check passed"
echo ""

# Show package info
echo "Step 5: Package info..."
ls -lh dist/
echo ""

# Upload based on target
if [ "$TARGET" = "test" ]; then
    echo "Step 6: Uploading to TestPyPI..."
    echo "URL: https://test.pypi.org/project/$PACKAGE_NAME/"
    python -m twine upload --repository testpypi dist/*
    
    echo ""
    echo "========================================"
    echo "TestPyPI Upload Complete!"
    echo "========================================"
    echo ""
    echo "Install with:"
    echo "pip install --index-url https://test.pypi.org/simple/ $PACKAGE_NAME==$VERSION"
    echo ""
    
elif [ "$TARGET" = "prod" ]; then
    echo "Step 6: Uploading to Production PyPI..."
    echo "URL: https://pypi.org/project/$PACKAGE_NAME/"
    echo ""
    read -p "Are you sure you want to upload to production PyPI? (yes/no): " confirm
    if [ "$confirm" = "yes" ]; then
        python -m twine upload dist/*
        
        echo ""
        echo "========================================"
        echo "PyPI Upload Complete!"
        echo "========================================"
        echo ""
        echo "Install with:"
        echo "pip install $PACKAGE_NAME"
        echo ""
        echo "PyPI page: https://pypi.org/project/$PACKAGE_NAME/"
        echo ""
    else
        echo "Upload cancelled."
        exit 0
    fi
else
    echo "✗ Unknown target: $TARGET"
    echo "Use 'test' or 'prod'"
    exit 1
fi

echo "Done!"
