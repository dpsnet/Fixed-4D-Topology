#!/bin/bash
# Fixed 4D Topology Release Commands
# Run these commands to complete the GitHub release

set -e

echo "========================================"
echo "Fixed 4D Topology Release Script"
echo "========================================"
echo ""

# Check if we're in the right directory
if [ ! -f "README.md" ] || [ ! -d "src" ]; then
    echo "Error: Please run this script from the Fixed-4D-Topology directory"
    exit 1
fi

# Step 1: Check git status
echo "Step 1: Checking git status..."
git status
echo ""

# Step 2: Create and push tag
echo "Step 2: Creating version tag v1.0.0..."
git tag -a v1.0.0 -m "Release v1.0.0: Dynamic Spectral Dimension Unified Field Theory

- T1: Cantor Class Fractal Representation (L1 strict)
- T2: Spectral Dimension Evolution PDE (L1-L2)  
- T3: Modular-Fractal Weak Correspondence (L2)
- T4: Fractal Arithmetic & Grothendieck Group (L2-L3)

Complete with numerical validation and comprehensive documentation."

echo "Step 3: Pushing tag to GitHub..."
git push origin v1.0.0

echo ""
echo "========================================"
echo "Tag v1.0.0 created and pushed!"
echo "========================================"
echo ""
echo "Next steps:"
echo "1. Go to: https://github.com/dpsnet/Fixed-4D-Topology/releases"
echo "2. Click 'Draft a new release'"
echo "3. Choose tag: v1.0.0"
echo "4. Title: Release v1.0.0 - Unified Field Theory Framework"
echo "5. Copy content from RELEASE_NOTES.md"
echo "6. Publish release"
echo ""
echo "Zenodo will automatically create a DOI when you publish the release."
