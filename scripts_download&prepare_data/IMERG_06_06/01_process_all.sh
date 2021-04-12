#!/bin/bash

# Textfile ifiles contains paths of half-hourly GPM IMERG final hdf files
# Needs to be slightly adjusted for November/December 2000 and January 2020

yyyy=2001
while [ $yyyy -le 2019 ] ;
do
    echo $yyyy
    grep 3B-HHR.MS.MRG.3IMERG.V06B/3B-HHR.MS.MRG.3IMERG.${yyyy} 2000-2019_infiles > ifiles

# Run 01a_process.sh to convert half-hourly files to netCDF and to remap to 0.25deg
    bash 01a_process.sh
    rm ifiles

# merge half-hourly files by day
    for mm in 01 02 03 04 05 06 07 08 09 10 11 12
    do
	d=1
	while [ $d -le 31 ] ;
	do
	    dd=`printf "%02d" $d`
	    echo $yyyy $mm $dd
	    FILE=3B*${yyyy}${mm}${dd}*S000000*nc
	    if [ -e $FILE ] ; then
		ncrcat -h 3B*${yyyy}${mm}${dd}*nc day_files/3B-HHR.MS.MRG.3IMERG.${yyyy}${mm}${dd}-S000000-E235959.V06B.025_WORLD.nc
		rm 3B*${yyyy}${mm}${dd}*nc
	    fi
	    ((d++))
	done

# merge daily files by month
	FILE=day_files/3B*${yyyy}${mm}01-S000000-E235959*nc
	if [ -e $FILE ] ; then
	    ncrcat -h day_files/3B*${yyyy}${mm}??-S000000-E235959*nc month_files/3B-HHR.MS.MRG.3IMERG.${yyyy}${mm}.V06B.025_WORLD.nc
	    rm day_files/3B*${yyyy}${mm}??-S000000-E235959*nc
	fi
    done
    ((yyyy++))
done
exit
