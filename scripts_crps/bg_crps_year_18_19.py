# CRPS for BG distribution

from scipy.stats import gamma
import scipy.special as sc
import numpy as np
import math 
import xarray as xr
import pandas as pd

######################### set paramters ############################

dir_imerg =''
dir_berngamma = ''
year = '2019'

####################################################################

def crps_berngamma(y, p, shape, scale):
    #rate = 1/scale
        #return(y*(1-2*p))
    q = shape*scale
    p1 = gamma.cdf(y, shape, scale = scale)
    p2 = gamma.cdf(y, shape + 1, scale = scale)
    return(2*p*y*p1 -p*q*2*p2+y*(1-2*p)+p*p*q-p*p*q*(1/math.pi)*sc.beta(shape+0.5,0.5))


def crps_berngamma_nan(y,p):
    return(y*(1-2*p))


Obs_target = xr.open_dataset(dir_imerg+'imergall.nc4')
tttime = pd.date_range(start='01/01/'+year, end='12/31/'+year)
Obs2019 = Obs_target.sel(time = tttime)

mean_crps = []
for integer in range(365):
    target =  "berngamma_" + str(integer) + ".nc"
    BG_target = xr.open_dataset(dir_berngamma + target)

    shape = BG_target["shape"]
    scale = BG_target["scale"]
    p = BG_target["prob"]
    #sel = 6589+integer-167
    obsval = Obs2019.precipitationCal[integer,:,:].values
    crps_berngamma = xr.apply_ufunc(crps_berngamma, obsval,p,shape, scale)
    indxnan = np.argwhere(np.array(np.isnan(crps_berngamma)))
    for indx in indxnan:
        i = indx[0]
        j = indx[1]
        pr = p[i,j]
        y = obsval[i,j]
        crps_berngamma[i,j] = y*(1-2*pr)
    mean_crps.append(np.mean(crps_berngamma))

