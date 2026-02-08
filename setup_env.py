#!/usr/bin/env python3
"""
Virtual Environment Setup Script for Dimensionics Framework
===========================================================

This script automates the setup of a Python virtual environment
with all necessary dependencies for the Dimensionics Framework.

Usage:
    python setup_env.py [options]

Options:
    --dev           Install development dependencies
    --minimal       Install only core dependencies (no jupyter/viz)
    --path PATH     Custom venv path (default: ./venv)
    --force         Force recreation of existing environment
    -h, --help      Show this help message

Examples:
    python setup_env.py                    # Basic setup
    python setup_env.py --dev              # Development setup
    python setup_env.py --minimal          # Minimal dependencies
    python setup_env.py --path ./myenv     # Custom path
"""

import os
import sys
import subprocess
import argparse
import platform
from pathlib import Path


class Colors:
    """Terminal colors for output"""
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    END = '\033[0m'


def print_header(text):
    """Print formatted header"""
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{text.center(60)}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.END}\n")


def print_success(text):
    """Print success message"""
    print(f"{Colors.GREEN}✓ {text}{Colors.END}")


def print_warning(text):
    """Print warning message"""
    print(f"{Colors.YELLOW}⚠ {text}{Colors.END}")


def print_error(text):
    """Print error message"""
    print(f"{Colors.RED}✗ {text}{Colors.END}")


def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print_error(f"Python {version.major}.{version.minor} is not supported")
        print("  Please use Python 3.8 or higher")
        return False
    print_success(f"Python {version.major}.{version.minor}.{version.micro} detected")
    return True


def check_venv_module():
    """Check if venv module is available"""
    try:
        import venv
        print_success("venv module is available")
        return True
    except ImportError:
        print_error("venv module is not available")
        print("  Please install python3-venv package:")
        if platform.system() == "Linux":
            print("    Ubuntu/Debian: sudo apt-get install python3-venv")
            print("    RHEL/CentOS:   sudo yum install python3-virtualenv")
        return False


def get_venv_path(args):
    """Get virtual environment path"""
    if args.path:
        return Path(args.path).resolve()
    return Path(__file__).parent / "venv"


def venv_exists(venv_path):
    """Check if virtual environment already exists"""
    return venv_path.exists() and (venv_path / "pyvenv.cfg").exists()


def create_venv(venv_path, force=False):
    """Create virtual environment"""
    if venv_exists(venv_path):
        if force:
            print_warning(f"Removing existing environment: {venv_path}")
            import shutil
            shutil.rmtree(venv_path)
        else:
            print_warning(f"Environment already exists: {venv_path}")
            print("  Use --force to recreate")
            return True
    
    print(f"Creating virtual environment at: {venv_path}")
    try:
        import venv
        builder = venv.EnvBuilder(with_pip=True, clear=True)
        builder.create(venv_path)
        print_success("Virtual environment created")
        return True
    except Exception as e:
        print_error(f"Failed to create virtual environment: {e}")
        return False


def get_python_executable(venv_path):
    """Get Python executable path in venv"""
    if platform.system() == "Windows":
        return venv_path / "Scripts" / "python.exe"
    return venv_path / "bin" / "python"


def get_pip_executable(venv_path):
    """Get pip executable path in venv"""
    if platform.system() == "Windows":
        return venv_path / "Scripts" / "pip.exe"
    return venv_path / "bin" / "pip"


def install_dependencies(venv_path, args):
    """Install dependencies"""
    pip = get_pip_executable(venv_path)
    
    # Upgrade pip first
    print("\nUpgrading pip...")
    result = subprocess.run(
        [str(pip), "install", "--upgrade", "pip"],
        capture_output=True,
        text=True
    )
    if result.returncode != 0:
        print_warning("Failed to upgrade pip, continuing anyway")
    else:
        print_success("pip upgraded")
    
    # Determine requirements file
    if args.minimal:
        # Create temporary minimal requirements
        print("\nInstalling minimal dependencies...")
        packages = ["numpy", "scipy"]
        result = subprocess.run(
            [str(pip), "install"] + packages,
            capture_output=True,
            text=True
        )
    else:
        requirements_file = (
            "requirements-dev.txt" if args.dev 
            else "requirements.txt"
        )
        print(f"\nInstalling dependencies from {requirements_file}...")
        result = subprocess.run(
            [str(pip), "install", "-r", requirements_file],
            capture_output=True,
            text=True
        )
    
    if result.returncode != 0:
        print_error("Failed to install dependencies")
        print(result.stderr)
        return False
    
    print_success("Dependencies installed successfully")
    return True


