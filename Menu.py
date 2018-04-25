import os
import sys
sys.path.insert(0, 'C:\\1. Patryk\\Data science\\repos\\ryanair-flight-search')
import Airports
import Distance
import Ryanair

# from Gmail import send_mail

os.chdir('C:\\1. Patryk\\Data science\\Python\\Kody\\Raporty')


def menu():
    ''' Printing out the menu on the screen'''

    choice = None
    while choice != "0":
        print \
        ("""
        --------------- MENU ---------------
                
        0 - Exit
        1 - Insert/change flight data
        2 - Show current flight data
        3 - Find IATA code of your airport
        4 - Check the nearest airports 
        5 - Search one-way tickets!
        6 - Search two-way tickets!
        
        """)
        
        choice = input("Choose: ") 
        print()
            
        if choice == "0":
            print("Bye bye!")  
        elif choice == "1":
            Ryanair.change_parameters()
        elif choice == "2":
            Ryanair.show_parameters()
        elif choice == "3":
            Airports.airport_menu()
        elif choice == '4':
            Distance.nearby_airports()
        elif choice == "5":
            Ryanair.n_way(ways=1)
        elif choice == "6":
            Ryanair.n_way(ways=2)
        else:
            print(" !!!!!!!!! Wrong option !!!!!!!!! ")


menu()