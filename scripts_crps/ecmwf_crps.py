# -*- coding: utf-8 -*-
"""
Created on Mon Mar  1 08:00:16 2021

@author: walz
"""
import xarray as xr
import numpy as np
from scipy.stats import rankdata
#import argparse 

#parser = argparse.ArgumentParser()
#parser.add_argument('--latstart', '-ls', required = True, help='first number of latitude band in splitted data')
#args = parser.parse_args()

window = 15

year = int(2012)



def crpsFromAlphaBeta(alpha,beta,heaviside0,heavisideN, nMember):
    Reli = 0.0
    CRPSpot = 0.0
    for i in range(nMember+1):
        meanoi = 0.0
        meangi = 0.0
        if i == 0:
            meanbeta = np.mean(beta[:, i])
            meanoi = np.mean(heaviside0)
            if meanoi != 0:
                meangi = meanbeta / meanoi
        if i == nMember:
            meanoi = np.mean(heavisideN)
            meanalpha = np.mean(alpha[:, i])
            if meanoi != 1:
                meangi = meanalpha /(1-meanoi)
        if i>0 and i <nMember:
            meanbeta = np.mean(beta[:, i])
            meanalpha = np.mean(alpha[:, i])
            if meanbeta == 0 and meanalpha == 0:
                continue
            else:
                meanoi = meanbeta/(meanalpha+meanbeta)
                meangi = meanalpha + meanbeta
        
        pi = i/nMember
        Reli = Reli + meangi*(meanoi-pi)*(meanoi-pi)
        CRPSpot = CRPSpot + meangi*meanoi*(1-meanoi)
    CRPS = Reli + CRPSpot
    return CRPS, CRPSpot

def crps_split(ens, obs):
    ens = np.transpose(ens)
    nMember = ens.shape[1]
    nObs = len(obs)

    alpha = np.zeros((nObs, (nMember+1)))
    beta = np.zeros((nObs, (nMember+1)))

    heaviside0 = np.zeros(nObs)
    heavisideN = np.zeros(nObs)

    prev = np.sort(ens, axis = 1)

    # 1) beta
    index = np.where(obs < prev[:,0])
    beta[index, 0] = prev[index, 0]-obs[index]
    index = np.where(obs>prev[:,nMember-1])
    alpha[index, nMember] = obs[index]-prev[index, nMember-1]

    # 2) heaviside for outlier
    index = np.where(obs <= prev[:, 0])
    heaviside0[index] = 1
    index = np.where(obs <= prev[:, nMember-1])
    heavisideN[index] = 1

    # 3) non outlier
    for i in range(nMember-1):
        index = np.where(obs > prev[:, i+1])
        alpha[index, i+1] = (prev[index, i+1]-prev[index, i]).squeeze()
        index = np.where(obs < prev[:, i])
        beta[index, i+1] = (prev[index, i+1]-prev[index, i]).squeeze()
        index = np.where((prev[:, i+1]> obs) & (obs > prev[:, i]))
        alpha[index, i+1] = (obs[index] - prev[index, i]).squeeze()
        beta[index, i+1] = (prev[index, i+1] - obs[index]).squeeze()
    
    
    crps, CRPSres = crpsFromAlphaBeta(alpha,beta,heaviside0,heavisideN, nMember)
    return CRPSres

