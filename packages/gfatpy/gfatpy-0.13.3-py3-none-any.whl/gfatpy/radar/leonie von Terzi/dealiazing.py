import os
import time
import numpy as np
import pandas as pd
import xarray as xr
import glob as glob
from sys import argv

# from netCDF4 import Dataset
import math
import matplotlib.pyplot as plt
from datetime import date
import time
import multiprocessing
import warnings

# warnings.filterwarnings("ignore")  # TODO don't use normally!!!


def dealiaze(data):
    n_cores = 16  # multiprocessing.cpu_count()
    # if n_cores > 1:
    # 	n_cores = n_cores - 1 # we have the main function running on one core and our institute does not allow to use all cores
    breakpoint()
    pool = multiprocessing.Pool(n_cores)
    Nyquvist = data.nyquist_velocity.values  # [6.350626, 4.981658, 2.61496353]
    RangeEnd = data.maximum_altitude.values  # [715.4785, 5902.698, 17994.29]
    doppLen = data.doppLen.values #TODO: check if this is range_vectors or len(range_vectors)
    vel = data.velocity_vectors.values 
    dv = np.diff(vel)[0]
    newVel = np.arange(-Nyquvist[0] * 2, Nyquvist[0] * 2 + dv, dv, dtype=np.float32)


    data["minVelH"] = xr.DataArray(
        dims=("range", "Time"), coords={"range": data.range, "Time": data.Time}
    )
    data["maxVelH"] = data["minVelH"].copy()
    data["minVelV"] = data["minVelH"].copy()
    data["maxVelV"] = data["minVelH"].copy()
    data["minVelZDR"] = data["minVelH"].copy()
    data["maxVelZDR"] = data["minVelH"].copy()
    data["HSpec_rot"] = xr.DataArray(
        dims=("Time", "range", "vel_rot"),
        coords={"vel_rot": newVel, "Time": data.Time, "range": data.range},
    )
    data["VSpec_rot"] = data["HSpec_rot"].copy()
    data["sZDR_rot"] = data["HSpec_rot"].copy()
    # - testing dealiasing:
    for tind, t in enumerate(data.Time):
        print(t.values)
        # print(data)
        dataRangeValues = data.range.where(
            np.isfinite(10 * np.log10(data.sel(Time=t).ZH)), drop=True
        )
        args = [(r, data.sel(Time=t)) for r in dataRangeValues]
        for (
            r,
            HSpec,
            VSpec,
            sZDR,
            sSNR_H,
            sSNR_V,
            maxVelH,
            minVelH,
            maxVelV,
            minVelV,
            maxVelZDR,
            minVelZDR,
            HSpec_rot,
            VSpec_rot,
            sZDR_rot,
        ) in pool.starmap(dealiazeOneHeight, args):
            data["HSpec"].loc[t, r, :] = HSpec
            data["VSpec"].loc[t, r, :] = VSpec
            data["sZDR"].loc[t, r, :] = sZDR
            data["sSNR_H"].loc[t, r, :] = sSNR_H
            data["sSNR_V"].loc[t, r, :] = sSNR_V
            data["maxVelH"].loc[r, t] = maxVelH
            data["minVelH"].loc[r, t] = minVelH
            data["maxVelV"].loc[r, t] = maxVelV
            data["minVelV"].loc[r, t] = minVelV
            data["maxVelZDR"].loc[r, t] = maxVelZDR
            data["minVelZDR"].loc[r, t] = minVelZDR
            data["HSpec_rot"].loc[t, r, :] = HSpec_rot
            data["VSpec_rot"].loc[t, r, :] = VSpec_rot
            data["sZDR_rot"].loc[t, r, :] = sZDR_rot

    return data

