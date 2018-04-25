import requests
from time import localtime, strftime
import copy
from operator import itemgetter

#########  PARAMETERS #########

# Default values
IATA_departure = 'SXF'  # Flight departure location, IATA code
IATA_arrival = ''       # Flight arrival location, IATA code (optional)
Language = 'pl'         # Language in which airport names are displayed
Limit = '100'           # Maximum number of displayed flights 
Offset = '0'            # ? No idea, no official API documentation
Flex_in = '0'           # The number of extra days to include with DateIn 
Flex_out = '0'          # The number of extra days to include with DateOut 
Price_value = '200'     # Maximum prize for a one-way or two-way ticket
dep_out_date_from = '2018-04-28' # Earliest departure date of an outbound flight
dep_out_date_to = '2018-05-03'   # Latest departure date of an outbound flight
dep_in_date_from ='2018-05-11'   # Earliest departure date of an inbound flight
dep_in_date_to = '2018-05-30'    # Latest departure date of an inbound flight

def change_parameters():
    ''' User defines other parameters than default ones.
    Variables must be defined as global, until the code will not be
    rewritten with classes.
    '''

    global dep_out_date_from
    global dep_out_date_to 
    global dep_in_date_from 
    global dep_in_date_to 
    global IATA_departure
    global IATA_arrival
    global Price_value 
    
    choice = None
    while choice != "0":
        print \
        ("""
        --------------- Changing flight search details ---------------
                
        0 - Back to the main menu
        1 - Change: Earliest departure date of an outbound flight
        2 - Change: Latest departure date of an outbound flight
        3 - Change: Earliest departure date of an inbound flight
        4 - Change: Latest departure date of an inbound flight
        5 - Change: Flight departure location
        6 - Change: Flight arrival location
        7 - Change: Maximum price for one-way or two-way ticket
        
        """)
        
        choice = input("Choose: ") 
        print()
            
        if choice == "0":
            print("Back to the main menu")  
        elif choice == "1":
            dep_out_date_from = input("Earliest departure date of an outbound flight (YYYY-MM-DD): ")
        elif choice == "2":
            dep_out_date_to = input("Latest departure date of an outbound flight (YYYY-MM-DD): ")
        elif choice == "3":
            dep_in_date_from = input("Earliest departure date of an inbound flight (YYYY-MM-DD): ")
        elif choice == "4":
            dep_in_date_to = input("Latest departure date of an inbound flight (YYYY-MM-DD): ") 
        elif choice == "5":
            IATA_departure = input("Flight departure location, three-letter IATA airport code: ")
        elif choice == "6":
        	iata = input('Do you want to change destination (press 1) or erase it completely, so that many locations are searched? (press 2): ')
        	if iata == "1":
        		IATA_arrival = input("Flight arrival location, three-letter IATA airport code: ")
        	if iata == "2":
        		IATA_arrival=''
        		print('/nArrival location erased!')
        elif choice == "7":
        	Price_value = input("Maximum price for one-way or two-way ticket (in departure location currency): ")
        else:
            print(" !!!!!!!!! Wrong option !!!!!!!!! ")
  
    
def show_parameters():
    ''' Displaying current parameters values'''

    print("Earliest departure date of an outbound flight: " + str(dep_out_date_from) + '\n') 
    print("Latest departure date of an outbound flight: " + str(dep_out_date_to) + '\n')
    print("Earliest departure date of an inbound flight: " + str(dep_in_date_from) + '\n')
    print("Latest departure date of an inbound flight: " + str(dep_in_date_to) + '\n')
    print("Maximum price for a one-way or two-way ticket (in departure location currency): " + str(Price_value) + '\n')
    print("Departure from: " + str(IATA_departure) + '\n')
    if IATA_arrival:
        print("Arrival in: " + str(IATA_arrival ) + '\n')
    else:
    	print("Arrival in: not specified")

def get_url(ways):
    '''Creating an URL to query Ryanair website'''

    if ways ==1:
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
    if r.ok:
        print("Status code:", r.status_code)
    else:
        print("HTTP %i - %s, Message %s" % (r.status_code, r.reason, r.text))

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
    
    # itemgetter: sort the list of dictionaries by the price
    return sorted(flights_clean, key=itemgetter('price_main'), reverse=False) 

def print_results(ways, flights_clean):
    ''' Printing out to the screen the lowest fares sorted by price '''

    print("\n\n" + IATA_departure, end='')
    
    if ways == 1:
        print(" - One-way trip: " + str(len(flights_clean)) + " offer(s) \n\n")
    if ways == 2:
        print(" - Two-way trip: " + str(len(flights_clean)) + " offer(s) \n\n")
    
    
    for flight in flights_clean:
        print (flight['airport'], end=": " )
        print (str(flight['price_total']) + ' ' + flight['currency'], end='')
        if ways == 1:
            print(" on " + flight['date'], end="\n\n")
        if ways == 2:
            print(" on " + str(flight['date']) + ' - ' + str(flight['date_back']), end="\n\n")

def txt_results(ways, flights_clean):
    ''' Saving the lowest fares to Ryanair.txt file in the current directory '''

    with open("Ryanair.txt", 'a') as f:
        f.write("================================================ \n\n")
        f.write("Script was initialized: ")
        f.write(strftime('%Y-%m-%d %H:%M:%S', localtime()))
        f.write('\n\n')
        f.write("----------------------------------------------- \n\n")
        f.write(IATA_departure)
        
        if ways == 1:
            f.write('- One-way trip: \n\n')
        if ways == 2:
            f.write('- Two-way trip: \n\n')

        for flight in flights_clean:
            f.write(str(flight['airport']) + ": ")
            f.write(str(flight['price_total']) + ' ')
            f.write(str(flight['currency']) + ' on ')
            if ways == 1:
                f.write(str(flight['date']) + "\n\n")
            if ways == 2:
                f.write(str(flight['date']) + " - ")
                f.write(str(flight['date_back']) + "\n\n")

def n_way(ways):
    ''' Getting clean results for one-way or two-way flights and printing them (to the screen + into txt file) '''

    flights_clean = clean_results(ways)
    print_results(ways, flights_clean)
    # txt_results(ways, flights_clean)
    # send_mail(toaddr="XYZ@gmail.com", subject="Wyszukiwarka lotow Ryanair", body="Patrz: załącznik", att_path="C:\\1. Patryk\\Data science\\Python\\Kody\\Raporty", att_filename="Ryanair.txt")