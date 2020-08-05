#!/bin/bash

filedir="Prtl24_2018-"
filedir2="Prtl2018-"
ending=".nc"
ending2="_cut.nc"
ending3="_tropics.nc"
months="01 02 03 04 05 06 07 08 09 10 11 12"
	
for month in $months
do
	filein1="$filedir$month$ending"
	fileout1="$filedir2$month$ending2"
	cdo sellonlatbox,-180,180,-40,40 $filein1 $fileout1
done


for month in $months
do
	filein1="$filedir2$month$ending2"
	fileout1="$filedir2$month$ending3"
	cdo invertlat $filein1 $fileout1
done
