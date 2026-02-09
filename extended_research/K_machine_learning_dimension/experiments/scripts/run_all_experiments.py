"""
Run All Experiments
===================

Master script to run E1-E6 experiments sequentially.
"""

import os
import sys
import subprocess
import argparse
import time
from pathlib import Path

# Experiment configurations
EXPERIMENTS = [
    {
        'name': 'E1: Effective Dimension Baseline',
        'script': 'E1_effective_dim_baseline.py',
        'estimated_time': '5-10 min',
    },
    {
        'name': 'E2: Training Dynamics',
        'script': 'E2_training_dynamics.py',
        'estimated_time': '10-20 min',
    },
    {
        'name': 'E3: Double Descent',
        'script': 'E3_double_descent.py',
        'estimated_time': '30-60 min',
    },
    {
        'name': 'E4: Neural Collapse',
        'script': 'E4_neural_collapse.py',
        'estimated_time': '20-40 min',
    },
    {
        'name': 'E5: Lottery Ticket',
        'script': 'E5_lottery_ticket.py',
        'estimated_time': '30-60 min',
    },
    {
        'name': 'E6: Generalization Bound',
        'script': 'E6_generalization_bound.py',
        'estimated_time': '20-40 min',
    },
]


def run_experiment(script_path: str, verbose: bool = True) -> bool:
    """
    Run a single experiment script.
    
    Args:
        script_path: Path to experiment script
        verbose: Print output
        
    Returns:
        True if successful
    """
    if not os.path.exists(script_path):
        print(f"Error: Script not found: {script_path}")
        return False
    
    start_time = time.time()
    
    try:
        result = subprocess.run(
            [sys.executable, script_path],
            capture_output=not verbose,
            text=True,
            check=True
        )
        
        elapsed = time.time() - start_time
        
        if verbose:
            print(f"✓ Completed in {elapsed:.1f}s")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"✗ Failed with error code {e.returncode}")
        if e.stderr:
            print(e.stderr)
        return False


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Run all K-direction experiments'
    )
    parser.add_argument(
        '--experiments', '-e',
        nargs='+',
        choices=['E1', 'E2', 'E3', 'E4', 'E5', 'E6', 'all'],
        default=['all'],
        help='Which experiments to run'
    )
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Verbose output'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Print what would be run without executing'
    )
    
    args = parser.parse_args()
    
    # Determine which experiments to run
    if 'all' in args.experiments:
        to_run = EXPERIMENTS
    else:
        exp_names = [f'{e}:'.upper() for e in args.experiments]
        to_run = [e for e in EXPERIMENTS if any(e['name'].startswith(n) for n in exp_names)]
    
    # Print summary
    print("=" * 60)
    print("K Direction: Running Experiments")
    print("=" * 60)
    print(f"\nWill run {len(to_run)} experiments:\n")
    
    for i, exp in enumerate(to_run, 1):
        print(f"{i}. {exp['name']}")
        print(f"   Script: {exp['script']}")
        print(f"   Estimated time: {exp['estimated_time']}")
        print()
    
    if args.dry_run:
        print("(Dry run - not executing)")
        return
    
    # Run experiments
    script_dir = Path(__file__).parent
    results = []
    
    total_start = time.time()
    
    for i, exp in enumerate(to_run, 1):
        print(f"\n[{i}/{len(to_run)}] Running {exp['name']}...")
        print("-" * 60)
        
        script_path = script_dir / exp['script']
        success = run_experiment(str(script_path), verbose=args.verbose)
        
        results.append({
            'name': exp['name'],
            'success': success
        })
        
        if not success:
            print(f"Warning: {exp['name']} failed, continuing...")
    
    total_elapsed = time.time() - total_start
    
    # Summary
    print("\n" + "=" * 60)
    print("Summary")
    print("=" * 60)
    
    successful = sum(1 for r in results if r['success'])
    failed = len(results) - successful
    
    print(f"\nTotal time: {total_elapsed/60:.1f} minutes")
    print(f"Successful: {successful}/{len(results)}")
    print(f"Failed: {failed}/{len(results)}")
    
    if failed > 0:
        print("\nFailed experiments:")
        for r in results:
            if not r['success']:
                print(f"  - {r['name']}")
    
    print("\nResults saved in: experiments/results/")
    print("=" * 60)
    
    return 0 if failed == 0 else 1


if __name__ == '__main__':
    sys.exit(main())