def crps_original(ens, obs):
    ens = np.transpose(ens)
    nMember = ens.shape[1]
    nObs = len(obs)

    alpha = np.zeros((nObs, (nMember+1)))
    beta = np.zeros((nObs, (nMember+1)))

    heaviside0 = np.zeros(nObs)
    heavisideN = np.zeros(nObs)

    prev = np.sort(ens, axis = 1)

    # 1) beta
    index = np.where(obs < prev[:,0])
    beta[index, 0] = prev[index, 0]-obs[index]
    index = np.where(obs>prev[:,nMember-1])
    alpha[index, nMember] = obs[index]-prev[index, nMember-1]

    # 2) heaviside for outlier
    index = np.where(obs <= prev[:, 0])
    heaviside0[index] = 1
    index = np.where(obs <= prev[:, nMember-1])
    heavisideN[index] = 1

    # 3) non outlier
    for i in range(nMember-1):
        index = np.where(obs > prev[:, i+1])
        alpha[index, i+1] = (prev[index, i+1]-prev[index, i]).squeeze()
        index = np.where(obs < prev[:, i])
        beta[index, i+1] = (prev[index, i+1]-prev[index, i]).squeeze()
        index = np.where((prev[:, i+1]> obs) & (obs > prev[:, i]))
        alpha[index, i+1] = (obs[index] - prev[index, i]).squeeze()
        beta[index, i+1] = (prev[index, i+1] - obs[index]).squeeze()
    
    
    crps, CRPSres = crpsFromAlphaBeta(alpha,beta,heaviside0,heavisideN, nMember)
    return crps

def rank_ensemble(ens):
    #print(ens.shape)
    ens = np.asarray(ens)
    nens = ens.shape[0]
    n = ens.shape[1]
    ranks = np.ones(n)
    #print(n)
    #print(nens)
    for i in range(1, n):
        for j in range(0, i):
            fct_event = ens[:, i]
            fct_nonevent = ens[:,j]
            rank1 = rankdata(np.concatenate((fct_event, fct_nonevent)), method='average')[0:int(nens)]
            pa = (np.sum(rank1)-nens*(nens+1)/2)/nens**2
            if pa > 0.5:
                ranks[i] = ranks[i] + 1
            if pa < 0.5:
                ranks[j] = ranks[j] + 1
            if pa == 0.5:
                ranks[i] = ranks[i] + 0.5
                ranks[j] = ranks[j] + 0.5
    return ranks

# not yet working with scipy
#@guvectorize(
#    "(float64[:,:], float64[:])",
#    "(nens,n) -> (n)",
#    nopython=True,
#)
def cpa_ens(ens, obs):
    print(ens.shape)
    ranks_ens = rank_ensemble(ens)
    
    #obsorder = np.argsort(obs)
    #obssort = obs[obsorder] 
    #rank_enssort = ranks_ens[obsorder]                
    forecastRank = rankdata(ranks_ens, method='average')
    responseRank = rankdata(obs, method='average')
    responseClass = rankdata(obs, method='dense')
    
    return((np.cov(responseClass,forecastRank)[0][1]/np.cov(responseClass,responseRank)[0][1]+1)/2) 



#DS_target_e = xr.open_dataset("/Users/eva/Documents/Work/data/imerg66_regridcon.nc")
ensemble_ecmwf = xr.open_dataset('/lsdf/kit/imk-tro/projects/MOD/Gruppe_Knippertz/lg4283/enseble_ECMWF/ecmwf_66_2001_2019/EPC_analysis/ensemble_final_update/PrtlCtrl24_cutlat_invert_mm_'+str(year)+'.nc')


###################################
# IMERG
#DS_target19 = DS_target_e.sel(time = pd.date_range(start='2019-01-01 06:00:00', end='2019-12-31 06:00:00'))
DS_target19 = xr.open_dataset("/home/kit/imk-tro/lg4283/EPC/Imerg/imerg66_regridcon_update"+str(year)+".nc")
lon_target_original = DS_target19.lon.values
lat_target_original = DS_target19.lat.values



for lat in np.arange(0, 289,16):    
    lat_start = int(lat)
    lat_end = int(int(lat_start) + 16)


    lon_target = lon_target_original
    lat_target = lat_target_original[lat_start:lat_end]
    DS_target19_sel = DS_target19.sel(lat = lat_target)

