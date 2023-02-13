"""
Brian Nason
Student Number: xxxxxxx
"""

import DeliveryMap
import Menu
import Parcel
import Truck

"""
This will parse the .csv files and create the chaining hash table and Delivery Map BEFORE the menu appears to the user.
"""
Parcel.parse_parcel_list()
DeliveryMap.parse_address_file()
DeliveryMap.parse_miles_file()

"""
Once all the .csv files have been parsed, the next code will initialize the trucks AND run the simulation.
"""
Truck.initialize_truck()

"""
Once the day is simulated, the User Menu appears and allows the user to make whatever inquiries they wish to do.
"""
Menu.main_menu()