def install_kernel(venv_path):
    """Install Jupyter kernel for this environment"""
    python = get_python_executable(venv_path)
    print("\nInstalling Jupyter kernel...")
    result = subprocess.run(
        [str(python), "-m", "ipykernel", "install", 
         "--user", "--name=dimensionics", "--display-name", "Python (Dimensionics)"],
        capture_output=True,
        text=True
    )
    if result.returncode == 0:
        print_success("Jupyter kernel 'dimensionics' installed")
    else:
        print_warning("Could not install Jupyter kernel (optional)")
    return True


def test_installation(venv_path):
    """Test the installation"""
    python = get_python_executable(venv_path)
    print("\nTesting installation...")
    
    test_code = '''
import sys
sys.path.insert(0, "src")
try:
    from unified_framework import Dimension, VariationalPrinciple
    vp = VariationalPrinciple()
    d_opt = vp.optimal_dimension()
    print(f"✓ Framework test passed (d_opt = {d_opt:.4f})")
except Exception as e:
    print(f"✗ Framework test failed: {e}")
    sys.exit(1)
'''
    
    result = subprocess.run(
        [str(python), "-c", test_code],
        capture_output=True,
        text=True,
        cwd=Path(__file__).parent
    )
    
    if result.returncode == 0:
        print(result.stdout.strip())
        return True
    else:
        print_error("Installation test failed")
        print(result.stderr)
        return False


def print_activation_instructions(venv_path):
    """Print activation instructions"""
    print_header("Setup Complete!")
    
    print(f"{Colors.BOLD}Virtual Environment:{Colors.END} {venv_path}")
    print()
    
    print(f"{Colors.BOLD}To activate the environment:{Colors.END}")
    if platform.system() == "Windows":
        print(f"  {venv_path}\\Scripts\\activate")
    else:
        print(f"  source {venv_path}/bin/activate")
    print()
    
    print(f"{Colors.BOLD}To deactivate:{Colors.END}")
    print("  deactivate")
    print()
    
    print(f"{Colors.BOLD}To use in Jupyter:{Colors.END}")
    print("  1. Activate the environment")
    print("  2. jupyter notebook")
    print("  3. Select kernel: 'Python (Dimensionics)'")
    print()


def main():
    parser = argparse.ArgumentParser(
        description="Setup virtual environment for Dimensionics Framework",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python setup_env.py              # Basic setup
  python setup_env.py --dev        # Development setup
  python setup_env.py --minimal    # Minimal dependencies
  python setup_env.py --force      # Recreate environment
        """
    )
    parser.add_argument(
        "--dev", 
        action="store_true",
        help="Install development dependencies"
    )
    parser.add_argument(
        "--minimal",
        action="store_true", 
        help="Install only core dependencies (no jupyter/viz)"
    )
    parser.add_argument(
        "--path",
        type=str,
        help="Custom venv path (default: ./venv)"
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Force recreation of existing environment"
    )
    
    args = parser.parse_args()
    
    print_header("Dimensionics Framework - Virtual Environment Setup")
    
    # Pre-flight checks
    if not check_python_version():
        return 1
    
    if not check_venv_module():
        return 1
    
    # Get venv path
    venv_path = get_venv_path(args)
    print(f"\nVirtual environment path: {venv_path}")
    
    # Create venv
    if not create_venv(venv_path, args.force):
        return 1
    
    # Install dependencies
    if not install_dependencies(venv_path, args):
        return 1
    
    # Install kernel (if not minimal)
    if not args.minimal:
        install_kernel(venv_path)
    
    # Test installation
    if not test_installation(venv_path):
        print_warning("Installation completed but tests failed")
    
    # Print instructions
    print_activation_instructions(venv_path)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
