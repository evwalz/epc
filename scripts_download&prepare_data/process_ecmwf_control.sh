#!/bin/bash

cdo mergetime operational*.nc operatinal2019.nc

cdo sellonlatbox,-180,180,-40,40 operatinal2019.nc operational2019_2.nc

cdo invertlat operatinal2019_2.nc operational2019_tropics.nc