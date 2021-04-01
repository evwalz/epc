import xarray as xr

import argparse 

parser = argparse.ArgumentParser()
parser.add_argument('--year', '-y', required = True, help='year of ensemble values')
args = parser.parse_args()

year = str(args.year)

ens30 = xr.open_dataset("PrtCtrl30_cutlat_invert_mm_"+year+".nc")
ens6 = xr.open_dataset("PrtCtrl6_cutlat_invert_mm_"+year+".nc")

ens6_new = ens6.assign_coords(time = ens30.time.values)
ens24 = ens30 - ens6_new

ens24.to_netcdf('PrtCtrl24_cutlat_invert_mm_'+year+'.nc')

