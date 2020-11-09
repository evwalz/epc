import numpy as np
import xarray as xr
import xskillscore as xs
import pandas as pd

#######################################################################
# set year_ff one of 18 or 19
year_ff = 19

# read in ecmwf data for 2018 or 2019:
perturbed = xr.open_mfdataset('Prtl_tropics_20'+str(year_ff)+'_*.nc', concat_dim='time')
control = xr.open_dataset('control_tropics_20'+str(year_ff)+'.nc')

imerg = xr.open_dataset('imerg_regridcon.nc4')

########################################################################

control = control.assign_coords(number = 0.0)
ensemble = xr.concat([control, perturbed], dim="number")
ensemble = ensemble*1000
ensemble.tp.attrs['units'] = 'mm'
tttime = pd.date_range(start='01/01/20'+str(year_ff), end='12/31/20'+str(year_ff))
imerg_year = imerg.sel(time = tttime)


obs3 = xr.DataArray(
    np.random.rand(321, 1440),
    coords=[imerg_year['lat'].values, imerg_year['lon'].values],
    dims=["lat", "lon"]
)
fct3 = xr.DataArray(
    np.random.rand(321, 1440, 51),
    coords=[imerg_year['lat'].values, imerg_year['lon'].values, np.arange(51)],
    dims=["lat", "lon", "member"],
)

day = tttime[0]
ensembleday = ensemble.sel(time=day)
ensembleday = ensembleday.drop('time')
observation = imerg_year.sel(time=day)
observation = observation.drop('time')
obs3[:,:] = observation['precipitationCal'].transpose()
fct3[:,:,:] = ensembleday['tp']
crpsday0 = xs.crps_ensemble(obs3, fct3, dim="member")
crpsday0 = crpsday0.assign_coords(time = day)
# crps values
for day in tttime[1:]:
    ensembleday = ensemble.sel(time=day)
    ensembleday = ensembleday.drop('time')
    observation = imerg_year.sel(time=day)
    observation = observation.drop('time')
    obs3[:,:] = observation['precipitationCal'].transpose()
    fct3[:,:,:] = ensembleday['tp']
    crpsday1 = xs.crps_ensemble(obs3, fct3, dim="member")
    crpsday1 = crpsday1.assign_coords(time = day)
    crpsday0 = xr.concat([crpsday0, crpsday1], dim='time')
    
crpsday0.to_netcdf('crps_ecmwf_20'+str(year_ff)+'.nc')
