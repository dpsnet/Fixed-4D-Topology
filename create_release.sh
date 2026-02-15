#!/bin/bash
# Create GitHub Release v3.1.0-paper
# Usage: ./create_release.sh YOUR_GITHUB_TOKEN

TOKEN=$1
if [ -z "$TOKEN" ]; then
    echo "Usage: ./create_release.sh YOUR_GITHUB_TOKEN"
    exit 1
fi

# Create release
curl -X POST \
  -H "Authorization: token $TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  https://api.github.com/repos/dpsnet/Fixed-4D-Topology/releases \
  -d '{
    "tag_name": "v3.1.0-paper",
    "name": "v3.1.0-paper: Open Source RMP Review Paper",
    "body": "## 📄 Paper: Spectral Flow as Energy-Dependent Mode Constraint\n\n**Published**: February 15, 2026\n**Authors**: Wang Bin (Independent Researcher), Kimi 2.5 Agent\n**License**: MIT License\n\n### 📊 Paper Statistics\n- **Pages**: 88 pages\n- **Figures**: 21 high-resolution research figures\n- **File Size**: 1.2 MB\n- **References**: 228 citations\n\n### 🎯 Key Contributions\n1. **Unified Formula**: c₁(d,w) = 1/2^{d-2+w}\n2. **E-6 Experiment**: Classical tabletop demonstration\n3. **Non-Commutative/Fractal Integration**\n4. **Experimental Validation**: Cu₂O c₁ = 0.516 ± 0.026\n\n### 📥 Download\n- Paper PDF: docs/research/spectral_flow/unified_theory/rmp_review_paper/output/main_80pages.pdf\n\n### 📚 Full Release Notes\nSee [RELEASE_v3.1.0-paper.md](RELEASE_v3.1.0-paper.md)",
    "draft": false,
    "prerelease": false
  }'

echo "Release created successfully!"
