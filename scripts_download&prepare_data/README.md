## Download and process data

**ECMWF ensemble**

Consists of 51 members: 1 control and 50 perturbed members. In the analysis 24-hour forecasts for accumulated precipitation initialized at 06 UTC are considered.Therefore, ensemble forecasts initialized at 00 UTC with step size 30 and step size 6 are downloaded and difference is computed to obtain the final 24-hour product from 06:00 - 06:00 UTC.   

1. **ecmwf_down.py** and **ecmwf_down_pf.py**

    Download ensemble. Successively use 6 and 30 for attribute "step" in the download script. 

2. **process_ecmwf.sh**

   Cut out relevant region (180W, 180E, 40N, 40S) and convert latitude to fit IMERG data format. Operation is applied over monthly files seperatly for control and   perturbed forecasts and step size 30 and 6.

3. **combine_ensemble.py**
 
    Combine control and perturbed for one step size (30 or 6) and convert from m to mm.
 
4. **subtract_ensemble**
 
     Compute difference between ensemble with step 30 and step 6.

**IMERG**

1. **process_imerg.sh**
 
    Conservative remapping of IMERG to fit resolution of ECMWF ensemble (0.25x0.25)
    

2. **IMERG_06_06**
    
    Create IMERG data with accumulated precipitation ranging from 06:00 - 06:00 UTC using CDO and NCL. Successively run the 4 scripts with number 01 up to 04.

