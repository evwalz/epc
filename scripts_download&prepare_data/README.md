## Download and process data

**ECMWF ensemble**

1. Download: *ecmwf_down.py* and *ecmwf_down_pf.py*

2. Cut out relevant region (180W, 180E, 40N, 40S) and convert latitude to fit IMERG data format: *process_ecmwf_control.sh* and *process_ecmwf_perturbed.sh*

**IMERG**

1. Conservative remapping of IMERG to fit resolution of ECMWF ensemble (0.25x0.25): *process_imerg.sh*


