"""
Pomysly na dalsze rozwiniecie programu:

- klasy zamiast funkcji!
- wyliczanie dystansu korzysta z tych samych danych, co airport df, ale kod jest powielony - fix this!
- do wyszukiwania lotnisk wokol wybranego dodac tez opcje wyszukiwania lotnisk wokol danej lokalizacji (zadanej przez dlugosc/szerokosc geogr, a moze po nazwie -> wyszukanie jej pozycji w Google Maps?)
- program wyszukuje jedynie najlepszej oferty na danym kierunku, stworzyc petle wyszukujaca wiele lotow w danym kierunku w danym interwale czasowym i je sortowac
- po zadaniu IATA_arrival, program wyszukuje lot na dane lotnisko, ale na zyczenie takze na pobliskie (np. do X km wg ortodromy)
- moze dodatkowy warunek wylotu/powrotu w okreslone dni tygodnia?
- codzienne sprawdzanie cen, gdy spadnie ponizej np. 15 EUR, poinformuj mailem

"""

# Co wiemy o ich API?

#	Flight info:
	#	https://api.ryanair.com/flightinfo/3/flights/?&arrivalAirportIataCode=SZZ&departureAirportIataCode=WAW&departureTimeScheduled \
	#	From=00:00&departureTimeScheduledTo=23:59&length=&number=&offset=

#	Currencies:
	#	https://desktopapps.ryanair.com/pl-pl/res/currencies

#	Calendar:
	#	https://desktopapps.ryanair.com/Calendar?Destination=WAW&IsTwoWay=TRUE&Months=16&Origin=SZZ&StartDate=2017-04-06

#	Schedule:
	#	https://api.ryanair.com/timetable/3/schedules/SZZ/WAW/years/2017/months/05

#	One-way Fares:
	# https://api.ryanair.com/farefinder/3/oneWayFares?&departureAirportIataCode=BCN&language=en&limit=16&market=en-gb&offset=0&outboundDepartureDateFrom=2016-10-11&outboundDepartureDateTo=2017-10-28&priceValueTo=150

# 	Cheapest per day:
	#	https://api.ryanair.com/farefinder/3/oneWayFares/SXF/TSR/cheapestPerDay?market=de-de&outboundMonthOfDate=2017-04-01
	
#	Round Trip Fares:
	# https://api.ryanair.com/farefinder/3/roundTripFares?&arrivalAirportIataCode=STN&departureAirportIataCode=VLC&inboundDepartureDateFrom=2016-10-11&inboundDepartureDateTo=2017-10-28&language=es&limit=16&market=es-es&offset=0&outboundDepartureDateFrom=2016-10-11&outboundDepartureDateTo=2017-10-28&priceValueTo=150


#	Availability and fares info:
	#	https://desktopapps.ryanair.com/en-gb/availability?ADT=1&CHD=0&DateIn=2017-04-02&DateOut=2017-04-10&Destination=WAW&FlexDaysIn=6&FlexDaysOut=6&INF=0&Origin=SZZ&RoundTrip=true&TEEN=0

# Discounts
	#	https://api.ryanair.com/discount/3/discounts

# Markets/language codes:
	#	https://www.ryanair.com/content/ryanair.markets.json

# wykaz lotnisk 
	#   https://api.ryanair.com/aggregate/3/common?embedded=airports&market=en-gb

#	Airports (names, IATA, coordinates, time-zones):
	#	https://desktopapps.ryanair.com/en-gb/res/stations

#	All together:
	# https://api.ryanair.com/aggregate/3/common?embedded=airports,countries,cities,regions,nearbyAirports,defaultAirport&market=en-gb

