## Download and process data

**ECMWF ensemble**

Consists of 51 members: 1 control and 50 perturbed members. In the analysis 24-hour forecasts for accumulated precipitation initialized at 06 UTC are considered.Therefore, ensemble forecasts initialized at 00 UTC with step size 30 and step size 6 are downloaded and difference is computed to obtain the final 24-hour product from 06:00 - 06:00 UTC.   

1. Download ensemble with: *ecmwf_down.py* and *ecmwf_down_pf.py*. Successively use 6 and 30 for attribute "step" in the download script. 

2. Cut out relevant region (180W, 180E, 40N, 40S) and convert latitude to fit IMERG data format: *process_ecmwf.sh*

3. Compute difference between ensemble with step 30 and step 6 and convert unit from m in mm: *combine_ensemble.py*

**IMERG**

1. Create IMERG data with accumulated precipitation ranging from 06:00 - 06:00 UTC 

2. Conservative remapping of IMERG to fit resolution of ECMWF ensemble (0.25x0.25): *process_imerg.sh*


