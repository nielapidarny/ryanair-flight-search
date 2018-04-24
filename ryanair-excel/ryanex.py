import requests
import datetime
import copy
import numpy as np
import pandas as pd
import xlwings as xw
import geopy.distance
from operator import itemgetter

#########  PARAMETERS #########

# Default values
Language = 'pl'         # Language in which airport names are displayed
Limit = '100'           # Maximum number of displayed flights 
Offset = '0'            # ? No idea, no official API documentation
Flex_in = '0'           # The number of extra days to include with DateIn 
Flex_out = '0'          # The number of extra days to include with DateOut 

def get_url(ways):
    '''Creating an URL to query Ryanair website'''

    if ways == 1:
        if IATA_arrival:
            return 'https://api.ryanair.com/farefinder/3/oneWayFares?'  + \
            '&arrivalAirportIataCode=' + IATA_arrival + \
            '&departureAirportIataCode=' + IATA_departure + \
            '&language=' + Language +   '&limit=' + Limit + '&FlexDaysIn=' + \
            Flex_in + '&FlexDaysOut=' + Flex_out +'&market=' + Language + '-' + \
            Language + '&offset=' + Offset + '&outboundDepartureDateFrom=' + \
            dep_out_date_from + '&outboundDepartureDateTo=' + \
            dep_out_date_to + '&priceValueTo=' + Price_value 
        else:
            return 'https://api.ryanair.com/farefinder/3/oneWayFares?'  + \
            '&departureAirportIataCode=' + IATA_departure + \
            '&language=' + Language +   '&limit=' + Limit + '&FlexDaysIn=' + \
            Flex_in + '&FlexDaysOut=' + Flex_out +'&market=' + Language + '-' + \
            Language + '&offset=' + Offset + '&outboundDepartureDateFrom=' + \
            dep_out_date_from + '&outboundDepartureDateTo=' + \
            dep_out_date_to + '&priceValueTo=' + Price_value 

    if ways == 2:
        if IATA_arrival:    
            return 'https://api.ryanair.com/farefinder/3/roundTripFares?' + \
            '&arrivalAirportIataCode=' + IATA_arrival + \
            '&departureAirportIataCode=' + IATA_departure + \
            '&inboundDepartureDateFrom=' + dep_in_date_from + \
            '&inboundDepartureDateTo=' + dep_in_date_to + \
            '&language=' + Language +   '&limit=' + Limit + '&FlexDaysIn=' + \
            Flex_in + '&FlexDaysOut=' + Flex_out +'&market=' + Language + '-' + \
            Language + '&offset=' + Offset + '&outboundDepartureDateFrom=' + \
            dep_out_date_from + '&outboundDepartureDateTo=' + \
            dep_out_date_to + '&priceValueTo=' + Price_value 
        else:
            return 'https://api.ryanair.com/farefinder/3/roundTripFares?' + \
            '&departureAirportIataCode=' + IATA_departure + \
            '&inboundDepartureDateFrom=' + dep_in_date_from + \
            '&inboundDepartureDateTo=' + dep_in_date_to + \
            '&language=' + Language +   '&limit=' + Limit + '&FlexDaysIn=' + \
            Flex_in + '&FlexDaysOut=' + Flex_out +'&market=' + Language + '-' + \
            Language + '&offset=' + Offset + '&outboundDepartureDateFrom=' + \
            dep_out_date_from + '&outboundDepartureDateTo=' + \
            dep_out_date_to + '&priceValueTo=' + Price_value 

def find_fares(ways):
    '''Getting JSON data containing lowest fares from Ryanair website'''

    # Connecting to Ryanair website
    url = get_url(ways)
    r = requests.get(url) 

    # Saving response  
    result  = r.json()
    return result['fares']


def get_vals(flight, key, one, two = 0):   
    '''Fares is a list of dictionaries that consist of 3 keys: outbound, inbound, summary
    We need to dig deeper inside their values, sub-values and sub-subvalues'''

    temp = []
    if two:
        temp = [v[one][two] for k,v in flight.items() if k == key]
    else:
        temp = [v[one] for k,v in flight.items() if k == key]
    return temp[0]


def clean_results(ways):
    ''' Results from JSON file are in a really ugly form. Let's make it more readable'''

    fares = find_fares(ways)
    flights_clean = []
    lowest_fares = {}
    
    for flight in fares:
        # Przygotowujemy slownik dla każdego kolejnego lotniska z listy
        lowest_fares['airport'] = get_vals(flight, 'outbound', 'arrivalAirport', 'name')
        lowest_fares['currency'] = get_vals(flight, 'outbound','price', 'currencyCode')
        lowest_fares['date'] =  get_vals(flight, 'outbound','departureDate')[:10]
        if ways == 2: lowest_fares['date_back'] = get_vals(flight,'inbound','departureDate')[:10]
        lowest_fares['price_main'] = int(get_vals(flight, 'summary', 'price', 'valueMainUnit'))
        lowest_fares['price_frac'] = int(get_vals(flight, 'summary', 'price', 'valueFractionalUnit'))
        lowest_fares['price_total'] = lowest_fares['price_main'] + lowest_fares['price_frac']/100
        flights_clean.append(copy.copy(lowest_fares)) # nasza zbiorcza lista wzbogaca sie o kolejny slownik-lotnisko, ALE UWAGA! Musi byc kopia, bo inaczej dane sie nadpisuja
    
    return flights_clean

