#!/usr/bin/env python3
"""
Prepare data for paper figures (pure Python, no external dependencies)
=====================================================================

This script generates data files that can be used with:
- LaTeX pgfplots
- Python with matplotlib (when available)
- Manual plotting in other tools

Usage:
    python prepare_figure_data.py --output-dir ./figure_data/
"""

import os
import json
import math
import argparse


def generate_figure1_data():
    """Figure 1: Network Dimension Hierarchy"""
    networks = [
        {"name": "Internet AS", "dimension": 4.36, "nodes": 1696415, "type": "infrastructure"},
        {"name": "DBLP", "dimension": 3.0, "nodes": 317080, "type": "academic"},
        {"name": "Facebook", "dimension": 2.57, "nodes": 4039, "type": "social"},
        {"name": "Yeast PPI", "dimension": 2.4, "nodes": 6800, "type": "biological"},
        {"name": "Twitter", "dimension": 2.0, "nodes": 81306, "type": "social"},
        {"name": "Power Grid", "dimension": 2.11, "nodes": 101, "type": "infrastructure"},
        {"name": "Email", "dimension": 1.24, "nodes": 1133, "type": "communication"},
    ]
    return networks


def generate_figure2_data():
    """Figure 2: Variational Principle"""
    # Free energy landscape data
    A, alpha, T = 1.0, 0.5, 0.3
    
    data = {
        'dimensions': [],
        'energy': [],
        'entropy': [],
        'free_energy': []
    }
    
    for i in range(1, 60):  # d from 0.1 to 3.0
        d = 0.1 + i * 0.05
        energy = A / (d ** alpha)
        entropy = T * d * math.log(d)
        free_energy = energy + entropy
        
        data['dimensions'].append(round(d, 3))
        data['energy'].append(round(energy, 4))
        data['entropy'].append(round(entropy, 4))
        data['free_energy'].append(round(free_energy, 4))
    
    # Temperature dependence data
    data['temperatures'] = []
    data['optimal_dimensions'] = []
    
    for i in range(1, 20):
        T_val = 0.05 + i * 0.05
        # Find optimal dimension numerically (simplified)
        best_d = 1.0
        best_F = float('inf')
        for j in range(1, 100):
            d = 0.1 + j * 0.05
            F = A / (d ** alpha) + T_val * d * math.log(d)
            if F < best_F:
                best_F = F
                best_d = d
        
        data['temperatures'].append(round(T_val, 3))
        data['optimal_dimensions'].append(round(best_d, 3))
    
    return data


def generate_figure3_data():
    """Figure 3: Model Comparison"""
    networks = [
        {"name": "Internet AS", "empirical": 4.36, "ba": 1.0, "ws": 1.0},
        {"name": "DBLP", "empirical": 3.0, "ba": 1.0, "ws": 1.0},
        {"name": "Yeast PPI", "empirical": 2.4, "ba": 1.0, "ws": 1.0},
        {"name": "Facebook", "empirical": 2.57, "ba": 1.0, "ws": 1.0},
        {"name": "Twitter", "empirical": 2.0, "ba": 1.0, "ws": 1.0},
        {"name": "Power Grid", "empirical": 2.11, "ba": 1.0, "ws": 1.0},
        {"name": "Email", "empirical": 1.24, "ba": 1.0, "ws": 1.0},
    ]
    return networks


def generate_latex_pgfplots():
    """Generate LaTeX pgfplots code for figures"""
    
    # Figure 1: Network Hierarchy
    fig1_latex = r'''%% Figure 1: Network Dimension Hierarchy
%% Auto-generated - Do not edit manually
\begin{tikzpicture}
\begin{axis}[
    xbar,
    width=10cm,
    height=8cm,
    xlabel={Effective Dimension},
    title={Network Dimension Hierarchy (7 Networks, 2.1M Nodes)},
    symbolic y coords={Email, Power Grid, Twitter, Yeast PPI, Facebook, DBLP, Internet AS},
    ytick=data,
    nodes near coords,
    nodes near coords align={horizontal},
    enlarge y limits=0.1,
    xmax=5,
    legend style={at={(0.98,0.3)},anchor=east},
]
\addplot[fill=red!60] coordinates {(4.36,Internet AS) (2.11,Power Grid)};
\addplot[fill=blue!60] coordinates {(3.0,DBLP)};
\addplot[fill=green!60] coordinates {(2.57,Facebook) (2.0,Twitter)};
\addplot[fill=purple!60] coordinates {(2.4,Yeast PPI)};
\addplot[fill=orange!60] coordinates {(1.24,Email)};
\legend{Infrastructure, Academic, Social, Biological, Communication}
\end{axis}
\end{tikzpicture}
'''
    
    return {'figure1.tex': fig1_latex}


def main():
    parser = argparse.ArgumentParser(description='Prepare figure data')
    parser.add_argument('--output-dir', default='./figure_data/',
                       help='Output directory for data files')
    args = parser.parse_args()
    
    os.makedirs(args.output_dir, exist_ok=True)
    
    print("Preparing figure data...")
    print("=" * 50)
    
    # Generate data files
    fig1_data = generate_figure1_data()
    with open(os.path.join(args.output_dir, 'figure1_data.json'), 'w') as f:
        json.dump(fig1_data, f, indent=2)
    print(f"✓ Figure 1 data: {len(fig1_data)} networks")
    
    fig2_data = generate_figure2_data()
    with open(os.path.join(args.output_dir, 'figure2_data.json'), 'w') as f:
        json.dump(fig2_data, f, indent=2)
    print(f"✓ Figure 2 data: variational principle ({len(fig2_data['dimensions'])} points)")
    
    fig3_data = generate_figure3_data()
    with open(os.path.join(args.output_dir, 'figure3_data.json'), 'w') as f:
        json.dump(fig3_data, f, indent=2)
    print(f"✓ Figure 3 data: model comparison ({len(fig3_data)} networks)")
    
    # Generate CSV files for easy import
    with open(os.path.join(args.output_dir, 'figure1_data.csv'), 'w') as f:
        f.write("name,dimension,nodes,type\n")
        for net in fig1_data:
            f.write(f"{net['name']},{net['dimension']},{net['nodes']},{net['type']}\n")
    print("✓ Figure 1 CSV created")
    
    with open(os.path.join(args.output_dir, 'figure2_data.csv'), 'w') as f:
        f.write("dimension,energy,entropy,free_energy\n")
        for i in range(len(fig2_data['dimensions'])):
            f.write(f"{fig2_data['dimensions'][i]},{fig2_data['energy'][i]},{fig2_data['entropy'][i]},{fig2_data['free_energy'][i]}\n")
    print("✓ Figure 2 CSV created")
    
    # Generate LaTeX pgfplots
    latex_code = generate_latex_pgfplots()
    for filename, code in latex_code.items():
        with open(os.path.join(args.output_dir, filename), 'w') as f:
            f.write(code)
    print("✓ LaTeX pgfplots code created")
    
    print("=" * 50)
    print(f"✓ All data files saved to: {args.output_dir}")
    print("\nUsage:")
    print("  - JSON files: For Python/Matplotlib scripts")
    print("  - CSV files: For Excel/R/MATLAB")
    print("  - .tex files: For direct LaTeX inclusion")


if __name__ == '__main__':
    main()
