import xarray as xr
import xskillscore as xs
import numpy as np
import pandas as pd

########################################################################

# set window:  0, 2, 5, 10, 15, 20 
window = 10

# set year for which forecast is constracted: 18, 19
year_ff = 19

# name of imerg data
target = "imergall.nc4"

# relevant time period to construct EPC from 2001 to 2018 / 2019
tttime = pd.date_range(start='12/12/2000', end='01/31/2020')

#######################################################################

if year_ff == 18:
    year_indx_jan = np.array([365,  730, 1095, 1461, 1826, 2191, 2556, 2922, 3287, 3652, 4017, 4383, 4748, 5113, 5478, 5844, 6209])
    year_indx_rest = np.array([365,  730, 1096, 1461, 1826, 2191, 2557, 2922, 3287, 3652,4018, 4383, 4748, 5113, 5479, 5844, 6209])
elif year_ff == 19:
    year_indx_jan = np.array([365,  730, 1095, 1461, 1826, 2191, 2556, 2922, 3287, 3652, 4017, 4383, 4748, 5113, 5478, 5844, 6209, 6574])
    year_indx_rest = np.array([365,  730, 1096, 1461, 1826, 2191, 2557, 2922, 3287, 3652,4018, 4383, 4748, 5113, 5479, 5844, 6209, 6574])
else:
    raise ValueError("year_ff must be 18 or 19")

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
ensembleindexrest = np.reshape(start, (year_ff,indx_end))+startposition
ensembleindexjan = np.reshape(start2, (year_ff,indx_end))+startposition
#endpos = len(dayyearlist)
#positionday = np.arange(0, endpos, 1)
obsjan = np.concatenate((0, year_indx_jan), axis=None)+20
obsrest = np.concatenate((0, year_indx_rest), axis=None)+20

time_stemp = pd.date_range(start = '01/01/20'+str(year_ff), end = '12/31/20'+str(year_ff))
year = year_ff - 1

for day in range(365):
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
    crps0 = xs.crps_ensemble(obssingle, ensemble, dim="time")
    #both = xr.concat([crps0, crps1], dim="new")
    #crps0 = both.sum(dim="new")
    #crps0 = crps0/365  
    date = pd.date_range(start = time_stemp[day], end= time_stemp[day])
    crps_dim = crps0.assign_coords(time=date[day])
    crps_dim.to_netcdf("crps"+str(year_ff)+"_"+str(window)+"_"+str(day+1)+".nc4")  