def print_results(ways, flights_clean):
    ''' Printing out to the screen the lowest fares sorted by price '''
 
    # itemgetter: sort the list of dictionaries by the price
    flights_clean = sorted(flights_clean, key=itemgetter('price_main'), reverse=False) 

    airport = np.zeros(len(flights_clean)).astype(str)
    price = np.zeros(len(flights_clean)).astype(float)
    currency = np.zeros(len(flights_clean)).astype(str)
    date = np.zeros(len(flights_clean)).astype(str)
    if ways ==2: date_back = np.zeros(len(flights_clean)).astype(str)

    for i, flight in enumerate(flights_clean):
        airport[i] = flight['airport']
        price[i] = flight['price_total']
        currency[i] = flight['currency']
        date[i] = flight['date']
        if ways ==2: date_back[i] = flight['date_back']

    if ways == 1:
        df = pd.DataFrame({'Airport': airport, 'Price': price, 'Currency': currency, 'Date': date})
        df = df[['Airport', 'Price', 'Currency', 'Date']]
    if ways == 2: 
        df = pd.DataFrame({'Airport': airport, 'Price': price, 'Currency': currency, 'Date': date, 'Date_back': date_back})
        df = df[['Airport', 'Price', 'Currency', 'Date', 'Date_back']]
    return df 
  

def go():
    ''' Getting clean results '''

    global dep_out_date_from
    global dep_out_date_to 
    global dep_in_date_from 
    global dep_in_date_to 
    global IATA_departure
    global IATA_arrival
    global Price_value
    global x_way 
              

    wb = xw.Book.caller()

    dep_out_date_from = str(wb.sheets['Fares'].range('B2').value.strftime('%Y-%m-%d'))
    dep_out_date_to = str(wb.sheets['Fares'].range('B3').value.strftime('%Y-%m-%d'))
    dep_in_date_from = str(wb.sheets['Fares'].range('B4').value.strftime('%Y-%m-%d'))
    dep_in_date_to = str(wb.sheets['Fares'].range('B5').value.strftime('%Y-%m-%d'))
    Price_value = str(int(wb.sheets['Fares'].range('B6').value))
    IATA_departure = str(wb.sheets['Fares'].range('B7').value)
    IATA_arrival = str(wb.sheets['Fares'].range('B8').value)
    if IATA_arrival == 'None': IATA_arrival = ''
    x_way = int(wb.sheets['Fares'].range('B9').value)

    # wb.sheets['Fares'].range('D1').value = get_url(int(float(x_way)))

    wb.sheets['Fares'].range('D:H').clear()

    flights_clean = clean_results(x_way)
    wb.sheets['Fares'].range('D1').options(index=False).value = print_results(x_way, flights_clean)


############################################################################################################################################3


def find_airports():
    '''Getting JSON data containing all airports within Ryanairscope of interest'''

    # Connecting to Ryanair website
    url = 'https://api.ryanair.com/aggregate/3/common?embedded=airports&market=en-gb'
    r = requests.get(url) 

    # Saving response  
    result  = r.json()
    list_of_airports = result['airports']
    return list_of_airports

def create_airports_df():
    '''Creating a dataframe containing IATA codes and coordinates of airports'''
    
    airports = find_airports()
    iata = [''] * len(airports)
    name = [''] * len(airports)
    lat =  [''] * len(airports)
    lon =  [''] * len(airports)

    for i, airport in enumerate(airports):
        iata[i] = airport['iataCode']
        name[i] = airport['name']
        lat[i] = airport['coordinates']['latitude']
        lon[i] = airport['coordinates']['longitude']

    df = pd.DataFrame({'IATA_code': iata, 'Name': name, 'Latitude': lat, 'Longitude': lon})
    df = df.set_index('Name')
    df = df.sort_index()
    return df

def find_iata():
    '''Submenu for browsing and filtering airport dataframe'''
    wb = xw.Book.caller()
    df = create_airports_df()
    reg = str(wb.sheets['IATA'].range('B2').value)
    wb.sheets['IATA'].range('D:G').clear()
    wb.sheets['IATA'].range('D1').options(index=True).value = df[df.index.str.contains(reg)]


############################################################################################################################################3

def nearby_airports():
    '''Submenu for finding nearby airports'''
    
    wb = xw.Book.caller()

    df = create_airports_df()
    airports = df.index.values
    df = df.set_index('IATA_code', drop=False)

    dist = []
    k = wb.sheets['Airports'].range('B2').value
    reg = str(wb.sheets['Airports'].range('B3').value)
    if reg in df.index:
        lon = df.loc[reg,'Latitude']
        lat = df.loc[reg,'Longitude']
        coords_1 = (lon, lat)

        for index, row in df.iterrows():
            lon = row['Latitude']
            lat = row['Longitude']
            coords_2 = (lon, lat)
            dist.append(geopy.distance.vincenty(coords_1, coords_2).km)            
        
        dist_df = pd.DataFrame({'IATA_code': df.index, 'Airport': airports,'distance (km)': dist})
        dist_df = dist_df.set_index('IATA_code').sort_values(by=['distance (km)'])
        dist_df = dist_df[dist_df['distance (km)'] <= int(k)]
        wb.sheets['Airports'].range('D:G').clear()
        wb.sheets['Airports'].range('D1').options(index=True).value = dist_df
    else:
        wb.sheets['Airports'].range('D:G').clear()
        wb.sheets['Airports'].range('D1').value = "This IATA code doesn't exist!"    