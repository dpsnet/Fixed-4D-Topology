"""Convexity in QFT"""

class ConvexityQFT:
    """Convexity analysis in quantum field theory"""
    def __init__(self, alpha, beta, T):
        self.alpha = alpha
        self.beta = beta
        self.T = T
    
    def check_stability(self):
        """Check thermodynamic stability"""
        return self.alpha + self.beta > self.T / 8
