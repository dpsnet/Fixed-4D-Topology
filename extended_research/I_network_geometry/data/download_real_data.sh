#!/bin/bash
# Download script for real network datasets
# Run this script to download real network data

mkdir -p real_data
cd real_data

echo "Downloading real network datasets..."

# Facebook (SNAP)
echo "1. Downloading Facebook network..."
wget -O facebook_combined.txt.gz \
    https://snap.stanford.edu/data/facebook_combined.txt.gz
gunzip facebook_combined.txt.gz

# Power Grid (NetworkRepository)
echo "2. Downloading Power Grid..."
wget -O power_grid.txt \
    https://networkrepository.com/power-grid-edges.txt

# Yeast Protein (NetworkRepository)
echo "3. Downloading Yeast Protein..."
wget -O yeast_protein.txt \
    https://networkrepository.com/bio-yeast-edges.txt

echo "Done! Datasets saved in real_data/"
echo "Note: Some datasets require manual download due to terms of service"
