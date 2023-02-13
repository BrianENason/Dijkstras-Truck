"""
Brian Nason
Student Number: xxxxxxx
"""

from math import ceil
from DeliveryMap import utah_map
from Parcel import truck_parcel_list
import Parcel

"""
This class creates a Truck object to hold pertinent information.
Speed and Capacity are initialized to the project's specifications.
It includes truck-specific functions of rout, load (load being the parcels it's carrying), and record (all the parcels
it has delivered from start of day to delivery completion).

NOTE: The project allows for 3 trucks, but since it only allows 2 drivers, there is no need for truck 3, so
only 2 truck objects are created for the simulation
"""
class Truck:
    def __init__(self, location, truck_number, speed=18, capacity=16):
        self.t_number = truck_number
        self.t_time = '00:00'
        self.t_speed = speed
        self.t_odometer = 0
        self.t_parcels = []
        self.t_location = location
        self.t_parcels_record = []

        """
        This initializes the t_parcels list with the max capacity of parcels it can contain.
        The project outline dictates capacity is 16, but this provides the ability to expand/reduce capacity
        depending on future requirements.
        """
        for i in range(capacity):
            self.t_parcels.append(None)

    """
    t_rout will take the rout that Dijkstra's Algorithm decides and apply it to the Truck. In the code, 3 things happen:
        1) The rout will progress location by location, updating the time and mileage of the truck as it goes
        2) It will update the parcel's delivery time as it "delivers" the parcel based on the updated truck time
        3) When it finishes a "delivery", it will look to the next location until no location remains in the rout
        
    Future versions should use the timedate type to update truck time and parcel times in real time, 
    but since this is a simulation, the extra computing power is not needed, so it is left as a string value.
    
    O(n)
    """
    def t_rout(self, t_map, rout):
        t_hour = int(self.t_time[0:2])
        t_minute = int(self.t_time[-2:])

        """
        O(n)
        """
        for t_address in range(len(rout) - 1):  # O(n)
            miles = t_map.miles[(rout[t_address], rout[t_address + 1])]
            self.t_odometer += miles

            # Truck time is calculated by a steady 18mph (t_speed variable).
            t_minute += ceil(miles / (self.t_speed / 60))
            t_hour += t_minute // 60
            t_minute = t_minute % 60

            """
            Once truck time is calculated:,  
                1) the parcels are removed from the truck
                2) their deliver time is updated based on the truck's time at the point of delivery
                3) their status is updated to "Delivered" 
            
            O(n)
            """
            for i, parcel in enumerate(self.t_parcels):  # O(n)

                if parcel is not None and parcel.p_address == rout[t_address + 1].address:
                    p_time = str(t_hour).zfill(2) + ':' + str(t_minute).zfill(2)
                    parcel.p_deliver_time = p_time

                    """
                    The below line is commented out for the simulation, but if this is run in real time, it 
                    would need to be included.
                    """
                    # parcel.p_status = 'Delivered'
                    
                    # NOTE: This printout below is for the simulation's sake and for the sake of proof of simulation
                    # completion. It will not be needed in future iterations of the program.
                    print("\tParcel: ", parcel.p_id, "Del Time: ", parcel.p_deliver_time)

                    # The index of the parcel delivered is updated from the parcel object to "None"
                    self.t_parcels[i] = None

        self.t_location = rout[-1]  # O(1)
        self.t_time = str(t_hour).zfill(2) + ':' + str(t_minute).zfill(2)  # O(1)

    """
    This takes in the list of parcel ids to be loaded onto a truck, looks up the parcels one-by-one in the HashTable,
    pulls the Parcel Object from that table, and adds it to the truck's parcel load for delivery.
    
    It also adds the parcels into a separate list - t_parcels_record - to keep a running record of ALL parcels
    that went onto the truck that day, since the parcels in the t_parcel list are removed each time they are delivered.
    
    In future iterations, it would be prudent to record the parcel AFTER the delivery takes place for real-time
    feedback, but in the simulation that is not needed, so the record is updated at load.
    
    O(n)
    """
    def truck_loader(self, parcel_list):
        # Parcel list is likely to be filled with None values, so those must be cleared before the list is filled again
        self.t_parcels.clear()

        for p, i in enumerate(parcel_list):
            new_parcel = Parcel.p_hash_table.search(i)
            new_parcel.p_load_time = self.t_time
            new_parcel.p_truck_number = self.t_number
            self.t_parcels.append(new_parcel)
            self.t_parcels_record.append(new_parcel)


