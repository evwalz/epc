import xarray as xr
import argparse 

parser = argparse.ArgumentParser()
parser.add_argument('--year', '-y', required = True, help='year of ensemble values')
args = parser.parse_args()

year = str(args.year)

perturbed = xr.open_mfdataset("Prt30_cut_invert_"+year+"-*.nc", combine='by_coords')
control = xr.open_mfdataset("Ctrl30_cut_invert_"+year+"-*.nc", combine='by_coords')

control = control.assign_coords(number = 0.0)

ensemble = xr.concat([control, perturbed], dim='number') 
ensemble = ensemble * 1000 
ensemble.tp.attrs['units'] = 'mm'

ensemble.to_netcdf('PrtCtrl30_cutlat_invert_mm_'+year+'.nc')

