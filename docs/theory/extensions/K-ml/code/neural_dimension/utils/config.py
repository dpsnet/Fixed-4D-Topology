"""
Configuration management for experiments.
"""

import yaml
import json
from pathlib import Path
from typing import Dict, Any, Optional
from dataclasses import dataclass, asdict


@dataclass
class Config:
    """Configuration class for experiments."""
    
    # Model configuration
    model_name: str = "TwoLayerMLP"
    hidden_dims: list = None
    activation: str = "relu"
    
    # Training configuration
    epochs: int = 100
    batch_size: int = 128
    learning_rate: float = 0.01
    momentum: float = 0.9
    weight_decay: float = 0.0
    optimizer: str = "SGD"
    
    # Data configuration
    dataset: str = "MNIST"
    data_dir: str = "./data"
    n_train: Optional[int] = None
    n_test: Optional[int] = None
    
    # Fisher information configuration
    fisher_sigma: float = 1.0
    fisher_approximation: str = "diagonal"  # or "full"
    
    # Experiment configuration
    seed: int = 42
    device: str = "auto"  # auto, cpu, cuda
    output_dir: str = "./results"
    
    # Logging configuration
    log_level: str = "INFO"
    log_file: Optional[str] = None
    
    def __post_init__(self):
        if self.hidden_dims is None:
            self.hidden_dims = [128]
        
        if self.device == "auto":
            import torch
            self.device = "cuda" if torch.cuda.is_available() else "cpu"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, config_dict: Dict[str, Any]) -> "Config":
        """Create from dictionary."""
        # Filter only valid fields
        valid_fields = {k: v for k, v in config_dict.items() 
                       if k in cls.__dataclass_fields__}
        return cls(**valid_fields)
    
    def save(self, path: str):
        """Save configuration to file."""
        path = Path(path)
        config_dict = self.to_dict()
        
        if path.suffix == '.yaml' or path.suffix == '.yml':
            with open(path, 'w') as f:
                yaml.dump(config_dict, f, default_flow_style=False)
        elif path.suffix == '.json':
            with open(path, 'w') as f:
                json.dump(config_dict, f, indent=2)
        else:
            raise ValueError(f"Unsupported file format: {path.suffix}")
    
    @classmethod
    def load(cls, path: str) -> "Config":
        """Load configuration from file."""
        path = Path(path)
        
        if not path.exists():
            raise FileNotFoundError(f"Config file not found: {path}")
        
        if path.suffix == '.yaml' or path.suffix == '.yml':
            with open(path, 'r') as f:
                config_dict = yaml.safe_load(f)
        elif path.suffix == '.json':
            with open(path, 'r') as f:
                config_dict = json.load(f)
        else:
            raise ValueError(f"Unsupported file format: {path.suffix}")
        
        return cls.from_dict(config_dict)
    
    def update(self, **kwargs):
        """Update configuration."""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
            else:
                raise ValueError(f"Unknown config key: {key}")


def load_config(path: str) -> Config:
    """Load configuration from file."""
    return Config.load(path)


def save_config(config: Config, path: str):
    """Save configuration to file."""
    config.save(path)
