"""
Setup script for Dimensionics package.

This package provides numerical implementations of the mathematical theories
developed in the Dimensionics research project.
"""

from setuptools import setup, find_packages

setup(
    name="dimensionics",
    version="3.0.0",
    author="Wang Bin & Kimi Agent",
    author_email="wang.bin@foxmail.com",
    description="Dimensionics: A Unified Mathematical Theory of Dimension",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/dpsnet/Fixed-4D-Topology",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Mathematics",
        "Topic :: Scientific/Engineering :: Physics",
    ],
    python_requires=">=3.8",
    install_requires=[
        "numpy>=1.21.0",
        "scipy>=1.7.0",
        "sympy>=1.9",
        "matplotlib>=3.4.0",
        "numba>=0.56.0",
        "pandas>=1.3.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.2.0",
            "pytest-cov>=3.0.0",
            "black>=21.0.0",
            "flake8>=4.0.0",
            "mypy>=0.910",
        ],
        "docs": [
            "sphinx>=4.3.0",
            "sphinx-rtd-theme>=1.0.0",
        ],
        "notebooks": [
            "jupyter>=1.0.0",
            "ipython>=7.30.0",
            "plotly>=5.3.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "dimensionics-verify=dimensionics.cli:verify_all_bridges",
            "dimensionics-demo=dimensionics.cli:demo",
        ],
    },
)
