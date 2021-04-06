# -*- coding: utf-8 -*-
"""
Created on Mon Mar  1 08:00:16 2021

@author: walz
"""
import xarray as xr
import numpy as np
import xskillscore as xs
import argparse 

parser = argparse.ArgumentParser()
parser.add_argument('--year', '-y', required = True, help='year considered')
args = parser.parse_args()

year = args.year
window = 15

ensemble_ecmwf = xr.open_dataset('PrtlCtrl24_cutlat_invert_mm_'+str(year)+'.nc')


###################################
# IMERG
DS_target = xr.open_dataset("imerg66_regridcon_update"+str(year)+".nc")
lon_target = DS_target.lon.values
lat_target = DS_target.lat.values

ensemble_ecmwf = ensemble_ecmwf.sel(latitude = lat_target)
ensemble_ecmwf = ensemble_ecmwf.sel(longitude = lon_target)
ensemble_len = 51

obs = xr.DataArray(
    np.random.rand( 365, len(lat_target), len(lon_target)),
    coords=[DS_target.time.values ,lat_target, lon_target],
    dims=["time","lat", "lon"],
    name='var'
    )
fct = xr.DataArray(
    np.random.rand(365, len(lat_target ), len(lon_target ), ensemble_len),
    coords=[DS_target.time.values, lat_target , lon_target, np.arange(ensemble_len)],
    dims=["time", "lat", "lon", "member"],
    name='var'
   )

obs[:,:,:] = DS_target["precipitationCal"].values


    
ensemble_mean = ensemble_ecmwf.mean(dim = 'number', skipna=True)

indices = np.where(np.isnan(ensemble_ecmwf['tp']))

#print('run imputation')
for i in range(len(indices[0])):
    ensemble_ecmwf.tp[indices[0][i], indices[1][i],indices[2][i],indices[3][i]] = ensemble_mean.tp[indices[0][i], indices[1][i],indices[2][i]].values

fct[:,:,:,:] = ensemble_ecmwf['tp'].values

# crps averaged over time 
crps = xs.crps_ensemble(obs, fct, dim=['time'])

crps.to_netcdf("ecmwf_crps_"+str(year)+".nc")


