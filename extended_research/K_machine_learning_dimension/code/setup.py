"""
Setup configuration for neural_dimension package.
"""

from setuptools import setup, find_packages
import os

# Read README
readme_path = os.path.join(os.path.dirname(__file__), '..', 'README.md')
if os.path.exists(readme_path):
    with open(readme_path, 'r', encoding='utf-8') as f:
        long_description = f.read()
else:
    long_description = 'Neural Dimension Toolkit - Analyze effective dimension of neural networks'

setup(
    name='neural_dimension',
    version='0.1.0',
    author='K Direction Research Team',
    author_email='',
    description='Toolkit for analyzing effective dimension of neural networks',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/dpsnet/Fixed-4D-Topology',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Scientific/Engineering :: Mathematics',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
    python_requires='>=3.8',
    install_requires=[
        'torch>=1.10.0',
        'torchvision>=0.11.0',
        'numpy>=1.20.0',
        'matplotlib>=3.3.0',
        'seaborn>=0.11.0',
        'scipy>=1.7.0',
        'tqdm>=4.60.0',
    ],
    extras_require={
        'dev': [
            'pytest>=6.2.0',
            'pytest-cov>=2.12.0',
            'black>=21.0',
            'flake8>=3.9.0',
            'mypy>=0.910',
            'jupyter>=1.0.0',
        ],
        'docs': [
            'sphinx>=4.0.0',
            'sphinx-rtd-theme>=0.5.0',
        ],
    },
    entry_points={
        'console_scripts': [
            'neural-dim=neural_dimension.cli:main',
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
