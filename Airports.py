import requests
import pandas as pd

def find_airports():
    '''Getting JSON data containing all airports within Ryanairscope of interest'''

    # Connecting to Ryanair website
    url = 'https://api.ryanair.com/aggregate/3/common?embedded=airports&market=en-gb'
    r = requests.get(url) 
    if r.ok:
        print("Status code:", r.status_code)
    else:
        print("HTTP %i - %s, Message %s" % (r.status_code, r.reason, r.text))

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


def airport_menu():
    '''Submenu for browsing and filtering airport dataframe'''
    
    df = create_airports_df()
    print('\n' + str(len(df.index)) + 'airports were found.')

    choice = None
    while choice != "0":
        reg = input('Type the (English, if exists) name of the airport you\'re looking for: ')
        
        if df.index.str.contains(reg).any():
            print('\n')
            print(df[df.index.str.contains(reg)])
        else:
            print('No match!')

        print('\nHave you found everything you were looking for?')
        choice = input('If yes - type 0 and press Enter, if not - simply press Enter: ')