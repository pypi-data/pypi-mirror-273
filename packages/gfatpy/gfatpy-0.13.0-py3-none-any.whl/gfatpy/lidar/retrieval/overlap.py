from matplotlib import pyplot as plt
import pandas as pd
import xarray as xr
import numpy as np
from scipy.integrate import cumtrapz


from gfatpy.lidar.retrieval.klett import klett_rcs
from gfatpy.lidar.retrieval.raman import retrieve_backscatter, retrieve_extinction
from gfatpy.lidar.utils.utils import refill_overlap, signal_to_rcs
from gfatpy.atmo.rayleigh import molecular_properties


def overlap_iterative(elastic_signal: xr.DataArray, 
                      raman_signal: xr.DataArray,                      
                      meteo_profiles: pd.DataFrame, 
                      particle_lidar_ratio: float, 
                      reference: tuple[float, float] = (8000,8500), 
                      wavelengths: tuple[float, float] = (532, 531), 
                      beta_aer_ref: float = 0, 
                      min_overlap_range: float = 200, #minimum range of overlap function
                      particle_angstrom_exponent: float = 0.,
                      iteration_limit: int= 10,
                      **kwargs: dict
                      ) -> tuple[xr.DataArray, np.ndarray, np.ndarray]:
    """Retrieve overlap function by means of the Wandinger's method. 

    Args:
        elastic_signal (xr.DataArray): Elastic lidar signal at wavelength `wavelengths[0]`.
        raman_signal (xr.DataArray): Raman lidar signal at wavelength `wavelengths[1]`.        
        meteo_profiles (pd.DataFrame): from  `gfatpy.atmo.atmo.generate_meteo_profiles` with pressure and temperature data.
        particle_lidar_ratio (float): Particle lidar ratio to be used in the Klett inversion. It shall be chosen so Klett backscatter profile fits Raman backscatter profile once full overlap is reached.    
        reference (tuple[float, float], optional): Reference range required by the Klett and Raman inversions. Defaults to (8000,8500).
        wavelengths (tuple[float, float], optional): Elastic and Raman wavelengths. Defaults to (532, 531).
        beta_aer_ref (float, optional): Particle backscatter coefficient at `reference range` in m^-1sr^-1. Defaults to 0 m^-1sr^-1.
        particle_angstrom_exponent (float, optional): Particle extinction-related Angstrom exponent. It is used in the Raman inversion. Defaults to 0.
        min_overlap_range (float, optional): Overlap function will be forced to zero below [m]. Defaults to 200 m.

    Returns:
        xr.DataArray: overlap function.
    """    
    #Check z in elastic and raman signals (the same for both signals)
    if len(elastic_signal.range) != len(raman_signal.range):
        raise   ValueError("elastic and Raman signals must have the same 'range' dimension.")
        
    if len(elastic_signal.range) != len(meteo_profiles['height']):
        raise   ValueError("Signals range dimension and meteo_profiles['heights'] must have the same size.")

    z = elastic_signal.range.values
    
    mol_properties = molecular_properties(wavelengths[0], meteo_profiles['pressure'], meteo_profiles['temperature'], heights=z)
    molecular_backscatter = mol_properties['molecular_beta'].values
    pressure = meteo_profiles['pressure'].values
    temperature = meteo_profiles['temperature'].values

    #Beta Klett
    elastic_backscater = klett_rcs(signal_to_rcs(elastic_signal, z),
                        z,
                        molecular_backscatter,
                        lr_part=particle_lidar_ratio,
                        reference = reference
                        ) 
    
    extinction = retrieve_extinction(
        raman_signal.values, 
        z, 
        wavelengths, 
        pressure, 
        temperature, 
        reference=reference,
    ) 

    #Refill extinction
    extinction = refill_overlap(extinction, z, kwargs.get('fulloverlap_height', 600.))

    fig, ax = plt.subplots()
    ax.plot(extinction*1e6, z)
    ax.set_xlabel('Extinction [m^-1]')
    ax.set_ylabel('Altitude [m]')
    ax.set_xlim(0, 500)
    fig.savefig('extinction.png')

    raman_backscatter = retrieve_backscatter(
        raman_signal.values, 
        elastic_signal.values,
        extinction, 
        z, 
        wavelengths, 
        pressure, 
        temperature, 
        particle_angstrom_exponent=particle_angstrom_exponent) #Fine mode has been chosen in Amstrong exponent 
    
    i = 0
    corrected_signal = np.zeros([iteration_limit, len(elastic_signal)])
    delta_overlap = np.zeros(corrected_signal.shape)
    elastic_backscatter_matrix = np.zeros(corrected_signal.shape)
    corrected_signal[i,:] = elastic_signal
    elastic_backscatter_matrix[i,:] = elastic_backscater
    delta_overlap[i,:] = (raman_backscatter - elastic_backscatter_matrix[i,:]) / (raman_backscatter + molecular_backscatter)

    #Iteraciones restantes
    for i in range(1, iteration_limit):
        corrected_signal[i,:] = corrected_signal[i-1, :] * (1 + delta_overlap[i-1,:])
        rcs_ = signal_to_rcs(corrected_signal[i,:], z)
        elastic_backscatter_matrix[i,:] = klett_rcs(rcs_,
                                z,
                                molecular_backscatter,
                                lr_part=particle_lidar_ratio,
                                beta_aer_ref=beta_aer_ref
                                )
        
        delta_overlap[i,:] = (raman_backscatter - elastic_backscatter_matrix[i,:]) / (raman_backscatter + molecular_backscatter)
    overlap_function = (corrected_signal[0,:] / corrected_signal[-1,:]) 

    #Set to zero the values of overlap function below 200 m
    overlap_function[:np.where(z > min_overlap_range)[0][0]] = 0
    
    #Search first 1 in overlap function
    first_1 = np.where(overlap_function >= 1)[0][0]

    #Set constant profile to 1 form first 1 up
    overlap_function[first_1:] = 1

    return overlap_function, elastic_backscatter_matrix, raman_backscatter

