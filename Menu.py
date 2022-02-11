"""
Brian Nason
Student Number: 1003011

This class controls the user menu.
It is modular and full expandable/adaptable.
"""

import Truck
import sys
import Parcel


"""
Main Menu is the first call from the main program for the user interface.

As this is a simulation, the menu appears to the user AFTER the simulation has been run.
For future releases, it would be prudent to call for the main menu at the program's initialization so that the
user can follow the trucks and parcels in real time.

O(1)
"""
def main_menu():
    answer = True
    while answer:
        print("""
        WGU Parcel Service Main Menu...    
        \tFor Truck Menu, type \'t\'
        \tFor Parcel Menu, type \'p\'
        \tTo quit, type \'q\'         
        """)
        answer = input("Please enter your selection: ")
        if answer.lower() == "t":
            truck_menu()
        elif answer.lower() == "p":
            parcel_menu()
        elif answer.lower() == "q":
            sys.exit("End Program")
        else:
            print("Invalid Selection!")


"""
parcel_menu holds all the view/modifies to the parcels that the user can do.
Here the user can look up either the status of ONE parcel or ALL parcels at a given time.
It contains a sub-menu for the specific lookups as requested in requirement F in the rubric.
Finally, it allows the user to go back to the main menu, or exit the program directly.

In future releases, this should gain the ability to allow users to add/delete/update parcels.

O(1)
"""
def parcel_menu():
    answer = True
    while answer:
        print("""
        Parcel Menu...
        \tFor status of A Parcel, type \'1\'
        \tFor status of ALL parcels, type \'2\'
        \tTo search for a parcel, type \'3\'
        \tTo go back to the main menu, type \'4\'
        \tTo quit program, type \'Q\'
        """)
        answer = input("Please enter your selection: ")
        if answer == "1":
            p_id = input("What is the Parcel ID you are looking up? ")
            user_time = input("What time are you looking at?(format as 00:00) ")
            time = time_check(user_time)
            if time == "Invalid Time Entered":
                print('Invalid Time Entered')
                continue
            a_parcel_status(p_id, time)
            input('Press enter to continue...')
            continue
        elif answer == "2":
            user_time = input("What time are you looking at?(format as 00:00) ")
            time = time_check(user_time)
            if time == "Invalid Time Entered":
                print('Invalid Time Entered')
                continue
            all_parcels_status(time)
            input('Press enter to continue...')
            continue
        elif answer == "3":
            parcel_lookup_menu()
        elif answer == "4":
            answer = False
        elif answer.lower() == "q":
            sys.exit("End Program")
        else:
            print("Invalid Selection!")


"""
truck_menu holds all the views that the user can do to the fleet of vehicles.
It also allows the user to go back to the main menu or exit the program.

The first 2 menu options are for real-time inquiries and, since this is a simulation, they are not needed. 
They are simply here as placeholders for future releases and most of their code is commented out.

O(1)
"""
def truck_menu():
    answer = True
    while answer:
        print("""
        Truck Menu...
        \tFor status of A truck, type \'1\'
        \tFor status of ALL trucks, type \'2\'
        \tFor TOTAL miles driven by A truck, type \'3\'
        \tFor total miles driven by ALL trucks, type \'4\'
        \tTo go back to the main menu, type \'5\'
        \tTo quit program, type \'Q\'
        """)
        answer = input("Please enter your selection: ")
        if answer == "1":
            # t_id = input("What is the Truck ID you are looking up? ")
            # time = input("What time are you looking at?(format as 00:00) ")
            print("Great menu option for future releases, but since this is a simulation, it is not needed")
            input('Press enter to continue...')
            continue
        elif answer == "2":
            # time = input("What time are you looking at?(format as 00:00) ")
            print("Great menu option for future releases, but since this is a simulation, it is not needed")
            input('Press enter to continue...')
            continue
        elif answer == "3":
            t_id = input("What is the Truck ID you are looking up? ")
            one_truck_miles(t_id)
            input('Press enter to continue...')
            continue
        elif answer == "4":
            all_truck_miles()
            input('Press enter to continue...')
            continue
        elif answer == "5":
            answer = False
        elif answer.lower() == "q":
            sys.exit("End Program")
        else:
            print("Invalid Selection!")


