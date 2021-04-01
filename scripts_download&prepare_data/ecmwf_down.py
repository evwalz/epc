from ecmwfapi import ECMWFService
import pandas as pd

server = ECMWFService("mars")
  
date_end = pd.date_range(start='2012-01-01', end='2020-01-01', freq='M')
date_start = pd.date_range(start='2012-01-01', end='2019-12-02', freq='MS')

for x, y in zip(date_start, date_end):
    date = x.strftime('%Y-%m-%d') +'/to/'+y.strftime('%Y-%m-%d')
    datestemp = date[14:21]
    target = 'Prtl6_%s.nc' % (datestemp)
    server.execute({
        "class"   : "od",
        "stream"  : "enfo",
        "expver"  : "1",
        "type"    : "cf",
        "levtype" : "sfc",
        "time"    : "00",
        "step"    : "6",
        "date"    : date,
        "param"   : "228.128",
        "grid"    : "0.25/0.25",
        "format"  : "netcdf",
        },
        target)

