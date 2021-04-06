import xarray as xr
import numpy as np
import argparse
import pandas as pd
import xskillscore as xs

# define target file: Imerg data ranging (at least) from 12/13/2000 to 01/31/2020
# window need to be <= 20.
# utc defines 24-hour time range of accumulated precipitation in imerg data which ranges either from 00-00 UTC or 06-06 UTC.

target = "imergall.nc4"


parser = argparse.ArgumentParser()
parser.add_argument('--year', '-y', required = True, help='year used for evaluation')
parser.add_argument('--window','-w',required=True, help='window to use for EPC construction')
parser.add_argument('--utc','-utc',default=0, help='either 0 or 6: Accumulated precipitation starting at 0 UTC or 6 UTC')
args = parser.parse_args()

year = int(args.year)
window = int(args.window)
utc = args.utc

if window > 20:
    raise ValueError('in this code window can not be larger than 20')
if window < 0:
    raise ValueError('window must be a positiv value')
if utc != 0 or utc != 6:
    raise ValueError('utc must be either 0 or 6')
if year <=2000 or year > 2019:
    raise ValueError('year must be in the range of 2001 - 2019')


ensemble_len = (window*2+1)*18
year2 = year+1

if utc == 6:
    tttime = pd.date_range(start='12/13/2000T06', end='01/31/2020T06')
    obs_day  = pd.date_range(start='01/02/'+str(year)+'T06', end='01/01/'+str(year2)+'T06')
else:
    tttime = pd.date_range(start='12/13/2000', end='01/31/2020')
    obs_day  = pd.date_range(start='01/02/'+str(year), end='01/01/'+str(year2))
    
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

obsjan = np.concatenate((0, year_indx_jan), axis=None)+20
obsrest = np.concatenate((0, year_indx_rest), axis=None)+20

lon_target = DS_target.lon.values
lat_target= DS_target.lat.values

obs = xr.DataArray(
       np.random.rand( len(lat_target), len(lon_target)),
       coords=[lat_target, lon_target],
       dims=["lat", "lon"],
       name='var'
   )

fct = xr.DataArray(
       np.random.rand( ensemble_len, len(lat_target ), len(lon_target )),
       coords=[np.arange(ensemble_len), lat_target , lon_target],
       dims=["member", "lat", "lon"],
       name='var'
   )

year_sel = year - 2001
year_sel = int(year_sel)

ensembleindx = ensembleindexjan 
ensemblerows = np.delete(ensembleindx, year_sel, 0)

ensemble =  DS_target['precipitationCal'][ensemblerows.flatten(),:,:]

fct[:,:,:] = ensemble
DS_obs_sel = DS_target.sel(time = obs_day[0])
obs[:,:] = DS_obs_sel["precipitationCal"][:,:]
crps0 = xs.crps_ensemble(obs, fct, dim=[])

for day in range(1,365):
    if day < 59:

        ensembleindx = ensembleindexjan + day
        ensemblerows = np.delete(ensembleindx, year_sel, 0)
    else:

        ensembleindx = ensembleindexrest + day
        ensemblerows = np.delete(ensembleindx, year_sel, 0)

    ensemble =  DS_target['precipitationCal'][ensemblerows.flatten(),:,:]
    fct[:,:,:] = ensemble

    DS_obs_sel = DS_target.sel(time = obs_day[day])
    obs[:,:] = DS_obs_sel["precipitationCal"][:,:]
    crps1 = xs.crps_ensemble(obs, fct, dim=[])
    both = xr.concat([crps0, crps1], dim="new")
    crps0 = both.sum(dim="new")

crps0 = crps0/365  
crps0.to_netcdf("./results_score/EPC15_crps_"+str(window)+"_"+str(year)+".nc")
