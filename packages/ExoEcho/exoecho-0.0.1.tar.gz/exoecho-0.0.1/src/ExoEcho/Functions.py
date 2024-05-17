import numpy as np
import pandas as pd
from astropy import constants as const
from astropy import units as u
import scipy.integrate as integrate

#-----# CONSTANTS #-----#
h = const.h.value # Planck constant
k_B = const.k_B.value # Boltzmann constant
c = const.c.value # speed of light in a vacuum


#-----# FUNCTIONS #-----#
# all from https://arxiv.org/abs/1502.00004 (Cowan et al 2015)

# helper function
def getConversion(units):
    if units in ["R_sun", "Rs"]:
        return const.R_sun.value
    elif units in ["R_jup", "Rj", "R_j"]:
        return const.R_jup.value
    elif units in ["R_earth", "Re", "R_e"]:
        return const.R_earth.value
    elif units in ["AU", "au"]:
        return const.au.value
    elif units in ["pc", "PC"]:
        return const.pc.value
    elif units in ["m"]:
       return 1
    elif units in ["um", "microns"]:
        return 1E-6
    elif units in ["nm"]:
        return 1E-9
    else:
        raise ValueError('Invalid units. Can choose from: "R_sun", "R_jup", "R_earth", "AU", "pc", "m", "um", "nm".') 

# planck function
def planckFunc(wavelength:float,temperature:float, wavelength_units:str="um", h:float=h, k_B:float=k_B, c:float=c)->float:    
    """Returns the Planck function as a functions wavelength, λ, and temperature, T (in Kelvin).

    Args:
        wavelength (float): The provided wavelength, in units provided by wavelength_units.
        temperature (float): The provided temperature, in Kelvin.
        wavelength_units (str, optional): Units for wavelength. Defaults to "um".
        h (float, optional): Plank's constant. Defaults to astropy's constant value h.
        k_B (float, optional): Boltzmann constant. Defaults to astropy's constant value k_B.
        c (float, optional): Speed of light in a vacuum. Defaults to astropy's constant value c.
        

    Returns:
        float: Resulting value of the Plank function given the input values for wavelength and temperature.
    """
    w_conversion = getConversion(wavelength_units)
    
    exponent = h*c/((w_conversion*wavelength)*k_B*temperature)
    return 2 * h * c ** 2 / ((w_conversion*wavelength) ** 5) / (np.exp(exponent) - 1)


# dayside emitting temperature
def Tday(T_star:float, R_star:float, a:float, Ab:float=0.3, E:float=0.2, R_units:str="R_sun", a_units:str="AU")->float:
    """Returns the dayside emitting temperature, as defined in Cowan et al 2015.

    Args:
        T_star (float): Stellar effective temperature, in K.
        R_star (float): Stellar radius, with units given by R_units. 
        a (float): Semi-major axis of planet, with units given by a_units.
        Ab (float, optional): Bond albedo. Defaults to 0.3.
        E (float, optional): Heat recirculation efficiency. Defaults to 0.2.
        R_units (str, optional): Units of provided stellar radius, R_star. Defaults to Solar radii, "R_sun".
        a_units (str, optional): Units of provided semi-major axis, a. Defaults to Astronomical units, "AU".

    Returns:
        floats: Resulting dayside emitting temperature.
    """
    # checking values for bond albedo and heat recirculation efficiency
    if Ab is None:
        Ab = 0.3
    if E is None:
        E = 0.2
    
    R_conversion = getConversion(R_units)
    a_conversion = getConversion(a_units)
    
    return T_star * (np.sqrt((R_star*R_conversion)/(a*a_conversion))) * ((1-Ab)*(2/3-E*5/12))**0.25


# thermal contrast ratio
def fluxRatio(Rp:float, R_star:float, wavelength:float, tday:float, teff:float, Rp_units:str="R_jup", R_star_units:str="R_sun", wavelength_units:str="um")->float:
    """Returns the thermal contrast ratio.

    Args:
        Rp (float): Planetary radius, in units provided by Rp_units.
        R_star (float): Stellar radius, in units provided by R_star_units.
        wavelength (float): Wavelength, in units provided by wavelength_units. Can also be a tuple or list-like data structure with two wavelengths indicating the lower bound and the upper bound of an instrument having "integrated band" capabilities.
        tday (float): Planetary dayside emitting temperature.
        teff (float): Stellar effective temperature
        Rp_units (str, optional): Units of provided planetary radius, Rp. Defaults to "R_jup".
        R_star_units (str, optional): Units of provided stellar radius, R_star. Defaults to "R_sun".
        wavelength_units (str, optional): Units of wavelength. Defaults to "um".

    Returns:
        float: Resulting thermal contrast ratio.
    """
    
    if type(wavelength) in [float, int]:
        radius_ratio = ( (Rp*getConversion(Rp_units)) / (R_star*getConversion(R_star_units)) )**2
        planck_function_planet = planckFunc(wavelength, tday, wavelength_units)
        planck_function_star = planckFunc(wavelength, teff, wavelength_units)
    
        return (radius_ratio*(planck_function_planet/planck_function_star))
    
    try:
        if len(wavelength) == 2:
            
            def integrand(wavelength):
                return fluxRatio(Rp, R_star, wavelength, tday, teff, Rp_units, R_star_units, wavelength_units)
            
        I = integrate.quad(integrand, wavelength[0], wavelength[1])
        return I[0] / abs(wavelength[0] - wavelength[1])  # Average over the wavelength range
            
    except:
        raise Exception("wavelength must be of type float or list-like with length 2.")
        
   
