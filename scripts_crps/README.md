## CRPS of ECMWF ensemble and EPC forecast

**ecmwf_crps.py**

Compute CRPS for ECMWF ensemble per year verified against IMERG. Use regridded version of IMERG which is obatined by applying *process_imerg.sh* from folder [scripts_download&prepare_data](scripts_download&prepare_data).

**bg_crps_year_18_19.py**

Compute CRPS for BG for 2018 and 2019 verified against IMERG.

**epc_crps_year_all.py**

Compute CRPS for EPC by successively selecting 18 of the 19 available years and using the omitted year for evaluation. 