def overlap_function_explicit(elastic_rcs: xr.DataArray, 
                              raman_rcs: xr.DataArray,
                              wavelengths: tuple[float, float],
                              reference_height: float,
                              particle_lidar_ratio: float,
                              meteo_profiles: pd.DataFrame, 
                              **kwargs: dict) -> np.ndarray:
    """Retrieve overlap function by means of the explicit method.

    Args:

        - elastic_rcs (xr.DataArray): Elastic range corrected signal at wavelength `wavelengths[0]`.
        - raman_rcs (xr.DataArray): Raman range corrected signal at wavelength `wavelengths[1]`.
        - wavelengths (tuple[float, float]): Elastic and Raman wavelengths.
        - reference_height (float): Aerosol-free region reference height in meters.
        - particle_lidar_ratio (float): Assumed particle lidar ratio.
        - meteo_profiles (pd.DataFrame): Meteo profiles with pressure and temperature data from `gfatpy.atmo.atmo.generate_meteo_profiles`.

    Returns:

        - np.ndarray: overlap function.

    References:

        - Comerón et al., 2023: https://doi.org/10.5194/amt-16-3015-2023
    """    
    
    r = elastic_rcs.range.values
    dr = r[1] - r[0]

    elastic_mol_properties = molecular_properties(wavelengths[0], meteo_profiles['pressure'], meteo_profiles['temperature'], heights=z)
    raman_mol_properties = molecular_properties(wavelengths[1], meteo_profiles['pressure'], meteo_profiles['temperature'], heights=z)

    
    # Computation of beta molecular for elastic and Raman signal
    beta_mol_el = elastic_mol_properties['molecular_beta']*1000 # it has to be in km-1*sr-1
    beta_mol_ra = raman_mol_properties['molecular_beta']*1000

    # Cálculo inverso de beta molecular, a partir de la señal Rayleigh
    X = elastic_rcs.values # elastic signal
    X_Ray = X_Ray # molecular backscatter normalized to RCS

    XR = raman_rcs.values # raman signal
    XR_Ray = XR_Ray # molecular backscatter normalized to RCS


    ref_height = reference_height / 1e3 # Reference height (km)
    idx = np.round(ref_height / dr).astype(int)
    X_ref = X_Ray[idx]
    XR_ref = XR_Ray[idx]
    beta_mol_ref = beta_mol_el[idx]

    nXR = XR/XR_ref
    nbeta_mol = beta_mol_el/beta_mol_ref

    Sa = particle_lidar_ratio # Assumed Lidar Ratio
    Sm_el = elastic_mol_properties['molecular_lidar_ratio']
    # Sm_ra = raman_mol_properties['molecular_lidar_ratio']

    beta_mol_el = beta_mol_el[:idx]
    beta_mol_ra = beta_mol_ra[:idx]
    nbeta_mol = nbeta_mol[:idx]
    nXR = nXR[:idx]
    X = X[:idx]

    fexp = np.exp(-2 * (Sa - Sm_el) * np.flip(cumtrapz(np.flip(beta_mol_el), initial=0, dx=dr)))

    #Not used because its efect is negligible
    # fexp_dif_ext_mol = np.exp(- Sm_el * np.flip(cumtrapz(np.flip(beta_mol_el - beta_mol_ra), initial=0, dx=dr)))

    g = (nbeta_mol/nXR) * fexp

    phi = (2 * beta_mol_el / (nXR * X_ref)) * fexp

    psi = (X * Sa) / fexp

    phi_psi = phi * psi

    fexp_phi_psi = np.exp(np.flip(cumtrapz(np.flip(phi_psi), initial=0, dx=dr)))

    fint_g_psi = np.flip(cumtrapz(np.flip(g * psi /fexp_phi_psi), initial=0, dx=dr))

    f = g + phi * fexp_phi_psi * fint_g_psi

    Oe = 1/f

    return Oe