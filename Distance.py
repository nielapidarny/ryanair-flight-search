import pandas as pd
import geopy.distance

import sys
sys.path.insert(0, 'C:\\1. Patryk\\Data science\\repos\\ryanair-flight-search')
import Airports

def nearby_airports():
    '''Submenu for finding nearby airports'''
    
    df = Airports.create_airports_df()
    airports = df.index.values
    df = df.set_index('IATA_code', drop=False)
    choice = None
    while choice != "0":
        dist = []
        k = input('Within what radius (in km) would you like to find nearby airports? Type: ')
        reg = input('Enter the IATA code, for which you\'ll get nearest airports: ').upper()
        if reg in df.index:
            lon = df.loc[reg,'Latitude']
            lat = df.loc[reg,'Longitude']
            coords_1 = (lon, lat)
            for index, row in df.iterrows():
                lon = row['Latitude']
                lat = row['Longitude']
                coords_2 = (lon, lat)
                dist.append(geopy.distance.vincenty(coords_1, coords_2).km)            
            
            dist_df = pd.DataFrame({'IATA_code': df.index, 'Airport': airports,'distance': dist})
            dist_df = dist_df.set_index('IATA_code').sort_values(by=['distance'])
            dist_df = dist_df[dist_df['distance'] <= int(k)]
            print(dist_df)
            print('\nHave you found everything you were looking for?')
            choice = input('If yes - type 0, if not - press Enter: ')
        else:
            print('No match!')
    return dist_df # so far, this value is not in use yet