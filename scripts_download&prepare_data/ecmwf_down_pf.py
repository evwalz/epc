from ecmwfapi import ECMWFService
import pandas as pd

server = ECMWFService("mars")
  
date_end = pd.date_range(start='2012-01-01', end='2020-01-01', freq='M')
date_start = pd.date_range(start='2012-01-01', end='2019-12-02', freq='MS')
    
for x, y in zip(date_start, date_end):
    date = x.strftime('%Y-%m-%d') +'/to/'+y.strftime('%Y-%m-%d')
    datestemp = date[14:21]
    target = 'Prtl30_%s.nc' % (datestemp)
    server.execute({
        "class"   : "od",
        "stream"  : "enfo",
        "expver"  : "1",
        "type"    : "pf",
        "levtype" : "sfc",
        "number" : "1/2/3/4/5/6/7/8/9/10/11/12/13/14/15/16/17/18/19/20/21/22/23/24/25/26/27/28/29/30/31/32/33/34/35/36/37/38/39/40/41/42/43/44/45/46/47/48/49/50",
        "time"    : "00",
        "step"    : "30",
        "date"    : date,
        "param"   : "228.128",
        "grid"    : "0.25/0.25",
        "format"  : "netcdf",
        },
        target)

