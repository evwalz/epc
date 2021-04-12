#!/bin/bash

# Loop through input files for each year
while read line 
do
	filein=$line
	echo $filein
	bname=`basename $filein`
	basename=${bname%%.HDF5}

# Convert to netCDF
	ncks $filein in.nc

# Cut out variable precipitationCal and latitude range from 39.95S to 39.95N
	ncl 01b_conv2nc.ncl

# Remap to 0.25deg grid
	cdo remap,targetgrid.txt,weights2.nc out.nc ${basename}_025_WORLD.nc
	rm in.nc out.nc
done < ifiles
exit
