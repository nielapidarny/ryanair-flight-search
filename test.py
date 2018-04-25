import sys
sys.path.insert(0, 'C:\\1. Patryk\\Data science\\repos\\ryanair-flight-search')
import Ryanair
import pandas as pd

IATA_departure = 'WMI'  # Flight departure location, IATA code
IATA_arrival = 'BAR'       # Flight arrival location, IATA code (optional)
dep_out_date_from = '2018-05-01' # Earliest departure date of an outbound flight
dep_out_date_to = '2018-05-07'   # Latest departure date of an outbound flight
dep_in_date_from = '2018-05-05'  # Earliest departure date of an inbound flight
dep_in_date_to = '2018-05-15'    # Latest departure date of an inbound flight

"""
for date_out in pd.date_range(dep_out_date_from, dep_out_date_to, freq='D'):
    dep_out_date_from = date_out
    dep_out_date_to = date_out
    for date_in in pd.date_range(dep_in_date_from, dep_in_date_to, freq='D'):
        dep_in_date_from = date_in
        dep_in_date_to = date_in
        print(date_out, " - ", date_in)
        Ryanair.n_way(ways=2)
"""

# zaciąga parametru z pliku Ryanair...

for date_out in pd.date_range(dep_out_date_from, dep_out_date_to, freq='D'):
    dep_out_date_from = date_out
    dep_out_date_to = date_out
    print(IATA_departure, " - ", IATA_arrival, ": ", date_out)
    Ryanair.n_way(ways=1)

x = IATA_departure 
IATA_departure = IATA_arrival
IATA_arrival = x

for date_in in pd.date_range(dep_in_date_from, dep_in_date_to, freq='D'):
    dep_in_date_from = date_in
    dep_in_date_to = date_in
    print(IATA_departure, " - ", IATA_arrival, ": ", date_in)
    Ryanair.n_way(ways=1)