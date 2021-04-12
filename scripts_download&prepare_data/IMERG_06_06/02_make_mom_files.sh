#!/bin/bash

# To calculate 06-06 UTC daily sums, the monthly merged half-hourly files are needed for the previous month for the first day of the current month
# To have smaller input files: Loop over files with monthly merged half-hourly files (in directory IMERG_025_WORLD_month_files) and select last couple of days

for files in IMERG_025_WORLD_month_files/*nc
do
    bname=`basename $files`
    name=${bname%%.nc}
    echo $name
    cdo selday,28,29,30,31 $files mom_files/${name}_t.nc
done
exit
