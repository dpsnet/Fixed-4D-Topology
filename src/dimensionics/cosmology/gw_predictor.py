"""Gravitational Wave Predictor"""
import numpy as np

class GravitationalWavePredictor:
    """Predict GW modifications from dimension flow"""
    def dispersion(self, E, E_QG=1e19):
        """Modified dispersion relation"""
        return (E / E_QG)**2