"""
This is a separate menu that will pop up from the parcel menu if the user wishes to look up parcels by attributes.
Attributes include: ID, Address, Deadline, City, Zipcode, Weight, and Status.
User can also use this menu to go back to the Parcel Menu, to the main menu, or exit the program entirely.

O(1)
"""
def parcel_lookup_menu():
    answer = True
    while answer:
        print("""
        Parcel Lookup Menu...
        \tTo search parcel by ID, type \'1\'
        \tTo search parcel by Address, type \'2\'
        \tTo search parcel by Deadline, type \'3\'
        \tTo search parcel by City, type \'4\'
        \tTo search parcel by Zipcode, type \'5\'
        \tTo search parcel by Weight, type \'6\'
        \tTo search parcel by status, type \'7\'
        \tTo go back to the parcel menu, type \'8\'
        \tTo go back to the main menu, type \'9\'
        \tTo quit program, type \'Q\'
        """)
        answer = input("Please enter your selection: ")
        if answer == "1":
            print("Lookup by parcel ID")
            p_id = input("Please enter a Parcel ID Number:")
            print(Parcel.p_hash_table.search(int(p_id)))  # p_id is stored as an int, so conversion from string happens
            input("\nPress Enter to continue...")  # Allows user to view info before menu appears again in the UI
            continue
        elif answer == "2":
            print("Lookup by parcel Address")
            user_address = input("Please enter address: ")
            parcel_search(user_address, 1)
            input("\nPress Enter to continue...")  # Allows user to view info before menu appears again in the UI
            continue
        elif answer == "3":
            print("Lookup by parcel Deadline")
            user_deadline = input("Please enter deadline (format hh:mm): ")
            if user_deadline.isalpha():
                print("Invalid Time Entered")
                input("\nPress Enter to continue...")  # Allows user to view info before menu appears again in the UI
                continue

            # This next code is needed as the time from the provided parcel form is in the format "hh:mm am"
            ampm = input("Press 1 for am, press 2 for pm, or 3 for neither: ")
            if ampm == '1':
                user_deadline = user_deadline + ' AM'
            if ampm == '2':
                user_deadline = user_deadline + ' PM'
            if ampm == '3':
                user_deadline = 'EOD'
            print('The time you are looking at is', user_deadline)
            parcel_search(user_deadline, 2)
            input("\nPress Enter to continue...")  # Allows user to view info before menu appears again in the UI
            continue
        elif answer == "4":
            print("Lookup by parcel City")
            user_city = input("Please enter city: ")
            parcel_search(user_city, 3)
            input("\nPress Enter to continue...")  # Allows user to view info before menu appears again in the UI
            continue
        elif answer == "5":
            print("Lookup by parcel Zipcode")
            user_zipcode = input("Please enter zipcode: ")
            parcel_search(user_zipcode, 4)
            input("\nPress Enter to continue...")  # Allows user to view info before menu appears again in the UI
            continue
        elif answer == "6":
            print("Lookup by parcel Weight")
            user_weight = input("Please enter weight (in kg): ")
            parcel_search(user_weight, 5)
            input("\nPress Enter to continue...")  # Allows user to view info before menu appears again in the UI
            continue
        elif answer == "7":
            print("Lookup by parcel Status")
            user_status = input("Please enter status (at hub, en rout, or delivered): ")
            parcel_search(user_status, 6)
            input("\nPress Enter to continue...")  # Allows user to view info before menu appears again in the UI
            continue
        elif answer == "8":
            answer = False
        elif answer == "9":
            answer = False
            main_menu()
        elif answer.lower() == "q":
            sys.exit("End Program")
        else:
            print("Invalid Selection!")
            continue


"""
This method is for looking up the "status" of a parcel at a user-specified time.
It will take in a parcel id and a user-specified time as an argument.
It first compares user time to delivered time. If user time is before delivered time, then parcel is delivered.
If user time is AFTER delivered time, then user time is compared to parcel's load time.
If user time is AFTER load time, then parcel is En Rout.
Finally, if user time is BEFORE load time, the status that is set when the parcel object is created is returned which
could be either delayed or at hub.

O(n)
"""
def a_parcel_status(parcel_id, time):
    print("At ", time, " parcel ", parcel_id, " is...", end='\n')
    value = Parcel.p_hash_table.search(int(parcel_id))
    if value.p_deliver_time <= time:
        print("\tDelivered (delivered at:", value.p_deliver_time, ") - loaded onto truck",
              value.p_truck_number, "at:", value.p_load_time)
        return
    if value.p_deliver_time > time > value.p_load_time:
        print(" \tOn Truck", value.p_truck_number, " (loaded at:", value.p_load_time, ')')
        return
    else:
        print(value.p_status)
        return


"""
This method is for looking up the "status" of ALL parcels at a specified time.
It loops through the parcel hash table, sending each parcel object along with the user time through the a_parcel_status 
method above to do the time comparison. It relies on the return from the a_parcel_status method.

O(n)
"""
def all_parcels_status(time):
    i = 40
    while i > 0:
        var1 = Parcel.p_hash_table.search(i)
        var2 = var1.p_id
        a_parcel_status(var2, time)
        i -= 1
    return


