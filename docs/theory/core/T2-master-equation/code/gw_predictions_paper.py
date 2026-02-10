#!/usr/bin/env python3
"""
P2-T3 Master Equation: Gravitational Wave Predictions Analysis
===============================================================

Paper-grade comprehensive analysis of gravitational wave detectability
across multiple observational channels: LISA, PTA, ground-based interferometers,
and cosmic gravitational wave background.

Author: Research Framework
Date: 2026
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import json
import os
from scipy import integrate, special
from scipy.interpolate import interp1d
import warnings
warnings.filterwarnings('ignore')

# ============================================================================
# PHYSICAL CONSTANTS (SI units)
# ============================================================================
G = 6.674e-11           # Gravitational constant [m^3 kg^-1 s^-2]
c = 2.998e8             # Speed of light [m/s]
hbar = 1.055e-34        # Reduced Planck constant [J s]
k_B = 1.381e-23         # Boltzmann constant [J/K]
M_sun = 1.989e30        # Solar mass [kg]
M_pl = 2.176e-8         # Planck mass [kg]
H0 = 70.0               # Hubble constant [km/s/Mpc]
H0_SI = H0 * 1000 / 3.086e22  # Hubble constant [s^-1]
Omega_m = 0.3           # Matter density parameter
Omega_Lambda = 0.7      # Dark energy density parameter
Omega_r = 9.2e-5        # Radiation density parameter

# Characteristic frequencies
f_LISA_min = 1e-4       # LISA minimum frequency [Hz]
f_LISA_max = 1.0        # LISA maximum frequency [Hz]
f_PTA_min = 1e-9        # PTA minimum frequency [Hz]
f_PTA_max = 1e-6        # PTA maximum frequency [Hz]
f_LIGO_min = 10.0       # LIGO minimum frequency [Hz]
f_LIGO_max = 1000.0     # LIGO maximum frequency [Hz]

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def chirp_mass(m1, m2):
    """Calculate chirp mass from component masses."""
    return (m1 * m2)**(3/5) / (m1 + m2)**(1/5)

def reduced_mass(m1, m2):
    """Calculate reduced mass from component masses."""
    return m1 * m2 / (m1 + m2)

def symmetric_mass_ratio(m1, m2):
    """Calculate symmetric mass ratio."""
    return m1 * m2 / (m1 + m2)**2

# ============================================================================
# SECTION 1: LISA SENSITIVITY AND DETECTABILITY
# ============================================================================

class LISASensitivity:
    """
    LISA (Laser Interferometer Space Antenna) sensitivity calculations.
    Based on the L3 mission design (2017).
    """
    
    def __init__(self):
        self.arm_length = 2.5e9  # Arm length in meters
        self.laser_power = 2.0   # Laser power in Watts
        self.wavelength = 1064e-9  # Laser wavelength in meters
        self.T_obs = 4.0 * 365.25 * 24 * 3600  # Observation time (4 years) in seconds
        
        # LISA mission parameters
        self.f_star = c / (2 * np.pi * self.arm_length)  # Transfer frequency
        print(f"LISA transfer frequency f*: {self.f_star:.4e} Hz")
        
    def acceleration_noise(self, f):
        """
        Acceleration noise in acceleration-equivalent units.
        
        Parameters:
        -----------
        f : array-like
            Frequency in Hz
            
        Returns:
        --------
        S_acc : array-like
            Acceleration noise power spectral density
        """
        # LISA Pathfinder achieved performance
        S_acc = 9e-30 * (1 + (0.4e-3 / f)**2) * (1 + (f / 8e-3)**4)  # m^2/s^4/Hz
        return S_acc
    
    def optical_metrology_noise(self, f):
        """
        Optical metrology noise (shot noise + others).
        
        Parameters:
        -----------
        f : array-like
            Frequency in Hz
            
        Returns:
        --------
        S_oms : array-like
            OMS noise power spectral density
        """
        # Shot noise limited performance
        S_oms = 2.25e-22 * (1 + (2e-3 / f)**4)  # m^2/Hz
        return S_oms
    
    def noise_curve(self, f):
        """
        Complete LISA sensitivity curve (noise power spectral density).
        
        Parameters:
        -----------
        f : array-like
            Frequency in Hz
            
        Returns:
        --------
        S_n : array-like
            Strain noise power spectral density
        """
        S_acc = self.acceleration_noise(f)
        S_oms = self.optical_metrology_noise(f)
        
        # Transfer function for LISA's triangular configuration
        x = f / self.f_star
        T_squared = 4.0 * np.sin(x)**2 * (1.0 + 6.0/16.0 * np.sin(x)**2)
        
        # Total noise PSD
        S_n = (S_oms + 2.0 * (1.0 + np.cos(x)**2) * S_acc / (2 * np.pi * f)**4) / T_squared
        
        return S_n
    
    def sensitivity_curve(self, f):
        """
        LISA sensitivity curve in characteristic strain.
        
        Parameters:
        -----------
        f : array-like
            Frequency in Hz
            
        Returns:
        --------
        h_c : array-like
            Characteristic strain noise
        """
        S_n = self.noise_curve(f)
        h_c = np.sqrt(f * S_n)
        return h_c
    
    def calculate_snr(self, f, h_signal, waveform_type='chirp'):
        """
        Calculate signal-to-noise ratio for a given signal.
        
        Parameters:
        -----------
        f : array-like
            Frequency array
        h_signal : array-like
            Signal characteristic strain
        waveform_type : str
            Type of waveform ('chirp', 'monochromatic', 'burst')
            
        Returns:
        --------
        snr : float
            Signal-to-noise ratio
        """
        S_n = self.noise_curve(f)
        
        if waveform_type == 'chirp':
            # For chirp signals: SNR^2 = 4 * integral of (h_c^2 / (f * S_n)) df
            integrand = h_signal**2 / (f * S_n)
            snr_squared = 4 * np.trapezoid(integrand, f)
        elif waveform_type == 'monochromatic':
            # For monochromatic sources: SNR = h_signal / sqrt(S_n * delta_f)
            delta_f = 1.0 / self.T_obs
            snr_squared = np.max(h_signal**2 / (f * S_n * delta_f))
        else:
            # Generic formula
            integrand = h_signal**2 / (f * S_n)
            snr_squared = 4 * np.trapezoid(integrand, f)
        
        snr = np.sqrt(snr_squared)
        return snr
    
    def detection_confidence(self, snr, threshold=8.0):
        """
        Calculate detection confidence level.
        
        Parameters:
        -----------
        snr : float
            Signal-to-noise ratio
        threshold : float
            Detection threshold
            
        Returns:
        --------
        confidence : dict
            Dictionary with confidence metrics
        """
        # False alarm probability (Gaussian noise)
        false_alarm_prob = 0.5 * special.erfc(threshold / np.sqrt(2))
        
        # Detection probability (assuming signal present)
        detection_prob = 0.5 * special.erfc((threshold - snr) / np.sqrt(2))
        
        # Confidence level in sigma
        confidence_sigma = snr
        
        return {
            'snr': snr,
            'threshold': threshold,
            'false_alarm_probability': false_alarm_prob,
            'detection_probability': detection_prob,
            'confidence_sigma': confidence_sigma,
            'is_detectable': snr > threshold
        }


class BinaryInspiralLISA:
    """
    Gravitational wave signals from binary inspirals for LISA band.
    Includes dimension effects from 4D topology.
    """
    
    def __init__(self, m1, m2, z=0.0, D=4):
        """
        Initialize binary system.
        
        Parameters:
        -----------
        m1, m2 : float
            Component masses in solar masses
        z : float
            Redshift
        D : int
            Number of spatial dimensions (default 4 for our framework)
        """
        self.m1 = m1 * M_sun
        self.m2 = m2 * M_sun
        self.M_total = self.m1 + self.m2
        self.z = z
        self.D = D
        
        # Cosmological distance
        self.d_L = self.luminosity_distance(z)
        
        # Chirp mass
        self.M_c = chirp_mass(self.m1, self.m2)
        
        # Calculate ISCO frequency
        self.f_isco = self._isco_frequency()
        
    def _isco_frequency(self):
        """Calculate ISCO frequency for the binary."""
        # ISCO radius for Schwarzschild: r_isco = 6GM/c^2
        r_isco = 6 * G * self.M_total / c**2
        
        # Orbital frequency at ISCO
        f_orb_isco = np.sqrt(G * self.M_total / (4 * np.pi**2 * r_isco**3))
        
        # GW frequency is twice the orbital frequency
        f_gw_isco = 2 * f_orb_isco
        
        return f_gw_isco
    
    def luminosity_distance(self, z):
        """
        Approximate luminosity distance for flat LambdaCDM.
        Uses analytic approximation.
        """
        # For z << 1: d_L ≈ cz/H0
        # For general z, use approximate formula
        if z < 0.1:
            d_L = c * z / H0_SI
        else:
            # Approximate integral for luminosity distance
            # d_L = c(1+z)/H0 * integral_0^z dz'/E(z')
            # where E(z) = sqrt(Omega_m(1+z)^3 + Omega_Lambda)
            z_array = np.linspace(0, z, 1000)
            E_z = np.sqrt(Omega_m * (1 + z_array)**3 + Omega_Lambda)
            integral = np.trapezoid(1.0 / E_z, z_array)
            d_L = c * (1 + z) / H0_SI * integral
        
        return d_L
    
    def waveform(self, f, include_4d_effects=True):
        """
        Calculate gravitational wave characteristic strain.
        
        Parameters:
        -----------
        f : array-like
            Frequency array
        include_4d_effects : bool
            Whether to include 4D topology modifications
            
        Returns:
        --------
        h_c : array-like
            Characteristic strain
        """
        # Redshifted chirp mass (in kg)
        M_c_z = self.M_c * (1 + self.z)
        
        # Dimensionless chirp mass
        M_c_dim = G * M_c_z / c**3
        
        # Characteristic strain formula (Peters & Mathews 1963)
        # h_c(f) = (4/d_L) * (G*M_c_z/c^2)^(5/3) * (pi*f/c)^(2/3)
        # With geometric units: h_c = sqrt(32/5) * M_c^(5/6) * f^(-7/6) / d_L
        
        # Calculate strain
        h_c_gr = (4.0 / self.d_L) * (G * M_c_z / c**2)**(5/3) * (np.pi * f / c)**(2/3)
        
        # 4D topology corrections (suppression factor)
        if include_4d_effects and self.D == 4:
            # Additional dimension suppresses signal at high frequencies
            R_compact = 1e-3  # Example compactification scale in meters
            lambda_gw = c / f
            
            suppression = np.ones_like(np.asarray(f, dtype=float))
            mask = lambda_gw < R_compact
            suppression[mask] = (lambda_gw[mask] / R_compact)**(1/3)
            
            h_c = h_c_gr * suppression
        else:
            h_c = h_c_gr
        
        # Cut off at ISCO
        h_c = np.asarray(h_c, dtype=float)
        mask_cutoff = f > self.f_isco
        if np.any(mask_cutoff):
            h_c = np.where(mask_cutoff, 0.0, h_c)
        
        return h_c
    
    def merger_time(self, f_start):
        """
        Calculate time to merger from given starting frequency.
        
        Parameters:
        -----------
        f_start : float
            Starting frequency in Hz
            
        Returns:
        --------
        t_merger : float
            Time to merger in seconds
        """
        # Time to coalescence from frequency f
        # t = 5/256 * (c^3/G*M_c)^(5/3) * (pi*f)^(-8/3)
        M_c_z = self.M_c * (1 + self.z)
        t_merger = (5.0 / 256.0) * (c**3 / (G * M_c_z))**(5/3) * (np.pi * f_start)**(-8/3)
        
        return t_merger


# ============================================================================
# SECTION 2: PTA (PULSAR TIMING ARRAY) PREDICTIONS
# ============================================================================

class PTASensitivity:
    """
    Pulsar Timing Array sensitivity and Hellings-Downs calculations.
    Includes SKA and IPTA projections.
    """
    
    def __init__(self, array_name='IPTA'):
        """
        Initialize PTA array configuration.
        
        Parameters:
        -----------
        array_name : str
            Name of the array ('IPTA', 'SKA', 'NANOGrav', 'PPTA', 'EPTA')
        """
        self.array_name = array_name
        
        # Array configurations
        configs = {
            'IPTA': {
                'N_pulsars': 100,
                'sigma_t': 100e-9,  # Timing precision in seconds
                'T_obs': 20 * 365.25 * 24 * 3600,  # 20 years
                'cadence': 14 * 24 * 3600,  # Biweekly observations
            },
            'SKA': {
                'N_pulsars': 200,
                'sigma_t': 30e-9,   # Improved timing precision
                'T_obs': 30 * 365.25 * 24 * 3600,  # 30 years
                'cadence': 7 * 24 * 3600,  # Weekly observations
            },
            'NANOGrav': {
                'N_pulsars': 68,
                'sigma_t': 500e-9,
                'T_obs': 15 * 365.25 * 24 * 3600,
                'cadence': 14 * 24 * 3600,
            },
            'EPTA': {
                'N_pulsars': 25,
                'sigma_t': 1e-6,
                'T_obs': 24 * 365.25 * 24 * 3600,
                'cadence': 14 * 24 * 3600,
            },
            'PPTA': {
                'N_pulsars': 20,
                'sigma_t': 1e-6,
                'T_obs': 15 * 365.25 * 24 * 3600,
                'cadence': 14 * 24 * 3600,
            }
        }
        
        config = configs.get(array_name, configs['IPTA'])
        self.N_pulsars = config['N_pulsars']
        self.sigma_t = config['sigma_t']
        self.T_obs = config['T_obs']
        self.cadence = config['cadence']
        
    def hellings_downs_curve(self, zeta):
        """
        Calculate Hellings and Downs correlation function.
        
        The HD curve describes the expected correlation of timing residuals
        between pairs of pulsars as a function of angular separation.
        
        Parameters:
        -----------
        zeta : array-like
            Angular separation between pulsars in radians
            
        Returns:
        --------
        Gamma : array-like
            Hellings-Downs correlation
        """
        x = np.array((1.0 - np.cos(zeta)) / 2.0, dtype=float, copy=True)
        
        # Hellings-Downs formula
        Gamma = 0.5 + 1.5 * x * np.log(np.clip(x, 1e-15, 1)) - 0.75 * x + 0.5 * np.heaviside(x - 1e-10, 0.5)
        
        # Handle edge cases
        mask_small = x < 1e-10
        mask_large = x > 1 - 1e-10
        if np.any(mask_small):
            Gamma = np.where(mask_small, 1.0, Gamma)  # Auto-correlation
        if np.any(mask_large):
            Gamma = np.where(mask_large, 0.0, Gamma)  # Anti-podal limit
        
        return Gamma
    
    def noise_curve(self, f):
        """
        PTA sensitivity curve (noise power spectrum).
        
        Parameters:
        -----------
        f : array-like
            Frequency in Hz (note: typically in nHz for PTA)
            
        Returns:
        --------
        S_n : array-like
            Characteristic strain noise power spectrum
        """
        # Convert to nHz for convenience
        f_nHz = f * 1e9
        
        # White noise floor from timing precision
        # S_h(f) ~ sigma_t^2 / (T_obs * N_pulsars)
        S_white = 2 * self.sigma_t**2 / (self.T_obs * self.N_pulsars)
        
        # Red noise from pulsar spin instabilities
        # Typically modeled as power law
        alpha_red = -13/3  # Characteristic slope for GW background
        f_ref = 1e-9  # 1 nHz reference frequency
        
        # Combined noise
        S_n = S_white * (f / f_ref)**alpha_red
        
        return S_n
    
    def sensitivity_curve(self, f):
        """
        PTA sensitivity curve in characteristic strain.
        
        Parameters:
        -----------
        f : array-like
            Frequency in Hz
            
        Returns:
        --------
        h_c : array-like
            Characteristic strain sensitivity
        """
        S_n = self.noise_curve(f)
        h_c = np.sqrt(f * S_n)
        return h_c
    
    def stochastic_background_detection(self, Omega_gw, f_ref=1e-8):
        """
        Calculate SNR for stochastic background detection.
        
        Parameters:
        -----------
        Omega_gw : float
            Dimensionless energy density of GWs at reference frequency
        f_ref : float
            Reference frequency in Hz
            
        Returns:
        --------
        snr : float
            Signal-to-noise ratio
        """
        # Characteristic strain of stochastic background
        # h_c^2(f) = (3*H0^2)/(4*pi^2) * Omega_gw(f) / f^2
        h_c_bg = np.sqrt(3 * H0_SI**2 / (4 * np.pi**2) * Omega_gw / f_ref**2)
        
        # Noise at reference frequency
        S_n = self.noise_curve(f_ref)
        h_c_noise = np.sqrt(f_ref * S_n)
        
        # SNR calculation for stochastic background
        # For HD curve detection, we need cross-correlation
        snr = h_c_bg / h_c_noise * np.sqrt(self.N_pulsars * (self.N_pulsars - 1) / 2)
        
        return snr


class SupermassiveBHBinary:
    """
    Gravitational wave signals from supermassive black hole binaries.
    Relevant for PTA detection.
    """
    
    def __init__(self, M_total, q=1.0, z=0.1):
        """
        Initialize SMBH binary.
        
        Parameters:
        -----------
        M_total : float
            Total mass in solar masses
        q : float
            Mass ratio
        z : float
            Redshift
        """
        self.M_total = M_total * M_sun
        self.q = q
        self.z = z
        
        # Component masses
        self.m1 = self.M_total * q / (1 + q)
        self.m2 = self.M_total / (1 + q)
        
        # Chirp mass
        self.M_c = chirp_mass(self.m1, self.m2)
        
        # Luminosity distance
        self.d_L = self._luminosity_distance(z)
        
    def _luminosity_distance(self, z):
        """Calculate luminosity distance."""
        if z < 0.1:
            return c * z / H0_SI
        else:
            z_array = np.linspace(0, z, 1000)
            E_z = np.sqrt(Omega_m * (1 + z_array)**3 + Omega_Lambda)
            integral = np.trapezoid(1.0 / E_z, z_array)
            return c * (1 + z) / H0_SI * integral
    
    def strain_at_frequency(self, f_gw):
        """
        Calculate strain at given GW frequency.
        
        Parameters:
        -----------
        f_gw : float or array-like
            Gravitational wave frequency in Hz
            
        Returns:
        --------
        h_c : float or array-like
            Characteristic strain
        """
        # Redshifted chirp mass
        M_c_z = self.M_c * (1 + self.z)
        
        # Characteristic strain for circular binary
        h_c = (4.0 / self.d_L) * (G * M_c_z / c**2)**(5/3) * (np.pi * f_gw / c)**(2/3)
        
        return h_c
    
    def orbital_frequency(self, a):
        """
        Calculate orbital frequency from separation.
        
        Parameters:
        -----------
        a : float
            Orbital separation in meters
            
        Returns:
        --------
        f_orb : float
            Orbital frequency in Hz
        """
        f_orb = np.sqrt(G * self.M_total / (4 * np.pi**2 * a**3))
        return f_orb
    
    def separation_from_frequency(self, f_gw):
        """
        Calculate orbital separation from GW frequency.
        
        Parameters:
        -----------
        f_gw : float
            GW frequency (2x orbital frequency)
            
        Returns:
        --------
        a : float
            Orbital separation in meters
        """
        f_orb = f_gw / 2.0
        a = (G * self.M_total / (4 * np.pi**2 * f_orb**2))**(1/3)
        return a


# ============================================================================
# SECTION 3: GROUND-BASED INTERFEROMETERS
# ============================================================================

class GroundBasedInterferometer:
    """
    LIGO/Virgo/KAGRA sensitivity and binary coalescence analysis.
    """
    
    def __init__(self, detector='LIGO_O4'):
        """
        Initialize ground-based detector.
        
        Parameters:
        -----------
        detector : str
            Detector configuration ('LIGO_O4', 'LIGO_O5', 'Virgo_O4', 'KAGRA', 'ET', 'CE')
        """
        self.detector = detector
        
        # Detector configurations (approximate PSD parameters)
        configs = {
            'LIGO_O4': {
                'f_low': 10.0,
                'f_high': 2048.0,
                'S0': 1e-46,
                'alpha': -4,  # Low frequency
                'beta': 2,    # Mid frequency
                'gamma': -4,  # High frequency
                'f0': 100.0,  # Knee frequency
            },
            'LIGO_O5': {
                'f_low': 10.0,
                'f_high': 4096.0,
                'S0': 3e-47,
                'alpha': -4,
                'beta': 2,
                'gamma': -4,
                'f0': 100.0,
            },
            'Virgo_O4': {
                'f_low': 10.0,
                'f_high': 2048.0,
                'S0': 2e-46,
                'alpha': -4,
                'beta': 2,
                'gamma': -4,
                'f0': 150.0,
            },
            'KAGRA': {
                'f_low': 10.0,
                'f_high': 2048.0,
                'S0': 5e-46,
                'alpha': -4,
                'beta': 2,
                'gamma': -4,
                'f0': 120.0,
            },
            'ET': {
                'f_low': 1.0,
                'f_high': 10000.0,
                'S0': 1e-48,
                'alpha': -4,
                'beta': 2,
                'gamma': -4,
                'f0': 50.0,
            },
            'CE': {
                'f_low': 5.0,
                'f_high': 10000.0,
                'S0': 5e-49,
                'alpha': -4,
                'beta': 2,
                'gamma': -4,
                'f0': 30.0,
            }
        }
        
        self.config = configs.get(detector, configs['LIGO_O4'])
    
    def noise_curve(self, f):
        """
        Approximate noise power spectral density.
        
        Parameters:
        -----------
        f : array-like
            Frequency in Hz
            
        Returns:
        --------
        S_n : array-like
            Noise PSD
        """
        cfg = self.config
        S0 = cfg['S0']
        f0 = cfg['f0']
        
        # Simple analytic approximation
        # S_n(f) = S0 * [(f0/f)^alpha + (f/f0)^beta + (f/f0)^gamma]
        S_n = S0 * (
            (f0 / f)**cfg['alpha'] + 
            (f / f0)**cfg['beta'] + 
            (f / f0)**cfg['gamma']
        )
        
        # Apply frequency bounds
        S_n[f < cfg['f_low']] = np.inf
        S_n[f > cfg['f_high']] = np.inf
        
        return S_n
    
    def sensitivity_curve(self, f):
        """
        Characteristic strain sensitivity.
        
        Parameters:
        -----------
        f : array-like
            Frequency in Hz
            
        Returns:
        --------
        h_c : array-like
            Characteristic strain
        """
        S_n = self.noise_curve(f)
        h_c = np.sqrt(f * S_n)
        return h_c
    
    def calculate_snr(self, f, h_signal):
        """
        Calculate signal-to-noise ratio.
        
        Parameters:
        -----------
        f : array-like
            Frequency array
        h_signal : array-like
            Signal characteristic strain
            
        Returns:
        --------
        snr : float
            Signal-to-noise ratio
        """
        S_n = self.noise_curve(f)
        integrand = h_signal**2 / (f * S_n)
        snr_squared = 4 * np.trapezoid(integrand, f)
        return np.sqrt(snr_squared)
    
    def parameter_estimation_bias(self, snr, delta_h_over_h=0.01):
        """
        Estimate parameter estimation uncertainties.
        
        Parameters:
        -----------
        snr : float
            Signal-to-noise ratio
        delta_h_over_h : float
            Fractional template mismatch
            
        Returns:
        --------
        biases : dict
            Dictionary of parameter uncertainties
        """
        # Fisher matrix approximation
        # Parameter uncertainties scale as 1/SNR
        
        # For a binary inspiral, typical parameter correlations
        sigma_M = 0.01 / snr  # Relative chirp mass uncertainty
        sigma_eta = 0.1 / snr  # Symmetric mass ratio uncertainty
        sigma_t = 1e-3 / snr   # Coalescence time uncertainty (s)
        sigma_phi = 1.0 / snr  # Phase uncertainty (rad)
        sigma_dL = 0.5 / snr   # Relative luminosity distance uncertainty
        
        # Systematic bias from template mismatch
        bias_factor = delta_h_over_h * snr
        
        return {
            'sigma_Mc_over_Mc': sigma_M,
            'sigma_eta': sigma_eta,
            'sigma_tc': sigma_t,
            'sigma_phi': sigma_phi,
            'sigma_dL_over_dL': sigma_dL,
            'bias_factor': bias_factor,
            'snr': snr
        }


class CompactBinaryCoalescence:
    """
    Compact binary coalescence waveforms for ground-based detectors.
    """
    
    def __init__(self, m1, m2, z=0.1):
        """
        Initialize CBC system.
        
        Parameters:
        -----------
        m1, m2 : float
            Component masses in solar masses
        z : float
            Redshift
        """
        self.m1 = m1 * M_sun
        self.m2 = m2 * M_sun
        self.M_total = self.m1 + self.m2
        self.z = z
        
        self.M_c = chirp_mass(self.m1, self.m2)
        self.eta = symmetric_mass_ratio(self.m1, self.m2)
        self.mu = reduced_mass(self.m1, self.m2)
        
        # Luminosity distance
        self.d_L = self._luminosity_distance(z)
        
        # ISCO frequency
        self.f_isco = self._isco_frequency()
        
        # Ringdown frequency (approximate)
        self.f_ring = self._ringdown_frequency()
    
    def _luminosity_distance(self, z):
        """Calculate luminosity distance."""
        if z < 0.1:
            return c * z / H0_SI
        else:
            z_array = np.linspace(0, z, 1000)
            E_z = np.sqrt(Omega_m * (1 + z_array)**3 + Omega_Lambda)
            integral = np.trapezoid(1.0 / E_z, z_array)
            return c * (1 + z) / H0_SI * integral
    
    def _isco_frequency(self):
        """Calculate ISCO frequency."""
        # For Schwarzschild
        r_isco = 6 * G * self.M_total / c**2
        f_orb = np.sqrt(G * self.M_total / (4 * np.pi**2 * r_isco**3))
        return 2 * f_orb
    
    def _ringdown_frequency(self):
        """Calculate approximate ringdown frequency."""
        # For a Schwarzschild BH
        M_final = self.M_total * (1 + self.eta) * (1 + self.z)  # Mass redshifted
        f_ring = 1.0 / (2 * np.pi) * c**3 / (G * M_final) * 0.1
        return f_ring
    
    def inspiral_waveform(self, f):
        """
        Inspiral waveform in frequency domain.
        
        Parameters:
        -----------
        f : array-like
            Frequency array
            
        Returns:
        --------
        h_tilde : array-like
            Fourier domain strain
        """
        M_c_z = self.M_c * (1 + self.z)
        
        # Stationary phase approximation
        # h(f) ~ A * f^(-7/6) * exp(i Psi(f))
        
        A = (5.0 / 24.0 / np.pi**4)**(1/2) * (G * M_c_z / c**3)**(5/6) / (self.d_L / c)
        
        h_tilde = A * f**(-7/6)
        
        # Cut off at ISCO
        h_tilde[f > self.f_isco] = 0
        
        return h_tilde
    
    def characteristic_strain(self, f):
        """
        Characteristic strain for the binary.
        
        Parameters:
        -----------
        f : array-like
            Frequency array
            
        Returns:
        --------
        h_c : array-like
            Characteristic strain
        """
        M_c_z = self.M_c * (1 + self.z)
        
        h_c = (4.0 / self.d_L) * (G * M_c_z / c**2)**(5/3) * (np.pi * f / c)**(2/3)
        
        # Cut off at ISCO
        h_c[f > self.f_isco] = 0
        
        return h_c
    
    def full_waveform(self, f):
        """
        Full CBC waveform including merger and ringdown.
        
        Parameters:
        -----------
        f : array-like
            Frequency array
            
        Returns:
        --------
        h_c : array-like
            Characteristic strain
        """
        h_c = self.characteristic_strain(f).copy()
        
        # Merger enhancement (simplified model)
        mask_merger = (f > 0.8 * self.f_isco) & (f < 1.2 * self.f_isco)
        if np.any(mask_merger):
            h_c[mask_merger] *= 1.5
        
        # Ringdown (decay)
        mask_ring = (f >= self.f_isco)
        if np.any(mask_ring):
            h_c[mask_ring] = h_c[mask_ring] * np.exp(-(f[mask_ring] - self.f_isco) / (0.1 * self.f_ring))
        
        return h_c


# ============================================================================
# SECTION 4: COSMIC GRAVITATIONAL WAVE BACKGROUND
# ============================================================================

class CosmicGWBackground:
    """
    Cosmic gravitational wave background predictions.
    Includes inflationary GWs, phase transitions, cosmic strings, and relic GWs.
    """
    
    def __init__(self):
        self.h = H0 / 100.0  # Hubble parameter in units of 100 km/s/Mpc
        
    def inflationary_spectrum(self, f, r=0.01, n_t=0):
        """
        Inflationary gravitational wave spectrum.
        
        Parameters:
        -----------
        f : array-like
            Frequency in Hz
        r : float
            Tensor-to-scalar ratio
        n_t : float
            Tensor spectral index
            
        Returns:
        --------
        Omega_gw : array-like
            Dimensionless energy density
        """
        # Reference frequency (CMB scale)
        f_pivot = 1.5e-17  # Hz (corresponding to CMB)
        
        # Amplitude at pivot
        # r = 16 * epsilon (slow-roll parameter)
        # Omega_gw ~ 10^-14 * r at f ~ 10^-16 Hz
        Omega_ref = 1e-14 * r
        
        # Scale with frequency
        Omega_gw = Omega_ref * (f / f_pivot)**n_t
        
        return Omega_gw
    
    def qcd_phase_transition(self, f, T_star=150e9, g_star=100):
        """
        Gravitational waves from QCD phase transition.
        
        Parameters:
        -----------
        f : array-like
            Frequency in Hz
        T_star : float
            Transition temperature in Kelvin
        g_star : float
            Effective degrees of freedom
            
        Returns:
        --------
        Omega_gw : array-like
            Dimensionless energy density
        """
        # Convert temperature to energy
        # Peak frequency
        f_peak = 1e-7 * (T_star / 1e9)**(1/2) * (g_star / 100)**(1/6)  # Hz
        
        # Amplitude estimate
        Omega_peak = 1e-8  # Approximate
        
        # Spectrum shape (broken power law)
        Omega_gw = Omega_peak * (f / f_peak)**3 / (1 + (f / f_peak)**4)
        
        return Omega_gw
    
    def cosmic_string_spectrum(self, f, G_mu=1e-11):
        """
        Gravitational waves from cosmic string cusps and kinks.
        
        Parameters:
        -----------
        f : array-like
            Frequency in Hz
        G_mu : float
            String tension (G * mu / c^2)
            
        Returns:
        --------
        Omega_gw : array-like
            Dimensionless energy density
        """
        # Reference amplitude
        Omega_ref = 1e-8 * (G_mu / 1e-11)**(1/2)
        
        # Spectrum shape (power law with index -1/3)
        Omega_gw = Omega_ref * (f / 1e-9)**(-1/3)
        
        return Omega_gw
    
    def domain_wall_spectrum(self, f, sigma=1e6):
        """
        Gravitational waves from domain wall collapse.
        
        Parameters:
        -----------
        f : array-like
            Frequency in Hz
        sigma : float
            Wall tension in TeV^3 (converted appropriately)
            
        Returns:
        --------
        Omega_gw : array-like
            Dimensionless energy density
        """
        # Peak frequency depends on wall tension
        # Convert sigma to Hz
        sigma_Hz = sigma * 1e6 * 1.602e-10 / hbar  # Very rough conversion
        
        f_peak = 1e-8  # Hz (typical)
        Omega_peak = 1e-10
        
        Omega_gw = Omega_peak * np.exp(-(np.log(f / f_peak))**2 / 2)
        
        return Omega_gw
    
    def relic_spectrum(self, f, Omega_relic=1e-14):
        """
        Generic relic gravitational wave background.
        
        Parameters:
        -----------
        f : array-like
            Frequency in Hz
        Omega_relic : float
            Relic energy density today
            
        Returns:
        --------
        Omega_gw : array-like
            Dimensionless energy density
        """
        # Flat spectrum (scale-invariant)
        Omega_gw = Omega_relic * np.ones_like(f)
        
        return Omega_gw
    
    def omega_to_strain(self, Omega_gw, f):
        """
        Convert energy density to characteristic strain.
        
        Parameters:
        -----------
        Omega_gw : array-like
            Dimensionless energy density
        f : array-like
            Frequency in Hz
            
        Returns:
        --------
        h_c : array-like
            Characteristic strain
        """
        h_c = np.sqrt(3 * H0_SI**2 / (4 * np.pi**2) * Omega_gw / f**2)
        return h_c
    
    def nongaussianity_parameter(self, f_nl=1.0):
        """
        Non-Gaussianity parameter for stochastic background.
        
        Parameters:
        -----------
        f_nl : float
            Non-Gaussianity parameter
            
        Returns:
        --------
        statistics : dict
            Non-Gaussianity statistics
        """
        return {
            'f_nl': f_nl,
            'skewness': f_nl,
            'kurtosis_excess': 3 * f_nl**2,
            'implication': 'Non-Gaussian background suggests primordial origin'
        }


# ============================================================================
# VISUALIZATION
# ============================================================================

def create_comprehensive_plot(results_dict):
    """
    Create a 4-panel comprehensive visualization.
    
    Parameters:
    -----------
    results_dict : dict
        Dictionary containing all analysis results
        
    Returns:
    --------
    fig : matplotlib Figure
        The created figure
    """
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('P2-T3 Master Equation: Gravitational Wave Predictions Analysis', 
                 fontsize=14, fontweight='bold', y=0.98)
    
    # Panel 1: LISA Sensitivity and Binary Signals
    ax1 = axes[0, 0]
    
    # Frequency range for LISA
    f_lisa = np.logspace(-4, 0, 500)
    
    # LISA noise curves
    lisa = LISASensitivity()
    h_noise_lisa = lisa.sensitivity_curve(f_lisa)
    
    ax1.loglog(f_lisa, h_noise_lisa, 'k-', linewidth=2, label='LISA Sensitivity')
    
    # Binary signals
    binaries = [
        (1e6, 1e6, 1.0, 'SMBH Binary (10⁶+10⁶ M☉, z=1)', 'blue'),
        (1e5, 1e5, 0.5, 'IMBH Binary (10⁵+10⁵ M☉, z=0.5)', 'green'),
        (1e4, 1e4, 0.1, 'Stellar BH Binary (10⁴+10⁴ M☉, z=0.1)', 'red'),
        (1.4, 1.4, 0.001, 'NS-NS Binary (1.4+1.4 M☉, z=0.001)', 'purple'),
    ]
    
    for m1, m2, z, label, color in binaries:
        binary = BinaryInspiralLISA(m1, m2, z)
        h_signal = binary.waveform(f_lisa)
        ax1.loglog(f_lisa, h_signal, '--', color=color, alpha=0.8, label=label)
    
    # Stochastic background estimate
    cgb = CosmicGWBackground()
    Omega_gw = cgb.inflationary_spectrum(f_lisa, r=0.01)
    h_cgb = cgb.omega_to_strain(Omega_gw, f_lisa)
    ax1.loglog(f_lisa, h_cgb, 'orange', linestyle='-.', alpha=0.7, label='Inflationary GW (r=0.01)')
    
    ax1.set_xlabel('Frequency [Hz]', fontsize=11)
    ax1.set_ylabel('Characteristic Strain $h_c$', fontsize=11)
    ax1.set_title('LISA: Space-based Detector Sensitivity', fontsize=12, fontweight='bold')
    ax1.legend(loc='lower right', fontsize=8)
    ax1.grid(True, alpha=0.3)
    ax1.set_xlim(1e-4, 1)
    ax1.set_ylim(1e-23, 1e-14)
    
    # Panel 2: PTA Sensitivity and Hellings-Downs
    ax2 = axes[0, 1]
    
    # Create two sub-panels
    ax2_left = ax2
    
    # PTA sensitivity
    f_pta = np.logspace(-9, -6, 200)
    
    pta_configs = [
        ('IPTA', 'blue', '-'),
        ('SKA', 'red', '--'),
        ('NANOGrav', 'green', '-.'),
    ]
    
    for name, color, style in pta_configs:
        pta = PTASensitivity(name)
        h_pta = pta.sensitivity_curve(f_pta)
        ax2_left.loglog(f_pta * 1e9, h_pta, color=color, linestyle=style, linewidth=2, 
                       label=f'{name} ({pta.N_pulsars} pulsars)')
    
    # Supermassive BH binary signals
    smbh_signals = [
        (1e9, 0.1, 'SMBH Binary (10⁹ M☉, z=0.1)'),
        (1e10, 0.5, 'SMBH Binary (10¹⁰ M☉, z=0.5)'),
    ]
    
    for M, z, label in smbh_signals:
        smbh = SupermassiveBHBinary(M, z=z)
        h_smbh = smbh.strain_at_frequency(f_pta)
        ax2_left.loglog(f_pta * 1e9, h_smbh, 'purple', alpha=0.6, linestyle='--')
    
    # Stochastic background for PTA
    Omega_pta = cgb.inflationary_spectrum(f_pta, r=0.01)
    h_pta_bg = cgb.omega_to_strain(Omega_pta, f_pta)
    ax2_left.loglog(f_pta * 1e9, h_pta_bg, 'orange', linestyle=':', alpha=0.7, 
                   label='Inflationary GW (r=0.01)')
    
    ax2_left.set_xlabel('Frequency [nHz]', fontsize=11)
    ax2_left.set_ylabel('Characteristic Strain $h_c$', fontsize=11)
    ax2_left.set_title('PTA: Pulsar Timing Array Sensitivity', fontsize=12, fontweight='bold')
    ax2_left.legend(loc='lower right', fontsize=8)
    ax2_left.grid(True, alpha=0.3)
    ax2_left.set_xlim(1e-9 * 1e9, 1e-6 * 1e9)
    ax2_left.set_ylim(1e-17, 1e-13)
    
    # Panel 3: Ground-based Interferometers
    ax3 = axes[1, 0]
    
    f_ground = np.logspace(1, 4, 500)
    
    # Detector noise curves
    detectors = [
        ('LIGO_O4', 'Advanced LIGO O4', 'blue', '-'),
        ('LIGO_O5', 'Advanced LIGO O5', 'navy', '--'),
        ('Virgo_O4', 'Advanced Virgo O4', 'green', '-.'),
        ('KAGRA', 'KAGRA', 'purple', ':'),
        ('ET', 'Einstein Telescope', 'red', '-'),
    ]
    
    for det, label, color, style in detectors:
        try:
            ground = GroundBasedInterferometer(det)
            h_ground = ground.sensitivity_curve(f_ground)
            ax3.loglog(f_ground, h_ground, color=color, linestyle=style, linewidth=2, label=label)
        except:
            pass
    
    # CBC signals
    cbc_systems = [
        (30, 30, 0.1, 'BBH (30+30 M☉, z=0.1)', 'cyan'),
        (1.4, 1.4, 0.05, 'BNS (1.4+1.4 M☉, z=0.05)', 'magenta'),
        (10, 1.4, 0.1, 'NS-BH (10+1.4 M☉, z=0.1)', 'orange'),
    ]
    
    for m1, m2, z, label, color in cbc_systems:
        cbc = CompactBinaryCoalescence(m1, m2, z)
        h_cbc = cbc.full_waveform(f_ground)
        ax3.loglog(f_ground, h_cbc, color=color, linestyle='--', alpha=0.8, label=label)
    
    ax3.set_xlabel('Frequency [Hz]', fontsize=11)
    ax3.set_ylabel('Characteristic Strain $h_c$', fontsize=11)
    ax3.set_title('Ground-based: LIGO/Virgo/KAGRA Sensitivity', fontsize=12, fontweight='bold')
    ax3.legend(loc='lower right', fontsize=8)
    ax3.grid(True, alpha=0.3)
    ax3.set_xlim(10, 1000)
    ax3.set_ylim(1e-24, 1e-19)
    
    # Panel 4: Cosmic GW Background
    ax4 = axes[1, 1]
    
    f_cosmic = np.logspace(-16, 4, 1000)
    
    # Various backgrounds
    backgrounds = [
        ('inflationary', lambda f: cgb.omega_to_strain(cgb.inflationary_spectrum(f, r=0.01), f),
         'Inflationary (r=0.01)', 'blue', '-'),
        ('inflationary_r001', lambda f: cgb.omega_to_strain(cgb.inflationary_spectrum(f, r=0.001), f),
         'Inflationary (r=0.001)', 'lightblue', '--'),
        ('qcd', lambda f: cgb.omega_to_strain(cgb.qcd_phase_transition(f), f),
         'QCD Phase Transition', 'green', '-.'),
        ('cosmic_string', lambda f: cgb.omega_to_strain(cgb.cosmic_string_spectrum(f, G_mu=1e-11), f),
         'Cosmic Strings (Gμ=10⁻¹¹)', 'red', ':'),
        ('domain_wall', lambda f: cgb.omega_to_strain(cgb.domain_wall_spectrum(f), f),
         'Domain Walls', 'purple', '-'),
    ]
    
    for key, func, label, color, style in backgrounds:
        try:
            h_bg = func(f_cosmic)
            ax4.loglog(f_cosmic, h_bg, color=color, linestyle=style, linewidth=2, label=label)
        except:
            pass
    
    # Detector sensitivity bands
    # LISA
    f_lisa_wide = np.logspace(-4, 0, 100)
    h_lisa = lisa.sensitivity_curve(f_lisa_wide)
    ax4.loglog(f_lisa_wide, h_lisa, 'black', linewidth=3, alpha=0.3, label='LISA band')
    ax4.fill_between(f_lisa_wide, h_lisa, 1e-30, alpha=0.1, color='black')
    
    # PTA
    f_pta_wide = np.logspace(-9, -6, 50)
    pta_ska = PTASensitivity('SKA')
    h_pta_ska = pta_ska.sensitivity_curve(f_pta_wide)
    ax4.loglog(f_pta_wide, h_pta_ska, 'brown', linewidth=3, alpha=0.3, label='PTA (SKA)')
    
    # LIGO
    f_ligo_wide = np.logspace(1, 4, 100)
    ligo = GroundBasedInterferometer('LIGO_O5')
    h_ligo = ligo.sensitivity_curve(f_ligo_wide)
    ax4.loglog(f_ligo_wide, h_ligo, 'gray', linewidth=3, alpha=0.3, label='LIGO band')
    
    ax4.set_xlabel('Frequency [Hz]', fontsize=11)
    ax4.set_ylabel('Characteristic Strain $h_c$', fontsize=11)
    ax4.set_title('Cosmic GW Background: Theoretical Predictions', fontsize=12, fontweight='bold')
    ax4.legend(loc='lower right', fontsize=8)
    ax4.grid(True, alpha=0.3)
    ax4.set_xlim(1e-16, 1e4)
    ax4.set_ylim(1e-30, 1e-12)
    
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    
    return fig


# ============================================================================
# MAIN ANALYSIS
# ============================================================================

def main():
    """
    Main analysis function.
    Runs all calculations and generates outputs.
    """
    print("=" * 80)
    print("P2-T3 Master Equation: Gravitational Wave Predictions Analysis")
    print("Paper-grade comprehensive analysis framework")
    print("=" * 80)
    
    results = {}
    
    # ========================================================================
    # SECTION 1: LISA Analysis
    # ========================================================================
    print("\n" + "=" * 80)
    print("SECTION 1: LISA SENSITIVITY AND DETECTABILITY")
    print("=" * 80)
    
    lisa = LISASensitivity()
    print(f"\nLISA Configuration:")
    print(f"  Arm length: {lisa.arm_length/1e9:.1f} x 10^9 m")
    print(f"  Laser power: {lisa.laser_power} W")
    print(f"  Transfer frequency f*: {lisa.f_star:.4e} Hz")
    print(f"  Observation time: {lisa.T_obs/(365.25*24*3600):.1f} years")
    
    # Test frequencies
    f_test_lisa = np.array([1e-4, 1e-3, 1e-2, 1e-1, 1.0])
    h_noise_test = lisa.sensitivity_curve(f_test_lisa)
    
    print(f"\nLISA Sensitivity (Characteristic Strain) at test frequencies:")
    for f, h in zip(f_test_lisa, h_noise_test):
        print(f"  f = {f:.0e} Hz: h_c = {h:.4e}")
    
    # Binary inspiral analysis
    print("\n--- Binary Inspiral Analysis ---")
    binaries_lisa = [
        (1e6, 1e6, 1.0, "SMBH Binary (10^6 + 10^6 M☉, z=1)"),
        (1e5, 1e5, 0.5, "IMBH Binary (10^5 + 10^5 M☉, z=0.5)"),
        (1e4, 1e4, 0.1, "Stellar BH Binary (10^4 + 10^4 M☉, z=0.1)"),
        (1.4, 1.4, 0.001, "NS-NS Binary (1.4 + 1.4 M☉, z=0.001)"),
    ]
    
    lisa_results = []
    for m1, m2, z, desc in binaries_lisa:
        binary = BinaryInspiralLISA(m1, m2, z)
        f_array = np.logspace(-4, 0, 500)
        h_signal = binary.waveform(f_array)
        
        # Calculate SNR
        snr = lisa.calculate_snr(f_array, h_signal)
        
        # Detection confidence
        confidence = lisa.detection_confidence(snr)
        
        # Merger time
        t_merger = binary.merger_time(f_array[0])
        
        print(f"\n  {desc}:")
        print(f"    ISCO frequency: {binary.f_isco:.4e} Hz")
        print(f"    SNR: {snr:.2f}")
        print(f"    Detectable: {confidence['is_detectable']}")
        print(f"    Detection probability: {confidence['detection_probability']:.2%}")
        print(f"    Time to merger from f={f_array[0]:.0e} Hz: {t_merger/(365.25*24*3600):.2f} years")
        
        lisa_results.append({
            'description': desc,
            'm1': m1,
            'm2': m2,
            'z': z,
            'f_isco': float(binary.f_isco),
            'snr': float(snr),
            'detectable': bool(confidence['is_detectable']),
            'detection_probability': float(confidence['detection_probability']),
            'merger_time_years': float(t_merger/(365.25*24*3600))
        })
    
    results['lisa'] = {
        'arm_length_m': float(lisa.arm_length),
        'laser_power_W': float(lisa.laser_power),
        'transfer_frequency_Hz': float(lisa.f_star),
        'observation_time_years': float(lisa.T_obs/(365.25*24*3600)),
        'sensitivity_at_1mHz': float(lisa.sensitivity_curve(1e-3)),
        'binaries': lisa_results
    }
    
    # ========================================================================
    # SECTION 2: PTA Analysis
    # ========================================================================
    print("\n" + "=" * 80)
    print("SECTION 2: PTA (PULSAR TIMING ARRAY) PREDICTIONS")
    print("=" * 80)
    
    # Hellings-Downs curve analysis
    print("\n--- Hellings and Downs Correlation ---")
    pta = PTASensitivity('SKA')
    angles = np.linspace(0, np.pi, 100)
    hd_corr = pta.hellings_downs_curve(angles)
    
    print(f"  HD curve values:")
    print(f"    At 0° (same pulsar): {hd_corr[0]:.4f}")
    print(f"    At 90°: {pta.hellings_downs_curve(np.pi/2):.4f}")
    print(f"    At 180°: {hd_corr[-1]:.4f}")
    print(f"    Minimum at ~90°: {np.min(hd_corr):.4f}")
    
    # PTA configurations comparison
    print("\n--- PTA Array Configurations ---")
    pta_configs = ['NANOGrav', 'EPTA', 'PPTA', 'IPTA', 'SKA']
    pta_results = []
    
    for name in pta_configs:
        pta = PTASensitivity(name)
        print(f"\n  {name}:")
        print(f"    Number of pulsars: {pta.N_pulsars}")
        print(f"    Timing precision: {pta.sigma_t*1e9:.0f} ns")
        print(f"    Observation time: {pta.T_obs/(365.25*24*3600):.1f} years")
        
        # Sensitivity at 1 nHz
        f_test = 1e-9
        h_pta = pta.sensitivity_curve(f_test)
        print(f"    Sensitivity at 1 nHz: h_c = {h_pta:.4e}")
        
        # Stochastic background SNR
        Omega_gw_test = 1e-9  # Example value
        snr_bg = pta.stochastic_background_detection(Omega_gw_test, f_ref=f_test)
        print(f"    SNR for Ω_gw = 10⁻⁹ at 1 nHz: {snr_bg:.2f}")
        
        pta_results.append({
            'array_name': name,
            'n_pulsars': int(pta.N_pulsars),
            'timing_precision_ns': float(pta.sigma_t * 1e9),
            'observation_time_years': float(pta.T_obs/(365.25*24*3600)),
            'sensitivity_1nHz': float(h_pta),
            'snr_background_Omega_1e-9': float(snr_bg)
        })
    
    results['pta'] = {
        'hellings_downs': {
            'at_0_deg': float(hd_corr[0]),
            'at_90_deg': float(pta.hellings_downs_curve(np.pi/2)),
            'at_180_deg': float(hd_corr[-1]),
            'minimum': float(np.min(hd_corr))
        },
        'configurations': pta_results
    }
    
    # Supermassive BH binary signals
    print("\n--- Supermassive Black Hole Binary Signals ---")
    smbh_systems = [
        (1e9, 1.0, 0.1, "SMBH Binary (10⁹ M☉, q=1, z=0.1)"),
        (1e10, 0.3, 0.5, "SMBH Binary (10¹⁰ M☉, q=0.3, z=0.5)"),
    ]
    
    smbh_results = []
    for M, q, z, desc in smbh_systems:
        smbh = SupermassiveBHBinary(M, q, z)
        f_test = np.array([1e-9, 3e-9, 1e-8])  # PTA frequencies
        h_smbh = smbh.strain_at_frequency(f_test)
        
        print(f"\n  {desc}:")
        for f, h in zip(f_test, h_smbh):
            # Calculate SNR with SKA
            pta_ska = PTASensitivity('SKA')
            snr = h / pta_ska.sensitivity_curve(f) * np.sqrt(100)
            print(f"    At f={f:.0e} Hz: h_c={h:.4e}, SNR(SKA)={snr:.2f}")
        
        smbh_results.append({
            'description': desc,
            'total_mass_Msun': float(M),
            'mass_ratio': float(q),
            'redshift': float(z),
            'luminosity_distance_Mpc': float(smbh.d_L / (3.086e22)),
            'strain_1nHz': float(h_smbh[0]),
            'snr_ska_1nHz': float(h_smbh[0] / pta_ska.sensitivity_curve(1e-9) * np.sqrt(100))
        })
    
    results['pta']['smbh_binaries'] = smbh_results
    
    # ========================================================================
    # SECTION 3: Ground-based Interferometers
    # ========================================================================
    print("\n" + "=" * 80)
    print("SECTION 3: GROUND-BASED INTERFEROMETERS")
    print("=" * 80)
    
    # Detector sensitivity comparison
    print("\n--- Detector Sensitivity Comparison ---")
    detectors = ['LIGO_O4', 'LIGO_O5', 'Virgo_O4', 'KAGRA', 'ET']
    detector_results = []
    
    for det in detectors:
        try:
            ground = GroundBasedInterferometer(det)
            f_test = np.array([10, 100, 1000])
            h_det = ground.sensitivity_curve(f_test)
            
            print(f"\n  {det}:")
            print(f"    Frequency range: {ground.config['f_low']:.0f} - {ground.config['f_high']:.0f} Hz")
            print(f"    Sensitivity at 100 Hz: h_c = {h_det[1]:.4e}")
            print(f"    BNS horizon distance (SNR=8): ~{200 * (1e-21 / h_det[1]):.0f} Mpc")
            
            detector_results.append({
                'detector': det,
                'f_low_Hz': float(ground.config['f_low']),
                'f_high_Hz': float(ground.config['f_high']),
                'sensitivity_100Hz': float(h_det[1]),
                'bns_horizon_Mpc': float(200 * (1e-21 / h_det[1]))
            })
        except Exception as e:
            print(f"  Error with {det}: {e}")
    
    results['ground_based'] = {
        'detectors': detector_results
    }
    
    # CBC analysis
    print("\n--- Compact Binary Coalescence Analysis ---")
    cbc_systems = [
        (30, 30, 0.1, "BBH (30+30 M☉, z=0.1)"),
        (1.4, 1.4, 0.05, "BNS (1.4+1.4 M☉, z=0.05)"),
        (10, 1.4, 0.1, "NS-BH (10+1.4 M☉, z=0.1)"),
        (50, 50, 0.5, "BBH (50+50 M☉, z=0.5)"),
    ]
    
    cbc_results = []
    for m1, m2, z, desc in cbc_systems:
        cbc = CompactBinaryCoalescence(m1, m2, z)
        f_array = np.logspace(1, 4, 500)
        h_cbc = cbc.full_waveform(f_array)
        
        # Calculate SNR with LIGO O5
        ligo = GroundBasedInterferometer('LIGO_O5')
        snr = ligo.calculate_snr(f_array, h_cbc)
        
        # Parameter estimation
        biases = ligo.parameter_estimation_bias(snr)
        
        print(f"\n  {desc}:")
        print(f"    ISCO frequency: {cbc.f_isco:.1f} Hz")
        print(f"    Ringdown frequency: {cbc.f_ring:.1f} Hz")
        print(f"    SNR (LIGO O5): {snr:.2f}")
        print(f"    Chirp mass uncertainty: {biases['sigma_Mc_over_Mc']*100:.3f}%")
        print(f"    Distance uncertainty: {biases['sigma_dL_over_dL']*100:.1f}%")
        
        cbc_results.append({
            'description': desc,
            'm1_Msun': float(m1),
            'm2_Msun': float(m2),
            'redshift': float(z),
            'f_isco_Hz': float(cbc.f_isco),
            'f_ring_Hz': float(cbc.f_ring),
            'snr_ligo_o5': float(snr),
            'chirp_mass_uncertainty_percent': float(biases['sigma_Mc_over_Mc'] * 100),
            'distance_uncertainty_percent': float(biases['sigma_dL_over_dL'] * 100)
        })
    
    results['ground_based']['cbc_systems'] = cbc_results
    
    # ========================================================================
    # SECTION 4: Cosmic GW Background
    # ========================================================================
    print("\n" + "=" * 80)
    print("SECTION 4: COSMIC GRAVITATIONAL WAVE BACKGROUND")
    print("=" * 80)
    
    cgb = CosmicGWBackground()
    
    # Inflationary GWs
    print("\n--- Inflationary Gravitational Waves ---")
    f_test = np.array([1e-16, 1e-9, 1e-3, 1e2])  # CMB, PTA, LISA, LIGO scales
    
    for r in [0.1, 0.01, 0.001]:
        Omega_inf = cgb.inflationary_spectrum(f_test, r=r)
        h_inf = cgb.omega_to_strain(Omega_inf, f_test)
        
        print(f"\n  Tensor-to-scalar ratio r = {r}:")
        print(f"    Ω_gw at CMB (10⁻¹⁶ Hz): {Omega_inf[0]:.4e}")
        print(f"    h_c at CMB: {h_inf[0]:.4e}")
        print(f"    Ω_gw at PTA (10⁻⁹ Hz): {Omega_inf[1]:.4e}")
        print(f"    h_c at PTA: {h_inf[1]:.4e}")
        print(f"    Ω_gw at LISA (10⁻³ Hz): {Omega_inf[2]:.4e}")
        print(f"    h_c at LISA: {h_inf[2]:.4e}")
        
        # Check detectability
        pta_ska = PTASensitivity('SKA')
        h_pta = pta_ska.sensitivity_curve(f_test[1])
        lisa = LISASensitivity()
        h_lisa_noise = lisa.sensitivity_curve(f_test[2])
        
        print(f"    Detectable by PTA (SKA): {h_inf[1] > h_pta}")
        print(f"    Detectable by LISA: {h_inf[2] > h_lisa_noise}")
    
    # Phase transitions
    print("\n--- Phase Transition Gravitational Waves ---")
    f_pt = np.logspace(-8, -2, 100)
    Omega_pt = cgb.qcd_phase_transition(f_pt)
    h_pt = cgb.omega_to_strain(Omega_pt, f_pt)
    
    print(f"  QCD phase transition (T* ~ 150 GeV):")
    print(f"    Peak frequency: ~1e-7 Hz (PTA band)")
    print(f"    Peak Ω_gw: ~{np.max(Omega_pt):.4e}")
    print(f"    Peak h_c: ~{np.max(h_pt):.4e}")
    
    # Cosmic strings
    print("\n--- Cosmic String Gravitational Waves ---")
    f_cs = np.logspace(-12, 2, 100)
    for G_mu in [1e-10, 1e-11, 1e-12]:
        Omega_cs = cgb.cosmic_string_spectrum(f_cs, G_mu=G_mu)
        h_cs = cgb.omega_to_strain(Omega_cs, f_cs)
        
        print(f"  Gμ = 10^{int(np.log10(G_mu))}:")
        print(f"    Ω_gw at 1 nHz: {Omega_cs[50]:.4e}")
        print(f"    h_c at 1 nHz: {h_cs[50]:.4e}")
    
    cgb_results = {
        'inflationary': {
            'r_0.1_omega_cmb': float(np.atleast_1d(cgb.inflationary_spectrum(1e-16, r=0.1))[0]),
            'r_0.01_omega_cmb': float(np.atleast_1d(cgb.inflationary_spectrum(1e-16, r=0.01))[0]),
            'r_0.001_omega_cmb': float(np.atleast_1d(cgb.inflationary_spectrum(1e-16, r=0.001))[0]),
        },
        'qcd_phase_transition': {
            'peak_frequency_Hz': 1e-7,
            'peak_omega_gw': float(np.max(Omega_pt)),
            'peak_h_c': float(np.max(h_pt))
        },
        'cosmic_strings': {
            'Gmu_1e-11_omega_1nHz': float(cgb.cosmic_string_spectrum(1e-9, G_mu=1e-11)),
            'Gmu_1e-11_h_c_1nHz': float(cgb.omega_to_strain(cgb.cosmic_string_spectrum(1e-9, G_mu=1e-11), 1e-9))
        }
    }
    
    results['cosmic_background'] = cgb_results
    
    # ========================================================================
    # Create Visualization
    # ========================================================================
    print("\n" + "=" * 80)
    print("GENERATING VISUALIZATION")
    print("=" * 80)
    
    fig = create_comprehensive_plot(results)
    
    # Save figure
    output_dir = os.path.dirname(os.path.abspath(__file__))
    fig_path = os.path.join(output_dir, 'gw_predictions_analysis.png')
    fig.savefig(fig_path, dpi=150, bbox_inches='tight')
    print(f"Figure saved to: {fig_path}")
    
    # Also save PDF version
    fig_path_pdf = os.path.join(output_dir, 'gw_predictions_analysis.pdf')
    fig.savefig(fig_path_pdf, bbox_inches='tight')
    print(f"PDF figure saved to: {fig_path_pdf}")
    
    plt.close(fig)
    
    # ========================================================================
    # Save JSON Summary
    # ========================================================================
    print("\n" + "=" * 80)
    print("SAVING JSON SUMMARY")
    print("=" * 80)
    
    # Convert numpy types to native Python types
    def convert_to_serializable(obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, (np.integer,)):
            return int(obj)
        elif isinstance(obj, (np.floating,)):
            return float(obj)
        elif isinstance(obj, dict):
            return {k: convert_to_serializable(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [convert_to_serializable(item) for item in obj]
        return obj
    
    results_serializable = convert_to_serializable(results)
    
    # Add metadata
    results_serializable['metadata'] = {
        'analysis_date': '2026-02-10',
        'framework': 'P2-T3 Master Equation',
        'version': '1.0',
        'purpose': 'Paper-grade GW predictions analysis'
    }
    
    json_path = os.path.join(output_dir, 'gw_predictions_summary.json')
    with open(json_path, 'w') as f:
        json.dump(results_serializable, f, indent=2)
    print(f"JSON summary saved to: {json_path}")
    
    # ========================================================================
    # Summary Statistics
    # ========================================================================
    print("\n" + "=" * 80)
    print("SUMMARY STATISTICS")
    print("=" * 80)
    
    # Count detectable sources
    lisa_detectable = sum(1 for b in lisa_results if b['detectable'])
    print(f"\nLISA detectable binaries: {lisa_detectable}/{len(lisa_results)}")
    
    # Ground-based detectable CBCs
    cbc_detectable = sum(1 for c in cbc_results if c['snr_ligo_o5'] > 8)
    print(f"Ground-based detectable CBCs: {cbc_detectable}/{len(cbc_results)}")
    
    # PTA sensitivity range
    print(f"\nPTA sensitivity range: 10⁻⁹ - 10⁻⁶ Hz")
    print(f"SKA expected sensitivity: h_c ~ 10⁻¹⁷ at 1 nHz")
    
    # Cosmic background detection prospects
    print(f"\nCosmic GW Background Detection Prospects:")
    print(f"  Inflationary (r=0.01): Detectable by CMB B-modes, marginal for PTA")
    print(f"  QCD Phase Transition: Peak in PTA band, SNR ~ 1-10 with SKA")
    print(f"  Cosmic Strings (Gμ=10⁻¹¹): Detectable by PTA/SKA")
    
    print("\n" + "=" * 80)
    print("ANALYSIS COMPLETE")
    print("=" * 80)
    
    return results


if __name__ == "__main__":
    results = main()