# Number of photons
def NPhotons(T_star:float, lambda1:float, lambda2:float, throughput:float, 
             integration_time:float, R_star:float, D_telescope:float, distance:float=20,
             wavelength_units:str="um", R_star_units:str="R_sun", distance_units="pc")->float:
    """Returns the number of photons collected by a telescope system. 

    Args:
        T_star (float): Stellar temperature, in K.
        lambda1 (float): Lower bound wavelength (i.e., minimum wavelength that system observes).
        lambda2 (float): Upper bound wavelength (i.e., maximum wavelength that system observes).
        throughput (float): System throughput (i.e., number of electrons out per photon in).
        integration_time (float): Total observation time, in s.
        R_star (float): Stellar radius, in units given by R_star_units.
        D_telescope (float): Diameter of telescope, in m.
        distance (float, optional): Distance to target. Defaults to 20pc (or whatever units provided by distance_units).
        wavelength_units (str, optional): Units for wavelength. Defaults to "um".
        R_star_units (str, optional): Stellar radius units. Defaults to solar radii, "R_sun".
        distance_units (str, optional): Distance to target units. Defaults to parsecs, "pc".

    Returns:
        float: Number of photons collected by a telescope system.
    """
    def planckInt(wavelength, T_star, wavelength_units):
        return planckFunc(wavelength, T_star, wavelength_units) * wavelength * getConversion(wavelength_units)
    
    lambda1 *= getConversion(wavelength_units)
    lambda2 *= getConversion(wavelength_units)
    I = integrate.quad(planckInt, lambda1, lambda2, args=(T_star, "m"))
    
    return np.pi**2 * throughput * integration_time / (h*c) * (R_star*getConversion(R_star_units) * D_telescope / (2*distance*getConversion(distance_units)))**2 * I[0]


# Noise estimate
def noiseEstimate(T_star:float, lambda1:float, lambda2:float, throughput:float, 
                      integration_time:float, R_star:float, D_telescope:float, distance:float=20,
                      wavelength_units="um", R_star_units:str="R_sun", distance_units="pc")->float:
    """Returns the precision (i.e., noise) estimate of a particular telescope system when observing a particular object. 

    Args:
        T_star (float): Stellar temperature, in K.
        lambda1 (float): Lower bound wavelength (i.e., minimum wavelength that system observes).
        lambda2 (float): Upper bound wavelength (i.e., maximum wavelength that system observes).
        throughput (float): System throughput (i.e., number of electrons out per photon in).
        integration_time (float): Total observation time, in s.
        R_star (float): Stellar radius, in units given by R_star_units.
        D_telescope (float): Diameter of telescope, in m.
        distance (float, optional): Distance to target. Defaults to 20pc (or whatever units provided by distance_units).
        wavelength_units (str, optional): Units for wavelength. Defaults to "um".
        R_star_units (str, optional): Stellar radius units. Defaults to solar radii, "R_sun".
        distance_units (str, optional): Distance to target units. Defaults to parsecs, "pc".

    Returns:
        float: Noise estimate given the telescope, stellar, and planetary parameters.
    """
    return 1 / np.sqrt(NPhotons(T_star, lambda1, lambda2, throughput, integration_time, R_star, D_telescope, distance, wavelength_units, R_star_units, distance_units))


# ESM estimate
def ESM(lambda1:float, lambda2:float, throughput:float, 
        integration_time:float,Rp:float, R_star:float, D_telescope:float, 
        tday:float, teff:float, wavelength:float=7.5, distance:float=20,
        wavelength_units:str="um", Rp_units:str="R_jup", R_star_units:str="R_sun", distance_units:str="pc")->float:
    """Returns the ESM based on the input parameters.

    Args:
        lambda1 (float): Lower bound wavelength (i.e., minimum wavelength that system observes).
        lambda2 (float): Upper bound wavelength (i.e., maximum wavelength that system observes).
        throughput (float): System throughput (i.e., number of electrons out per photon in).
        integration_time (float): Total observation time, in s.
        Rp (float): Planet radiy, in units given by Rp_units.
        R_star (float): Stellar radius, in units given by R_star_units.
        D_telescope (float): Diameter of telescope, in m.
        tday (float): Planet's dayside emitting temperature, in K.
        teff (float): Stellar effective temperature, in K.
        wavelength (float, optional): Representative wavelength. Defaults to 7.5.
        distance (float, optional): Distance to target. Defaults to 20pc (or whatever units provided by distance_units).
        wavelength_units (str, optional): Units for wavelength. Defaults to "um".
        Rp_units (str, optional): Planet radius units. Defaults to Jupiter radii, "R_jup".
        R_star_units (str, optional): Stellar radius units. Defaults to solar radii, "R_sun".
        distance_units (str, optional): Distance to target units. Defaults to parsecs, "pc".

    Returns:
        float: Estimated ESM
    """
    
    signal = fluxRatio(Rp, R_star, wavelength, tday, teff, Rp_units, R_star_units, wavelength_units)
    noise = noiseEstimate(teff, lambda1, lambda2, throughput, 
                              integration_time, R_star, D_telescope, distance, 
                              wavelength_units, R_star_units, distance_units)
    
    return signal / noise