"""
This method will take in the user search inquiry from the menu above.
It will use "parameter" to decide what type of search the user wishes to perform with this data.
It will then search the parcel table to pull each parcel object, check its parameter against the search parameter,
and then add it to a dict if it is a match.
Finally, it will display the dict to the user by ID number.

To expand in future releases, you could have this return the objects themselves if all the data they contain is needed.
Also, to expand, the output formatting should be re-worked to make it clearer to the user what the search results are.
Finally, to expand, add checks to the user input to make sure it will match the specific formatting of the inquiry.

O(n)
"""
def parcel_search(user_input, parameter):
    i = 40
    j = {}
    while i > 0:
        var1 = Parcel.p_hash_table.search(i)
        if parameter == 1:
            if user_input.lower() in var1.p_address.lower():
                j[var1.p_id] = var1.p_address
            i -= 1
        elif parameter == 2:
            if var1.p_deadline == user_input:
                j[var1.p_id] = var1.p_deadline
            i -= 1
        elif parameter == 3:
            if user_input.lower() in var1.p_city.lower():
                j[var1.p_id] = var1.p_city
            i -= 1
        elif parameter == 4:
            if var1.p_zip == int(user_input):
                j[var1.p_id] = var1.p_zip
            i -= 1
        elif parameter == 5:
            if var1.p_weight == int(user_input):
                j[var1.p_id] = var1.p_weight
            i -= 1
        elif parameter == 6:
            if var1.p_status.lower() == user_input.lower():
                j[var1.p_id] = var1.p_status
            i -= 1

    print("Parcels matching \"", user_input, "\" are...")
    if len(j) == 0:
        print("No results found")
        return
    else:
        for x in j.keys():
            print(x, end=' | ')
        return


"""
This method is for looking up the "status" of A truck at a specified time.
It will take in a truck id and a user time as an argument and return the mileage and its associated parcels including
their statuses ("On Rout", "Delivered").

Since this program is a simulation and not a "real time", the function is not needed. It is here as a placeholder.
 
O(1)
"""
def a_truck_status(t_id, time):
    print("At ", time, " truck ", t_id, " is...")


"""
This method is for looking up the "status" of ALL truck at a specified time.
It will take in a user time as an argument and return the TOTAL mileage of ALL trucks and 
their associated parcels including their statuses ("On Rout", "Delivered").

Since this program is a simulation and not a "real time", the function is not needed. It is here as a placeholder.

O(1)
"""
def all_trucks_status(time):
    print("The status of ALL trucks at ", time, " is...")


"""
This method is for looking up the total miles driven by a SINGLE truck at the end of the day.
It will take a truck ID as the argument and send it to the "Fleet" class that holds all the trucks that are created.

The Fleet class will perform the search and return a truck object if it finds a matching truck.

The function will decide if there is any return, and if so, it will display the odometer reading for the matching truck,
otherwise it will let the user know that the truck was not found.

O(1)
"""
def one_truck_miles(t_id):
    t_search = Truck.truck_fleet.search_truck(t_id)
    if t_search:
        print('\n\t', 'Truck', t_id, 'traveled', round(t_search.t_odometer, 2), 'miles\n')
    else:
        print('\n\tTruck not found\n')


"""
This method is for looking up the total miles driven by ALL trucks at the end of the day.

It sends the search inquiry to the "Fleet" class to handle the search, and uses the return list to calculate the
total mileage of ALL trucks.

As it returns the TOTAL miles driven by all truck in the day, it takes no arguments.

Since the trucks are stored in a "Fleet" dictionary, it is fully expandable. It will take all the odometer readings
from all trucks in the "Fleet", add them together, and display them to the user.

O(1)
"""
def all_truck_miles():
    t_search = Truck.truck_fleet.get_all_trucks()
    miles = 0  # Place Holder for the total odometer reading
    for i in t_search:
        miles += round(i.t_odometer, 2)  # round to 2 decimals
    print('\n\tThe total mileage for all trucks is', miles, 'miles\n')



"""
This small function verifies that the user is entering a correct time to search in the correct format.
In future iterations of the program, it would be prudent to use the dateTime class in Python, but since
this is merely a simulation, it is not needed.

O(1)
"""
def time_check(time):
    for i in time:
        if i.isalpha():
            return "Invalid Time Entered"
    if len(time) > 5:
        return "Invalid Time Entered"
    if time[2] == ':':
        return time
    if len(time) < 5:
        if time[1] == ':':
            time = '0' + time
            return time
        else:
            return "Invalid Time Entered"
    return "Invalid Time Entered"