"""
The Fleet class below is to hold the Trucks that are "run" during the simulation so that their information can be
accessed later in the program. Has 3 basic functions for ease of use:
    1) insert_truck - this will add a truck to the fleet dict.
    2) search_truck - this will allow the functions accessing the truck-specific data to pull the correct truck based
    on the truck number
    3) get_all_trucks - this will return a list of all the trucks that are a part of the fleet.
"""
class Fleet:
    def __init__(self):
        self.fleet = {}  # Truck records are kept in a dict with number being the key and the truck object as the value

    """
    A truck object is passed into this function. The truck's number is recorded for the "key" in the dict, the truck
    object is recorded as the value in the dict. 
    
    O(1)
    """
    def insert_truck(self, truck):
        self.fleet[truck.t_number] = truck

    """
    This will search the "fleet" dict for a truck object based on a passed-in truck id (t_id).
    
    In future iterations, it might be prudent to add some checks to make sure the program isn't crashed by
    incorrect data being passed in.
    
    O(n)
    """
    def search_truck(self, t_id):
        t_search = int(t_id)
        if t_search in self.fleet:
            t_result = self.fleet.get(t_search)
            return t_result

    """
    This will pull all the truck objects from the "fleet" and return them in a list to be used in whatever function
    called it.
    
    O(n)
    """
    def get_all_trucks(self):
        result = []
        for t in self.fleet:
            t_result = self.fleet.get(t)
            result.append(t_result)
        return result


"""
This will "run" the truck. 
It takes a truck object as an argument, looks at that truck's parcel list, and then performs the following comparisons:
    1) Sees if the "Parcel" is set to "None" ie, the truck is empty. If it isn't, then it sets the variable 
    parcel_address to the address of the parcel we are working with from the list.
    2) It then looks at the addresses in the map that is created for this simulation, specifically targeting the keys
    of the "neighbors" dict. Since any address can be a neighbor to any other, this list contains ALL possible
    address combinations
    3) It compares the parcel's address to the keys in "neighbor".
    4) It passes the truck's location and the parcel's address to the routing function, returning Dijkstra's ideal
    rout.
    5) Finally, it passes the rout and the map into the t_routing program to run that portion of the simulation
    
O(n^2)
"""
def run_truck(truck):
    while truck.t_parcels.count(None) < len(truck.t_parcels):
        next_address = None
        parcel_address = None

        for parcel in truck.t_parcels:
            if parcel is not None:
                parcel_address = parcel.p_address
                break

        for t_address in utah_map.neighbors.keys():
            if t_address.address == parcel_address:
                next_address = t_address
                break

        truck.t_rout(utah_map, utah_map.find_rout(truck.t_location, next_address))


"""
Since the Trucks have to return to the hub to re-load, the mileage for that trip must be taken into account. 
This function does this.

O(1)
"""
def return_to_hub(truck):
    truck.t_rout(utah_map, utah_map.rout_to_hub(truck.t_location))


"""
Formatting function to create a uniform break between simulation parts

O(1)
"""
def line_break():
    print('\n---------------------------------------\n')


"""
Formatting function to create a uniform output of information as each delivery rout is completed.

O(1)
"""
def truck_run_result(truck):
    print('\nTruck', truck.t_number, 'time is: ', truck.t_time)
    print('Truck', truck.t_number, 'Total Miles: ', round(truck.t_odometer, 2), 'miles')


"""
The variable truck_fleet is initialized as a "Fleet" class object. It will contain the truck's that are "run" in the
simulation for ease of information access "after the fact".
"""
truck_fleet = Fleet()

