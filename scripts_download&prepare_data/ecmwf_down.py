from ecmwfapi import ECMWFService

server = ECMWFService("mars")
  
dates = ['2018-12-31/to/2019-01-30', '2019-01-31/to/2019-02-27', '2019-02-28/to/2019-03-30', '2019-03-31/to/2019-04-29', '2019-04-30/to/2019-05-30', '2019-05-31/to/2019-06-29', '2019-06-30/to/2019-07-30',
             '2019-07-31/to/2019-08-30', '2019-08-31/to/2019-09-29', '2019-09-30/to/2019-10-30', '2019-10-31/to/2019-11-29', '2019-11-30/to/2019-12-30']


for date in dates:
    datestemp = date[14:21]
    target = 'operational24_%s.nc' % (datestemp)
    server.execute({
        "class"   : "od",
        "stream"  : "enfo",
        "expver"  : "1",
        "type"    : "cf",
        "levtype" : "sfc",
        "time"    : "00",
        "step"    : "24",
        "date"    : date,
        "param"   : "228.128",
        "grid"    : "0.25/0.25",
        "format"  : "netcdf",
        },
        target)

