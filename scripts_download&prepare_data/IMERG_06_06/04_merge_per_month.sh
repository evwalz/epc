#!/bin/bash

# Merge single daily files to monthly files of daily data
# Needs to be adjusted or manually done for December 2000 and January 2020

yyyy=2001
while [ $yyyy -le 2019 ] ;
do
    echo $yyyy
    cdo -r mergetime IMERG_025_daily_WORLD/3B-HHR.MS.MRG.3IMERG.day.${yyyy}01??.V06B.025_WORLD.nc IMERG_025_WORLD_day/3B-HHR.MS.MRG.3IMERG.day.${yyyy}01.V06B.025_WORLD.nc
    cdo -r mergetime IMERG_025_daily_WORLD/3B-HHR.MS.MRG.3IMERG.day.${yyyy}02??.V06B.025_WORLD.nc IMERG_025_WORLD_day/3B-HHR.MS.MRG.3IMERG.day.${yyyy}02.V06B.025_WORLD.nc
    cdo -r mergetime IMERG_025_daily_WORLD/3B-HHR.MS.MRG.3IMERG.day.${yyyy}03??.V06B.025_WORLD.nc IMERG_025_WORLD_day/3B-HHR.MS.MRG.3IMERG.day.${yyyy}03.V06B.025_WORLD.nc
    cdo -r mergetime IMERG_025_daily_WORLD/3B-HHR.MS.MRG.3IMERG.day.${yyyy}04??.V06B.025_WORLD.nc IMERG_025_WORLD_day/3B-HHR.MS.MRG.3IMERG.day.${yyyy}04.V06B.025_WORLD.nc
    cdo -r mergetime IMERG_025_daily_WORLD/3B-HHR.MS.MRG.3IMERG.day.${yyyy}05??.V06B.025_WORLD.nc IMERG_025_WORLD_day/3B-HHR.MS.MRG.3IMERG.day.${yyyy}05.V06B.025_WORLD.nc
    cdo -r mergetime IMERG_025_daily_WORLD/3B-HHR.MS.MRG.3IMERG.day.${yyyy}06??.V06B.025_WORLD.nc IMERG_025_WORLD_day/3B-HHR.MS.MRG.3IMERG.day.${yyyy}06.V06B.025_WORLD.nc
    cdo -r mergetime IMERG_025_daily_WORLD/3B-HHR.MS.MRG.3IMERG.day.${yyyy}07??.V06B.025_WORLD.nc IMERG_025_WORLD_day/3B-HHR.MS.MRG.3IMERG.day.${yyyy}07.V06B.025_WORLD.nc
    cdo -r mergetime IMERG_025_daily_WORLD/3B-HHR.MS.MRG.3IMERG.day.${yyyy}08??.V06B.025_WORLD.nc IMERG_025_WORLD_day/3B-HHR.MS.MRG.3IMERG.day.${yyyy}08.V06B.025_WORLD.nc
    cdo -r mergetime IMERG_025_daily_WORLD/3B-HHR.MS.MRG.3IMERG.day.${yyyy}09??.V06B.025_WORLD.nc IMERG_025_WORLD_day/3B-HHR.MS.MRG.3IMERG.day.${yyyy}09.V06B.025_WORLD.nc
    cdo -r mergetime IMERG_025_daily_WORLD/3B-HHR.MS.MRG.3IMERG.day.${yyyy}10??.V06B.025_WORLD.nc IMERG_025_WORLD_day/3B-HHR.MS.MRG.3IMERG.day.${yyyy}10.V06B.025_WORLD.nc
    cdo -r mergetime IMERG_025_daily_WORLD/3B-HHR.MS.MRG.3IMERG.day.${yyyy}11??.V06B.025_WORLD.nc IMERG_025_WORLD_day/3B-HHR.MS.MRG.3IMERG.day.${yyyy}11.V06B.025_WORLD.nc
    cdo -r mergetime IMERG_025_daily_WORLD/3B-HHR.MS.MRG.3IMERG.day.${yyyy}12??.V06B.025_WORLD.nc IMERG_025_WORLD_day/3B-HHR.MS.MRG.3IMERG.day.${yyyy}12.V06B.025_WORLD.nc
    ((yyyy++))
done
exit
