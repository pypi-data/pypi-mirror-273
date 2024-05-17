import xarray as xr
import numpy as np    

def retrieve_dBZe(Ze: xr.DataArray, band: str) -> xr.DataArray:
    dBZe = xr.apply_ufunc( lambda x: 10 * np.log10(x), Ze , dask='parallelized')  # convert to dBZ, 10log10(x) = 10 * log10(x)
    dBZe.attrs = {"long_name": f"{band}-band equivalent reflectivity", "units": "dBZe"}
    return dBZe

def retrieve_PhiDP(phiDP: xr.DataArray) -> xr.DataArray:
    phiDP_data = np.rad2deg(
        phiDP
    )  # convert to deg, add -1 because convention is other way around (now the phase shift gets negative, we want it to get positive with range...) TODO: check with Alexander if that makes sense!!
    phiDP_data.attrs = {
        "standard_name": "PhiDP",
        "long_name": "Differential phase shift",
        "units": "deg",
    }
    return phiDP_data

def retrieve_KDP( 
    phiDP: xr.DataArray, moving_windows: tuple[int, int] = (30, 5)
) -> xr.DataArray:
    # time window: timewindow*timeres gives the amount of seconds over which will be averaged
    # calculate KDP from phidp directly
    range_resolution_array = np.diff(phiDP.range)
    if not "time" in phiDP.dims:
        raise ValueError("No time dimension found")
    if len(phiDP.time) < 2:
        raise ValueError(
            "dimension time found to be less than 2. KDP calculation not possible."
        )

    time_window, range_window = moving_windows
    time_rolled_phiDP = phiDP.rolling(
        time=time_window, min_periods=1, center=True
    ).mean()  # moving window average in time
    range_time_rolled_phiDP = time_rolled_phiDP.rolling(
        range=range_window, min_periods=1, center=True
    ).mean()  # moving window average in range
    specific_diff_phase_shift = range_time_rolled_phiDP.diff(dim="range") / (
        2.0 * abs(range_resolution_array) * 1e-3
    )  # in order to get °/km we need to multiply with 1e-3
    specific_diff_phase_shift = specific_diff_phase_shift.reindex(range=phiDP.range, method="nearest")
    specific_diff_phase_shift = specific_diff_phase_shift.rename(
        "specific_diff_phase_shift"
    )
    specific_diff_phase_shift.attrs = {
        "long_name": "Specific differential phase shift",
        "units": "°/km",
    }
    return specific_diff_phase_shift

def add_all_products_from_LV1(raw: xr.Dataset, band: str) -> xr.Dataset:
    # Add products becomes too big.
    # How far can we go with LV1 data? Is it need to use LV0 from the scratch?
    # Implement here the functions made by Chris
    # It may be insteresting to compare the netcdf from the RPGpy and the one from RPG software
    # There are products that can be only calculated from the spectral data
    data = raw.copy()
    data["dBZe"] = retrieve_dBZe(data["Ze"], band)    
    data["differential_phase"] = retrieve_PhiDP(data["differential_phase"])    
    data["specific_differential_phase"] = retrieve_PhiDP(data["differential_phase"]) 
    return data

def add_all_products_from_LV0(raw: xr.Dataset) -> xr.Dataset:
    data = raw.copy()       
    chirp_number = xr.DataArray(np.zeros(data.range.size), coords={'range': data.range})   
    for idx, start_chirp_ in enumerate(data['chirp_start_indices'].values):
        chirp_number.loc[{'range': data.range[start_chirp_:]}] = idx
    data['chirp_number'] = chirp_number
    data = data.assign_coords(chirp = np.sort(np.unique(chirp_number.values.astype(int))))

    # data['sensitivity_limit_h'] = 10*np.log10(data['sensitivity_limit_h'])
    # data['sensitivity_limit'] = 10*np.log10(data['sensitivity_limit'])
    # data['HSpec'] = data['HSpec'].where(data['sensitivity_limit_h']>10)#>10**(-37/10))
    # data["VSpec"] = data['VSpec'].where(data['sensitivity_limit_v']>10) 
    # data['sZDR'] = 10*np.log10(data['HSpec']) - 10*np.log10(data['VSpec'])    
    # data['sZDRmax'] = 
    return data