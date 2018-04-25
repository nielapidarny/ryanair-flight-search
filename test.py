import sys
sys.path.insert(0, 'C:\\1. Patryk\\Data science\\repos\\ryanair-flight-search')
import Ryanair
import pandas as pd

IATA_departure = 'SXF'  # Flight departure location, IATA code
IATA_arrival = 'INI'       # Flight arrival location, IATA code (optional)
dep_out_date_from = pd.to_datetime('2018-05-01') # Earliest departure date of an outbound flight
dep_out_date_to = pd.to_datetime('2018-05-07')   # Latest departure date of an outbound flight
dep_in_date_from = pd.to_datetime('2018-05-05')   # Earliest departure date of an inbound flight
dep_in_date_to = pd.to_datetime('2018-05-15')    # Latest departure date of an inbound flight

i = 0 
for date_out in pd.date_range(dep_out_date_from, dep_out_date_to, freq='D'):
    for date_in in pd.date_range(dep_in_date_from, dep_in_date_to, freq='D'):
        i = i+ 1
        print(date_out, " - ", date_in, i)
        # Ryanair.n_way(ways=1)