def dealiazeOneHeight(r,data):
	Nyquvist = data.nyquist_velocity.values#[6.350626, 4.981658, 2.61496353]
	RangeEnd = data.maximum_altitude.values#[715.4785, 5902.698, 17994.29]
	doppLen = data.doppLen.values
	vel = data.velocity_vectors.values
	dv = np.diff(vel)[0]
	newVel = np.arange(-Nyquvist[0]*2,Nyquvist[0]*2+dv,dv,dtype=np.float32)
	#print(r)
	datasel = data.sel(range=r)
	#datasel = datasel[['sZDR','HSpec','VSpec','sSNR_H','sSNR_V']]
	sZDR = datasel.sZDR
	HSpec = datasel.HSpec
	VSpec = datasel.VSpec
	sSNR_H = datasel.sSNR_H
	sSNR_V = datasel.sSNR_V
	if r > RangeEnd[1]: # get correct nyquvist vel (I already regridded everything so I need to do it like tha
		maxVel = Nyquvist[2]
		ra = RangeEnd[2]
	elif r <= RangeEnd[0]:
		maxVel = Nyquvist[0]
		ra = RangeEnd[0]
	else:
		maxVel = Nyquvist[1]
		ra = RangeEnd[1]
	
	if (~np.isnan(sZDR.sel(Vel=maxVel,method='nearest')) or ~np.isnan(sZDR.sel(Vel=-maxVel,method='nearest')) or ~np.isnan(sZDR.sel(Vel=-maxVel+dv,method='nearest')) 
		or ~np.isnan(sZDR.sel(Vel=maxVel-dv,method='nearest')) or ~np.isnan(sZDR.sel(Vel=-maxVel+2*dv,method='nearest')) or ~np.isnan(sZDR.sel(Vel=maxVel-2*dv,method='nearest')) 
		or ~np.isnan(sZDR.sel(Vel=-maxVel+3*dv,method='nearest')) or ~np.isnan(sZDR.sel(Vel=maxVel-3*dv,method='nearest'))): 
	# if we have non-noise values at +- Nyquvist range or upto 3 vel bins to the right or left
		datadrop = datasel.where(data.Vel < maxVel,drop=True) #- since we regridded, I need to drop everything that is larger or smaller than +- Ny to actually kit the spectra together (otherwise we would have a lot of nan in between..)
		datadrop = datadrop.where(data.Vel > -maxVel,drop=True)
		q = len(datadrop.Vel.values)-1;
		k = 0;
		
		if np.isnan(datadrop.HSpec.isel(Vel=q)):
			datadrop.HSpec.values[q] = -99999
		for i in range(q):
			if np.isnan(datadrop.HSpec.isel(Vel=[i])) and  ~np.isnan(datadrop.HSpec.isel(Vel=[i+1])):
				datadrop.HSpec.values[i] = -99999
			elif np.isnan(datadrop.HSpec.isel(Vel=[i])) and  ~np.isnan(datadrop.HSpec.isel(Vel=[i+2])):
				datadrop.HSpec.values[i] = -99999
			elif np.isnan(datadrop.HSpec.isel(Vel=[i])) and  ~np.isnan(datadrop.HSpec.isel(Vel=[i+3])):
				datadrop.HSpec.values[i] = -99999
			elif np.isnan(datadrop.HSpec.isel(Vel=[i])) and  ~np.isnan(datadrop.HSpec.isel(Vel=[i+4])):
				datadrop.HSpec.values[i] = -99999
			elif np.isnan(datadrop.HSpec.isel(Vel=[i])) and  ~np.isnan(datadrop.HSpec.isel(Vel=[i+5])):
				datadrop.HSpec.values[i] = -99999
		if datadrop.HSpec.isnull().any(dim='Vel'):
			while ~np.isnan(datadrop.HSpec.isel(Vel=q)): #-- find out how much we need to shift
				k = k + 1;
				q = q - 1;
		# now roll the coordinates:
		datadrop = datadrop.where(datadrop.HSpec!=-99999,np.nan)
		#print(maxVel)
		dataRoll = datadrop.roll(Vel=k+1,roll_coords=False)  # shift everything, the direction doesnt matter
		
		dataRollRegridded = dataRoll.reindex({'Vel':data.Vel.values}, method = 'nearest', tolerance = 0.05) # now I need to go back to original velocity
		HSpec = dataRollRegridded.HSpec
		VSpec = dataRollRegridded.VSpec
		sZDR = dataRollRegridded.sZDR
		sSNR_H = dataRollRegridded.sSNR_H
		sSNR_V = dataRollRegridded.sSNR_V
	
	
	#- now move everything to 0 and name that rot (better for plotting)
	velMatrix = HSpec.values/HSpec.values*vel
	maxVelH = np.nanmax(velMatrix)#,axis=1)
	minVelH = np.nanmin(velMatrix)#,axis=1)
	if np.isnan(maxVelH):
		maxVelH = 0
	if np.isnan(minVelH):
		minVelH = 0
	
	velMatrix = VSpec.values/VSpec.values*vel
	maxVelV = np.nanmax(velMatrix)#,axis=1)
	minVelV = np.nanmin(velMatrix)#,axis=1)
	if np.isnan(maxVelV):
		maxVelV = 0
	if np.isnan(minVelV):
		minVelV = 0
		
	velMatrix = sZDR.values/sZDR.values*vel
	maxVelZDR = np.nanmax(velMatrix)#,axis=1)
	minVelZDR = np.nanmin(velMatrix)#,axis=1)
	if np.isnan(maxVelZDR):
		maxVelZDR = 0
	if np.isnan(minVelZDR):
		minVelZDR = 0
	#- now shift everything to 0, because we might get folding I have to increase Dopplervelocity range to have +-12
	HSpecRe = HSpec.reindex({'Vel':newVel}, method = 'nearest', tolerance = 0.05) 
	vel2rot = int((-maxVelH/dv).round())
	if datasel.maxVelV > 0:
		HSpec_rot = HSpecRe.roll(Vel=vel2rot-1,roll_coords=False)
	else:
		HSpec_rot = HSpecRe.roll(Vel=vel2rot,roll_coords=False)
	
	VSpecRe = VSpec.reindex({'Vel':newVel}, method = 'nearest', tolerance = 0.05) 	
	vel2rot = int((-maxVelV/dv).round())
	if datasel.maxVelV > 0:
		VSpec_rot = VSpecRe.roll(Vel=vel2rot-1,roll_coords=False)
	else:
		VSpec_rot = VSpecRe.roll(Vel=vel2rot,roll_coords=False)
		
	sZDRRe = sZDR.reindex({'Vel':newVel}, method = 'nearest', tolerance = 0.05) 
	vel2rot = int((-maxVelZDR/dv).round())
	if datasel.maxVelZDR > 0:
		sZDR_rot = sZDRRe.roll(Vel=vel2rot-1,roll_coords=False)
	else:
		sZDR_rot = sZDRRe.roll(Vel=vel2rot,roll_coords=False)
	return r,HSpec,VSpec,sZDR,sSNR_H,sSNR_V,maxVelH,minVelH,maxVelV,minVelV,maxVelZDR,minVelZDR,HSpec_rot,VSpec_rot,sZDR_rot
