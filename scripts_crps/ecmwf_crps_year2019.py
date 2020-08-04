import numpy as np
import xarray as xr
import xskillscore as xs
import pandas as pd

perturbed = xr.open_mfdataset('/Prtl_*_tropics.nc', concat_dim='time')
control = xr.open_dataset('control2019.nc')
imerg = xr.open_dataset('imerg_regridcon.nc4')

control = control.assign_coords(number = 0.0)
ensemble = xr.concat([control, perturbed], dim="number")
ensemble = ensemble*0.001
ensemble.tp.attrs['units'] = 'mm'
tttime = pd.date_range(start='01/01/2019', end='12/31/2019')
imerg2019 = imerg.sel(time = tttime)
#imerg2019 = imerg2019.rename_vars({"precipitationCal": "tp"})

obs3 = xr.DataArray(
    np.random.rand(321, 1440),
    coords=[imerg2019['lat'].values, imerg2019['lon'].values],
    dims=["lat", "lon"]
)
fct3 = xr.DataArray(
    np.random.rand(321, 1440, 51),
    coords=[imerg2019['lat'].values, imerg2019['lon'].values, np.arange(51)],
    dims=["lat", "lon", "member"],
)

day = tttime[0]
ensembleday = ensemble.sel(time=day)
ensembleday = ensembleday.drop('time')
observation = imerg2019.sel(time=day)
observation = observation.drop('time')
obs3[:,:] = observation['precipitationCal'].transpose()
fct3[:,:,:] = ensembleday['tp']
crpsday0 = xs.crps_ensemble(obs3, fct3, dim="member")
crpsday0 = crpsday0.assign_coords(time = day)
# crps values
for day in tttime[1:]:
    ensembleday = ensemble.sel(time=day)
    ensembleday = ensembleday.drop('time')
    observation = imerg2019.sel(time=day)
    observation = observation.drop('time')
    obs3[:,:] = observation['precipitationCal'].transpose()
    fct3[:,:,:] = ensembleday['tp']
    crpsday1 = xs.crps_ensemble(obs3, fct3, dim="member")
    crpsday1 = crpsday1.assign_coords(time = day)
    crpsday0 = xr.concat([crpsday0, crpsday1], dim='time')
    
crpsday0.to_netcdf('crps_ecmwf_2019.nc')
