"""
Result analysis and visualization for experiments.
"""

import json
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import pandas as pd


class ResultAnalyzer:
    """
    Analyze and visualize experiment results.
    """
    
    def __init__(self, results_dir: str):
        """
        Initialize analyzer.
        
        Args:
            results_dir: Directory containing experiment results
        """
        self.results_dir = Path(results_dir)
        self.results = {}
    
    def load_experiment(self, experiment_name: str) -> Dict:
        """
        Load experiment results from JSON.
        
        Args:
            experiment_name: Name of experiment (e.g., 'E1', 'E2')
            
        Returns:
            Results dictionary
        """
        # Look for JSON files in results subdirectories
        for subdir in self.results_dir.iterdir():
            if subdir.is_dir():
                json_files = list(subdir.glob('*.json'))
                for json_file in json_files:
                    if experiment_name in json_file.name:
                        with open(json_file, 'r') as f:
                            self.results[experiment_name] = json.load(f)
                        return self.results[experiment_name]
        
        raise FileNotFoundError(f"Results for {experiment_name} not found")
    
    def load_all(self) -> Dict:
        """
        Load all experiment results.
        
        Returns:
            Dictionary of all results
        """
        for subdir in self.results_dir.iterdir():
            if subdir.is_dir():
                json_files = list(subdir.glob('*.json'))
                for json_file in json_files:
                    exp_name = json_file.stem.split('_')[0]
                    try:
                        with open(json_file, 'r') as f:
                            self.results[exp_name] = json.load(f)
                    except:
                        pass
        
        return self.results
    
    def compare_dimensions(self, save_path: Optional[str] = None):
        """
        Compare effective dimensions across experiments.
        
        Args:
            save_path: Path to save figure
        """
        if not self.results:
            self.load_all()
        
        # Extract dimensions from each experiment
        dimensions = {}
        
        for exp_name, result in self.results.items():
            if 'd_eff' in result:
                dimensions[exp_name] = result['d_eff']
            elif 'd_eff_fisher' in result:
                dimensions[exp_name] = result['d_eff_fisher']
            elif 'fisher_effective_dimension' in result:
                dimensions[exp_name] = result['fisher_effective_dimension']
        
        if not dimensions:
            print("No dimension data found")
            return
        
        # Plot
        fig, ax = plt.subplots(figsize=(10, 6))
        
        exp_names = list(dimensions.keys())
        d_effs = [dimensions[name] for name in exp_names]
        
        colors = plt.cm.viridis(np.linspace(0, 1, len(exp_names)))
        ax.bar(exp_names, d_effs, color=colors)
        ax.set_ylabel('Effective Dimension', fontsize=12)
        ax.set_title('Effective Dimension Comparison Across Experiments', fontsize=14)
        ax.grid(True, alpha=0.3, axis='y')
        
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        return fig
    
    def generate_summary_table(self) -> pd.DataFrame:
        """
        Generate summary table of all results.
        
        Returns:
            Pandas DataFrame with summary
        """
        if not self.results:
            self.load_all()
        
        summary = []
        
        for exp_name, result in self.results.items():
            row = {'Experiment': exp_name}
            
            # Extract key metrics
            if 'd_eff' in result or 'd_eff_fisher' in result:
                d_eff = result.get('d_eff', result.get('d_eff_fisher'))
                row['d_eff'] = d_eff
            
            if 'total_parameters' in result:
                row['Parameters'] = result['total_parameters']
            
            if 'test_acc' in result:
                row['Test Accuracy'] = result['test_acc']
            
            if 'train_loss' in result:
                row['Train Loss'] = result['train_loss']
            
            summary.append(row)
        
        df = pd.DataFrame(summary)
        return df
    
    def plot_correlation_matrix(self, save_path: Optional[str] = None):
        """
        Plot correlation matrix of metrics.
        
        Args:
            save_path: Path to save figure
        """
        df = self.generate_summary_table()
        
        if len(df.columns) <= 2:
            print("Not enough metrics for correlation analysis")
            return
        
        # Compute correlation
        numeric_df = df.select_dtypes(include=[np.number])
        corr = numeric_df.corr()
        
        # Plot
        fig, ax = plt.subplots(figsize=(10, 8))
        
        im = ax.imshow(corr, cmap='coolwarm', vmin=-1, vmax=1)
        
        # Set ticks
        ax.set_xticks(range(len(corr.columns)))
        ax.set_yticks(range(len(corr.columns)))
        ax.set_xticklabels(corr.columns, rotation=45, ha='right')
        ax.set_yticklabels(corr.columns)
        
        # Add colorbar
        plt.colorbar(im, ax=ax)
        
        # Add text annotations
        for i in range(len(corr.columns)):
            for j in range(len(corr.columns)):
                text = ax.text(j, i, f'{corr.iloc[i, j]:.2f}',
                             ha='center', va='center', color='black')
        
        ax.set_title('Metric Correlation Matrix', fontsize=14)
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        return fig
    
    def export_latex_table(self, save_path: str):
        """
        Export summary table to LaTeX format.
        
        Args:
            save_path: Path to save LaTeX file
        """
        df = self.generate_summary_table()
        
        latex = df.to_latex(index=False, float_format='%.2f')
        
        with open(save_path, 'w') as f:
            f.write(latex)
        
        print(f"LaTeX table saved to {save_path}")
    
    def generate_report(self, save_path: Optional[str] = None) -> str:
        """
        Generate comprehensive text report.
        
        Args:
            save_path: Path to save report
            
        Returns:
            Report string
        """
        if not self.results:
            self.load_all()
        
        report = []
        report.append("=" * 60)
        report.append("K Direction: Experiment Results Summary")
        report.append("=" * 60)
        report.append("")
        
        # Summary table
        df = self.generate_summary_table()
        report.append("Summary Table:")
        report.append("-" * 60)
        report.append(df.to_string(index=False))
        report.append("")
        
        # Individual experiment details
        for exp_name, result in self.results.items():
            report.append(f"\n{exp_name} Details:")
            report.append("-" * 60)
            
            for key, value in result.items():
                if isinstance(value, float):
                    report.append(f"  {key}: {value:.4f}")
                elif isinstance(value, (int, str)):
                    report.append(f"  {key}: {value}")
            
            report.append("")
        
        report_text = "\n".join(report)
        
        if save_path:
            with open(save_path, 'w') as f:
                f.write(report_text)
        
        return report_text


def aggregate_results(results_list: List[Dict]) -> Dict:
    """
    Aggregate results from multiple runs.
    
    Args:
        results_list: List of result dictionaries
        
    Returns:
        Aggregated statistics
    """
    aggregated = {}
    
    # Collect all keys
    all_keys = set()
    for result in results_list:
        all_keys.update(result.keys())
    
    for key in all_keys:
        values = [r[key] for r in results_list if key in r and isinstance(r[key], (int, float))]
        
        if values:
            aggregated[key] = {
                'mean': np.mean(values),
                'std': np.std(values),
                'min': np.min(values),
                'max': np.max(values),
                'n': len(values)
            }
    
    return aggregated