"""
This is the actual simulation. When called, it will "run" the day.
There are 3 assumptions at play here based on the requirements:
    1) There are 3 trucks, but only 2 drivers
    2) A driver would have to return to the hub to get the third truck
    3) There is no "load time" for any of the trucks, so the same truck can return to the hub and leave with a new 
    load instantly
Because of these assumptions, there is only need for 2 trucks to be taken into account, as long as the "load" 
count is tracked.

Each Truck is initialized with their location being the hub, their truck number (1 or 2), and their time set to 08:00am

Each truck is then added to the "Fleet" class to save its record for information pulls by the user.

The two trucks are then sent a list of packages based on the argument of truck number and load number.

Both trucks are then run, their time and odometers being incremented as deliveries happen while their parcel lists gets
decremented each time a delivery is made. When their parcel list is 0, they are instructed to return to the hub (adding
the travel time/distance necessary) and then they are loaded with their second loads.

When first_truck finishes its 2nd load. it is left at the last address and its totals are sent to the report.
When second_truck finishes its 3rd load, it is left at the last address and its totals are sent to the report.

NOTE: Only second_truck needs a 3rd load.

O(1) 
"""
def initialize_truck():
    first_truck = Truck(utah_map.hub, 1)
    first_truck.t_time = '08:00'
    truck_fleet.insert_truck(first_truck)

    second_truck = Truck(utah_map.hub, 2)
    second_truck.t_time = '08:00'
    truck_fleet.insert_truck(second_truck)

    """
    In the requirements, it is mentioned that parcel 9 has the wrong address. This will search for parcel 9 in the 
    hash table, and then update it's address with the correct information. 
    
    In the loading of the trucks, parcel 9 is then delegated to first_truck, second load so then it will not be
    delivered until after 10:20 and ends up being delivered at 10:23.
    
    O(1) 
    """
    wrong_addy = Parcel.p_hash_table.search(9)
    if wrong_addy is not None:
        wrong_addy.p_address = '410 S State St'
        wrong_addy.p_zip = '84111'

    """
    The truck loader uses the truck number and the load number, sends it through to the Parcel class to pull
    the correct load list, assign that list as the truck's parcel list, and then sends that list into the 
    truck_loader function.
    
    O(1)
    """
    first_truck.truck_loader(truck_parcel_list(1, 1))
    second_truck.truck_loader(truck_parcel_list(2, 1))

    """
    Now we "run" each truck, then return them to the "hub" for the next loads. To track the "simulation", truck and 
    parcel information is printed to the console. 
    """
    print('First Truck, first load:\n')
    run_truck(first_truck)
    return_to_hub(first_truck)
    truck_run_result(first_truck)
    line_break()
    print('Second Truck, first load:\n')
    run_truck(second_truck)
    return_to_hub(second_truck)
    truck_run_result(second_truck)
    line_break()

    """
    Load and Run each truck a second time.

    Note: second_truck's time is manually overridden to 09:10 to account for the parcels that are not arriving to
    the hub until 09:05.
    """
    first_truck.truck_loader(truck_parcel_list(1, 2))
    second_truck.t_time = '09:10'
    second_truck.truck_loader(truck_parcel_list(2, 2))

    print('First Truck, second load:\n')
    run_truck(first_truck)
    truck_run_result(first_truck)  # Note: truck is left at last delivery since the Hub doesn't have a 3rd load for it
    line_break()
    print('Second Truck, second load:\n')
    run_truck(second_truck)
    return_to_hub(second_truck)
    truck_run_result(second_truck)
    line_break()

    """
    # Only Truck 2 needs a 3rd load
    """
    second_truck.truck_loader(truck_parcel_list(2, 3))
    print('Second Truck, third load:\n')
    run_truck(second_truck)
    truck_run_result(second_truck)  # NOTE: There is no more loads for the truck, so it is left at last address
    line_break()

    """
    Once the simulation is completed, the targeted information is presented.
    Total miles between all trucks and all loads MUST be below 140 miles.
    """
    print('Total Truck Miles: ', (round(first_truck.t_odometer + second_truck.t_odometer, 2)), 'miles')