#DS_target19 = DS_target19.sel(lon = lon_target)
#Ensemble
#lon_sel = ensemble_ecmwf.longitude.values[600:961]
    ensemble_ecmwf_sel = ensemble_ecmwf.sel(longitude = lon_target)
    ensemble_ecmwf_sel = ensemble_ecmwf_sel.sel(latitude = lat_target)

    ensemble_len = 51
    day_dim = len(DS_target19.time.values)

    obs = xr.DataArray(
        np.random.rand( day_dim, len(lat_target), len(lon_target)),
        coords=[DS_target19.time.values ,lat_target, lon_target],
        dims=["time","lat", "lon"],
        name='var'
        )
    fct = xr.DataArray(
        np.random.rand(day_dim, len(lat_target ), len(lon_target ), ensemble_len),
        coords=[DS_target19.time.values, lat_target , lon_target, np.arange(ensemble_len)],
        dims=["time", "lat", "lon", "number"],
        name='var'
        )

    obs[:,:,:] = DS_target19_sel["precipitationCal"].values


    ensemble_ecmwf_sel = ensemble_ecmwf_sel.sel(latitude = lat_target)
    ensemble_mean = ensemble_ecmwf_sel.mean(dim = 'number', skipna=True)

    indices = np.where(np.isnan(ensemble_ecmwf_sel['tp']))

#print('run imputation')
    for i in range(len(indices[0])):
        ensemble_ecmwf_sel.tp[indices[0][i], indices[1][i],indices[2][i],indices[3][i]] = ensemble_mean.tp[indices[0][i], indices[1][i],indices[2][i]].values

    fct[:,:,:,:] = ensemble_ecmwf_sel['tp'].values

#print('start crps resolution')
    crps_resolution = xr.apply_ufunc(
        crps_split,  # first the function
        #fct_all.sel(lat = -40, lon = 0),  # now arguments in the order expected by 'interp1_np'
        fct,
        obs,
        input_core_dims=[["number", "time"], ["time"]],  # list with one entry per arg
    #output_core_dims=('lon', 'lat', 'day'),
    #output_core_dims = [["day"]],
        exclude_dims=set(("number", "time")), 
        vectorize = True,
        dask="parallelized",
        output_dtypes=[np.dtype(float)],# dimensions allowed to change size. Must be set!
        )


    crps_resolution.to_netcdf("/home/kit/imk-tro/lg4283/precip/cpa/results_ecmwf/results/ecmwf_crpsres_"+str(window)+"_lat_"+str(lat_start)+"_"+str(year)+".nc")

#print('start crps computation')
    crps_all = xr.apply_ufunc(
        crps_original,  # first the function
    #fct_all.sel(lat = -40, lon = 0),  # now arguments in the order expected by 'interp1_np'
        fct,
        obs,
        input_core_dims=[["number", "time"], ["time"]],  # list with one entry per arg
    #output_core_dims=('lon', 'lat', 'day'),
    #output_core_dims = [["day"]],
        exclude_dims=set(("number", "time")), 
        vectorize = True,
        dask="parallelized",
        output_dtypes=[np.dtype(float)],# dimensions allowed to change size. Must be set!
        )

    crps_all.to_netcdf("/home/kit/imk-tro/lg4283/precip/cpa/results_ecmwf/results/ecmwf_crps_"+str(window)+"_lat_"+str(lat_start)+"_"+str(year)+".nc")

#print('start cpa')
############################################
#cpa_out = xr.apply_ufunc(
#    cpa_ens,  # first the function
#    #fct_all.sel(lat = -40, lon = 0),  # now arguments in the order expected by 'interp1_np'
#    fct,
#    obs,
#    input_core_dims=[["number", "time"], ["time"]],  # list with one entry per arg
#    #output_core_dims=('lon', 'lat', 'day'),
#    #output_core_dims = [["day"]],
#    exclude_dims=set(("number", "time")), 
#    vectorize = True,
#    dask="parallelized",
#    output_dtypes=[np.dtype(float)],# dimensions allowed to change size. Must be set!
#)
#cpa_out.to_netcdf("/home/kit/imk-tro/lg4283/precip/cpa/results_ecmwf/results/ecmwf_cpa_"+str(window)+"_lat_"+str(lat_start)+"_"+str(year)+".nc")
#################################################
