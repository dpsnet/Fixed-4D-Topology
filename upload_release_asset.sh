#!/bin/bash
# Upload PDF asset to GitHub Release v3.1.0-paper
# Usage: ./upload_release_asset.sh YOUR_GITHUB_TOKEN

TOKEN=$1
if [ -z "$TOKEN" ]; then
    echo "Usage: ./upload_release_asset.sh YOUR_GITHUB_TOKEN"
    exit 1
fi

# Get release ID
RELEASE_ID=$(curl -s -H "Authorization: token $TOKEN" \
  https://api.github.com/repos/dpsnet/Fixed-4D-Topology/releases/tags/v3.1.0-paper | \
  grep -o '"id": [0-9]*' | head -1 | grep -o '[0-9]*')

echo "Release ID: $RELEASE_ID"

# Upload PDF
curl -X POST \
  -H "Authorization: token $TOKEN" \
  -H "Content-Type: application/pdf" \
  --data-binary @docs/research/spectral_flow/unified_theory/rmp_review_paper/output/main_80pages.pdf \
  "https://uploads.github.com/repos/dpsnet/Fixed-4D-Topology/releases/$RELEASE_ID/assets?name=main_80pages.pdf"

echo "PDF uploaded successfully!"
