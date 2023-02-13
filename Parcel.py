"""
Brian Nason
Student Number: xxxxxxx
"""

import csv
from ChainingHashTable import ChainingHashTable


'''
Initialize a p_hash_table to be used in the Parcel Class below
'''
p_hash_table = ChainingHashTable()


"""
The Parcel Class below contains variables for all the attributes of a "parcel" object.

In addition to the attributes parsed from the .csv file, it adds 4 attributes:
    1) p_status is used to hold the status of a parcel at creation - could be "At Hub" or "Not Arrived"(if delayed)
    2) p_load_time is used to hold the time value for when the parcel is loaded onto a truck
    3) p_deliver_time is used to hold the time value for when the parcel is delivered to its address.
    4) p_truck_number is used to hold the truck number that the parcel is loaded onto.
    *NOTE: 2 and 3 are initialized to 00:00 at the object's creation, but will change throughout the simulation

NOTE: In future releases, this class should utilize the time function in Python so that real-time changes/updates can be
made, but since this is a simulation and all deliveries happen almost instantly, it is not needed.

NOTE: Also in future releases, the "weight" of a parcel should/could be a consideration in the loading of trucks as
weight can effect both the gas mileage AND the capacity of a delivery. Since it is not a concern in this simulation, 
it is merely here as a curiosity.
"""
class Parcel:
    def __init__(self, p_id, address, city, state, p_zip, deadline, weight,
                 notes):
        self.p_id = p_id  # Given by .csv file. In future, should be auto gen. for expandability
        self.p_address = address  # physical street address only
        self.p_city = city
        self.p_state = state  # will always be WA in this simulation, but has ability to hold any state sent into it
        self.p_zip = int(p_zip)  # zip is an int since it is always a number
        self.p_deadline = deadline  # stored as a string, since realtime updates aren't required for simulation
        self.p_weight = int(weight)  # weight is rounded to the nearest whole kg
        self.p_notes = notes

        """
        Status variable is to hold the status of the parcel (At Hub, Not Arrived, On Truck, Delivered).
        Default status is set to "At Hub".
        
        If .csv file's special notes indicate the parcel's delayed, status is initialized to "Not Arrived"
        
        When the parcel is delivered, the status is set to "Delivered".
        """
        self.p_status = 'At Hub'
        if 'Delayed' in self.p_notes:
            self.p_status = 'Not Arrived'

        """
        2 time variables to hold the time the parcel is loaded on a truck and when it is delivered.
        
        NOTE: Since its a simulation, string data type is fine, but if project was to run in real time, Python 
        dateTime type should be used.
        """
        self.p_load_time = '00:00'
        self.p_deliver_time = '00:00'

        """
        Variable to hold what truck the parcel is loaded onto. Good for the simulation to recall information of the
        parcel, but also good for future releases as there will be many more trucks in the fleet and it is useful
        to know what truck the parcel will be/is/was loaded onto.
        """
        self.p_truck_number = 0  # will be updated when the parcel object is loaded onto a truck

    """
    Overwrites the general class display to display the parcel object in a more user-friendly way.
    
    Provides 2 views -
    1) If there is NOT any special notes in the parcel object, then it displays "None" for the special note line
    2) If there IS any special notes in the parcel object, then it displays the note for the user in line.
    
    O(1)
    """
    def __repr__(self):
        # No special notes
        if self.p_notes == '':
            print("\n - Parcel Number: " + self.p_id)
            return "\t-> Parcel is going to: %s %s, %s %s \n\t-> Weight(in kg): %s " \
                   "\n\t-> Due by: %s.\n\t-> Special Notes: None\n\t-> Status: %s" \
                   "\n\t-> Load Time: %s\n\t-> Deliver Time: %s" % (
                       self.p_address, self.p_city, self.p_state, self.p_zip, self.p_weight, self.p_deadline,
                       self.p_status, self.p_load_time, self.p_deliver_time)
        # Has special notes
        else:
            print("\n - Parcel Number: " + self.p_id)
            return "\t-> Parcel is going to: %s %s, %s %s \n\t-> Weight(in kg): %s " \
                   "\n\t-> Due by: %s.\n\t-> Special Notes: %s\n\t-> Status: %s" \
                   "\n\t-> Load Time: %s\n\t-> Deliver Time: %s" % (
                       self.p_address, self.p_city, self.p_state, self.p_zip, self.p_weight, self.p_deadline,
                       self.p_notes, self.p_status, self.p_load_time, self.p_deliver_time)


"""
This will parse the parcel data from the provided .csv file and create parcel objects from the information it contains.
It will then send each parcel object into the p_hash_table for storage, using the p_id as the key.

NOTE: For the key, p_id is converted to an int data type so that the parcel object can be inserted into the correct
bucket in the hash table. 

O(n)
"""
def parse_parcel_list():
    with open('WGUPS Package File.csv') as parcels:
        parcel_file = csv.reader(parcels, delimiter=',')

        # next will be called 2X to bypass the header in the .csv file.
        next(parcel_file)
        next(parcel_file)

        """
        This will take the .csv file line-by-line, extract the parcel's attributes from the appropriate columns, and
        use that information to create a parcel object and a p_id key. It will use that key/object pair to
        insert the parcel into the proper place in the p_hash_table.
        
        NOTE: as there is no range, this function is fully expandable for any-sized parcel file. ie, you can send
        through a parcel file that contains 1 or 1,000 + parcels, and it can handle it.
        
        O(n)
        """
        for parcel in parcel_file:
            parcel_id = int(parcel[0])
            parcel = Parcel(parcel[0], parcel[1], parcel[2], parcel[3], parcel[4], parcel[5], parcel[6], parcel[7])
            p_hash_table.insert(parcel_id, parcel)


"""
This will manually load the trucks with the parcels. Depending on their "load", they will be loaded with a tuple of 
parcel id numbers.
Each time the function is called, it will require the truck number(t_num) and the load number(l_num).

This will be for the simulation. In future iterations, manual loading of the trucks should not be done. The loading
should be done by something like the greedy algorithm that takes things like weight into account as a truck full
of 16 5lb parcels will get much better travel/mileage than a truck of 16 50lb parcels.

The special notes are related to the specific quirks that the rubric outlined. 

O(1)
"""
def truck_parcel_list(t_num, l_num):
    if t_num == 1:
        if l_num == 1:
            # Parcels have to be delivered together (same truck) are 13, 14, 15, 16, 19, 20
            # Parcel 15 HAS to be one of the first delivered as it MUST be delivered by 9:00am
            self_load = [15, 16, 34, 14, 20, 21, 19, 4, 40, 1, 13, 39, 27, 35]  # 14 Parcels
            return self_load
        if l_num == 2:
            # Number 9 has wrong address and CAN'T be delivered until after 10:20
            self_load = [2, 33, 17, 8, 9]  # 5 Parcels
            return self_load
    elif t_num == 2:
        # Parcels HAVE to be on truck 2 include 3 (load 1), 18 (load 3), 36 (load 2), 38 (load 1)
        if l_num == 1:
            self_load = [3, 30, 5, 37, 38, 10, 7, 29]  # 8 Parcels
            return self_load
        if l_num == 2:
            # Parcels that are delayed on flight and won't be at hub until 9:05. Parcels 6, 25, 28, 32
            self_load = [25, 26, 31, 32, 6, 36, 28]  # 7 Parcels
            return self_load
        if l_num == 3:
            self_load = [11, 12, 18, 22, 23, 24]  # 6 Parcels
            return self_load
    else:
        print('Truck number: ', t_num, 'does not exist')

