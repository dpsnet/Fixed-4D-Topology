#!/usr/bin/env python3
"""
Convexity Analysis

Implements the convexity condition: alpha + beta > T/8
"""

import numpy as np


class ConvexityAnalyzer:
    """
    Analyze convexity of free energy in dimension space.
    
    The convexity condition α + β > T/8 ensures thermodynamic
    stability and well-defined phase transitions.
    """
    
    def __init__(self, alpha: float, beta: float):
        self.alpha = alpha
        self.beta = beta
    
    def check(self, T: float = 1.0) -> bool:
        """Check if convexity condition is satisfied"""
        return self.alpha + self.beta > T / 8.0
    
    def critical_temperature(self) -> float:
        """Calculate critical temperature"""
        return 8.0 * (self.alpha + self.beta)
