import xarray as xr
import xskillscore as xs
import numpy as np
import pandas as pd

###############################################################

# Set window: 0, 2, 5, 10, 15, 20
window = 2
target = "imergall.nc4"
ensemble_len = (window*2+1)*18
###############################################################

# relevant time period for EPC with window sizes between 0 - 20 for years 2001 - 2019
tttime = pd.date_range(start='12/12/2000', end='01/31/2020')

year_indx_jan = np.array([365,  730, 1095, 1461, 1826, 2191, 2556, 2922, 3287, 3652, 4017, 4383, 4748, 5113, 5478, 5844, 6209, 6574])
year_indx_rest = np.array([365,  730, 1096, 1461, 1826, 2191, 2557, 2922, 3287, 3652,4018, 4383, 4748, 5113, 5479, 5844, 6209, 6574])

indx_end = 2*window+1

DS_target_e = xr.open_dataset(target)
DS_target = DS_target_e.sel(time=tttime)


start = np.arange(0,indx_end ,1)
for indx in year_indx_rest:
    add = np.arange(indx, (indx+indx_end),1)
    start = np.append(start, add)

start2 = np.arange(0,indx_end ,1)
for indx2 in year_indx_jan:
    add2 = np.arange(indx2, (indx2+indx_end),1)
    start2 = np.append(start2, add2)

startposition = 20-window
ensembleindexrest = np.reshape(start, (19,indx_end))+startposition
ensembleindexjan = np.reshape(start2, (19,indx_end))+startposition
#endpos = len(dayyearlist)
#positionday = np.arange(0, endpos, 1)
obsjan = np.concatenate((0, year_indx_jan), axis=None)+20
obsrest = np.concatenate((0, year_indx_rest), axis=None)+20

obs = xr.DataArray(
       np.random.rand(3600, 800),
       coords=[DS_target.lon.values, DS_target.lat.values],
       dims=["lon", "lat"],
       name='var'
   )
fct = xr.DataArray(
       np.random.rand(ensemble_len, 3600, 800),
       coords=[np.arange(ensemble_len), DS_target.lon.values, DS_target.lat.values],
       dims=["member", "lon", "lat"],
       name='var'
   )


for year in range(19):
    obsindx = obsjan[year]
    ensembleindx = ensembleindexjan 
    ensemblerows = np.delete(ensembleindx, year, 0)
    obssingle = DS_target['precipitationCal'][(obsindx),:,:]
    ensemble =  DS_target['precipitationCal'][ensemblerows.flatten(),:,:]
    obs[:,:] =  obssingle
    fct[:,:,:] = ensemble
    crps0 = xs.crps_ensemble(obs, fct, dim=[])
    for day in range(1,365):
        if day < 59:
            obsindx = obsjan[year] + day
            ensembleindx = ensembleindexjan + day
            ensemblerows = np.delete(ensembleindx, year, 0)
        else:
            obsindx = obsrest[year] + day
            ensembleindx = ensembleindexrest + day
            ensemblerows = np.delete(ensembleindx, year, 0)
        obssingle = DS_target['precipitationCal'][(obsindx),:,:]
        ensemble =  DS_target['precipitationCal'][ensemblerows.flatten(),:,:]
        obs[:,:] =  obssingle
        fct[:,:,:] = ensemble
        crps1 = xs.crps_ensemble(obs, fct, dim=[])
        both = xr.concat([crps0, crps1], dim="new")
        crps0 = both.sum(dim="new")
    crps0 = crps0/365  
    crps0.to_netcdf("crps_"+str(window)+"_"+str(2001+year)+".nc4")  
