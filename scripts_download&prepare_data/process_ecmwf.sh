#!/bin/bash

filedir="Prt6_"
filedirout1="Prt6_cut_"
filedirout2="Prt6_cut_invert_"
ending=".nc"
months="01 02 03 04 05 06 07 08 09 10 11 12"
years="2012 2013 2014 2015 2016 2017 2018 2019"
sep="-"
for year in $years	
do
	for month in $months
	do
		filein1="$filedir$year$sep$month$ending"
		fileout1="$filedirout1$year$sep$month$ending"
		cdo sellonlatbox,-180,180,-40,40 $filein1 $fileout1
	done
done

for year in $years	
do
	for month in $months
	do
		filein1="$filedirout1$year$sep$month$ending"
		fileout="$filedirout2$year$sep$month$ending"
		cdo invertlat $filein1 $fileout
	done
done
