"""
Brian Nason
Student Number: 1003011
"""

import csv

"""
This class will create the properties of the Destination objects to use as the "vertex" portion of the graph(Map).
Each Destination has 3 properties: 
    1) The address - this is the actual point in the graph - where to go
    2) The travel distance to the next addresses - the "edge" on the map 
    3) The last address that was visited.
"""
class Destination:
    def __init__(self, address):
        self.address = address  # This is taken from the provided .csv file
        self.travel_distance = float('inf')  # Initialized to infinity until updated with the algorithm
        self.last_address = None

    """
    The below code was used for Debug, but is left in if the case is needed to display the actual "address" of
    the Destination object to the user in future iterations.
    """
    # def __repr__(self):
    #     print(self.address)


"""
This will create a Map object to direct the trucks from one location to another. 
Each location is a Destination object(address) and acts as the "vertex" for the map. 
Travel distance in miles is the "edge".
Map's components include: 
    1) .neighbors dictionary - to hold the addresses
    2) .miles dictionary - to hold the travel miles to each neighbor
    3) .hub - Hub will be the index 0 from the distance table.
     
NOTE: Requirements dictate that you can travel from any address to any other address in any order whatsoever, every
address is each other addresses "neighbor". Due to this, the .neighbors has to be able to contain all the addresses
available. Trucks will start at the hub, but from there, they can visit any address in any order.
"""
class Map:
    def __init__(self):
        self.neighbors = {}  # Neighboring destinations with key being their index position from the .csv file
        self.miles = {}
        self.hub = 'HUB'

    """
    This will add an address as the key in the "neighbors" dictionary and initialize its related value with nothing.
    Since the value is held in a separate source file from the key, it's insertion into the key will be done by a 
    separate function.
    
    NOTE: The key(address) is a Destination object
    
    O(1)
    """
    def add_address(self, new_address):
        self.neighbors[new_address] = []  # address is the key in the .neighbors dict

    """
    The provided .csv file contains the miles from any one address to any other address.
    2 addresses are passed in as well as the miles between them. 
    2 Dictionaries are updated simultaneously: 
        1) miles - which uses the start/end address combination as the key the travel miles between them as the value
        2) neighbors - It uses the start location as the key and the end location as the value. 
    
    O(1)    
    """
    def add_one_way_rout(self, start_location, end_location, mileage):
        self.miles[(start_location, end_location)] = mileage
        self.neighbors[start_location].append(end_location)

    """
    In this project, the distance from pointA to pointB is the same as the distance from pointB to pointA. 
    To ensure all combinations of points are added to the "neighbors" dictionary, the keys need to be both ways.
    
    This will simply call the "add_one_way_rout" function 2X - once for A to B and once for B to A.
    
    O(1)     
    """
    def add_two_way_rout(self, location_a, location_b, mileage):
        self.add_one_way_rout(location_a, location_b, mileage)
        self.add_one_way_rout(location_b, location_a, mileage)

    """
    This uses Dijkstra's algorithm to consider the best/shortest rout between deliveries. It returns a list that
    contains the "best" rout for each truck to take from one parcel delivery to the next.
    NOTE: This is only as good as the loading of the trucks is. It can only work with whatever parcels are loaded onto
    the trucks. For the most efficient routing possible, the trucks themselves need to be loaded in the most efficient
    way.
    
    Inspiration/guidance for the code below came from the readings as well as a large help from the videos posted in
    the course search webinars, most importantly the video titled:
        "C950-Webinar3 - How to Dijkstra - Recording (20 min)"
    
    NOTE: In future releases, it might be prudent to break the "find_rout" function into 2 parts:
        1) Find the shortest distances and return those
        2) Find the shortest path from a list of all "shortest distances" queued into a list
    This way it can be used separately if needed throughout the project like in conjunction with a "greedy" algorithm
    to load the trucks based on their distances.
    
    O(n(log n))

    """
    def find_rout(self, location_a, location_b):
        # Step 1: Create list to queue up all possible addresses
        address_queue = []

        # Step 2: Fill queue will all known addresses - from the provided .csv file
        for d_address in self.neighbors:  # O(n)
            address_queue.append(d_address)

        # Step 3: location_a is where the truck is starting from, so it's distance to itself is set to 0
        location_a.travel_distance = 0

        # Step 4: Visit all addresses and remove one per iteration until the queue is empty. This ensures that all
        # possible travel combinations are considered before making a decision.
        while len(address_queue) > 0:
            s_index = 0  # "smallest index" - Helps track the "smallest" distance from the start location

            # Step 5: This finds the "start" address in the queue because we set that distance to 0 (in step 3) whereas
            #         all other distances are set to inf. and 0 < inf.
            for i in range(1, len(address_queue)):  # range(start, stop)   O(log|n|)
                if address_queue[i].travel_distance < address_queue[s_index].travel_distance:
                    s_index = i

            # Step 6: once the index of the start location is found, it is popped from the queue and set to the variable
            #         "current_address"
            current_address = address_queue.pop(s_index)

            # Step 7: Look at all the potential mileages from the start(current_vertex) to all neighbors(n_addresses) in
            #         the "miles" dictionary where current_address is 1 part of the 2 part key and the value is "miles",
            #         and we swap in all n_addresses one-by-one as the 2nd part of the key to find the "smallest"
            for n_addresses in self.neighbors[current_address]:
                travel_distance_a = self.miles[(current_address, n_addresses)]
                travel_distance_b = current_address.travel_distance + travel_distance_a

                # Step 8: If shorter mileage is found from current_address to n_address, then its travel_distance is
                #         updated to the mileage we found in step 7 and its last_address variable is updated to the
                #         current_address
                if travel_distance_b < n_addresses.travel_distance:
                    n_addresses.travel_distance = travel_distance_b
                    n_addresses.last_address = current_address

        # Step 9: Create a list to hold the "best rout" that Djikstra's found
        best_rout = []

        # Step 10: Set the current address variable to the "end" address we know the next parcel has to go to. This was
        #          passed in at the calling of this function. This allows us to work backwards from the destination TO
        #          the start.
        current_address = location_b

        # Step 11: Starting at the destination, we go backwards through all possible address combinations until we find
        #          the start location (location_a). It adds each location to the FRONT of the best_rout list, and then
        #          sets the current_address variable to the next address in line (which, since we are working backwards,
        #          will be the last_address value). It repeatedly adds the locations to the front of the rout list
        #          until the start address is reached.
        while current_address is not location_a:
            best_rout.insert(0, current_address)
            current_address = current_address.last_address

        # Step 12: Now that the routing has been established, we add the start location to the front of the routing
        #          list (index 0) so when the best_rout list is read, it will read index 0 first, then 1, and so on.
        best_rout.insert(0, location_a)

        # Step 13: With the "best" rout discovered, we must reset all the variables in "neighbors" to their initial
        #          values to prep the "neighbors" dict for the next query.
        for address in self.neighbors:
            address.last_address = None
            address.travel_distance = float('inf')

        """
        This is for proof of Djikstra's working. It is not needed for the actual program unless it becomes necessary to
        display the rout.        
        """
        for i in best_rout:
            print(i.address)

        # Step 14: Finally, we return the rout to the calling function for it to use.
        return best_rout

    """
    This provides the opportunity for the truck to return to the hub from any address it is at.
    
    In the simulation:
        1) truck 1 has to return to the hub once to pick up another load
        2) truck 2 has to return to the hub TWICE to pick up more loads.
    
    Each time the truck has to pick up a new load (ie. when their truck is empty), time and mile calculation
    has to be taken into account. This function allows those calculations to happen from whatever address their 
    last parcel has them going to.
    
    NOTE: As in the requirements, the trucks DON'T have to return to the hub when they are empty UNLESS they
    have to pick up another load, so this function is separate from the rest of the mileage calculations so that
    when truck 1 is done with its 2nd load and truck 2 is done with its 3rd load, the mileage to return to the hub
    is not added to their odometer.
    
    O(1)
    """
    def rout_to_hub(self, start_location):
        return self.find_rout(start_location, self.hub)


"""
This creates an outside variable to hold the locations that are parsed from the provided .csv file. It will allow
easier association with the mileage between addresses in the parse_miles_file() function.
"""
locations = []

"""
This creates an instance of the Map class (the graph for the vertices and edges to be contained in) 
for this particular set of data to use in the simulation.

Since the data is related to Utah, it will be called utah_map.
"""
utah_map = Map()


"""
This function will parse the 'WGUPS Distance Table Addresses.csv' file to pull the provided addresses,
use that address to create a "Destination" object to be used as a vertex in the graph (Map).

NOTE: Each destination object takes the raw address as input in the creation.

NOTE: The original course-provided Excel file needed to be converted to .csv for parsing since without using outside
libraries, it is the easiest way to parse the data. HOWEVER, for ease of parsing and to get around some of the weird 
reads I was getting from the converted .csv file, I found it prudent to break it into 2 files - one with JUST the 
addresses, and the other with just the mileage between each address (the edges for the graph). Since none of the 
structure was edited, the indices for the address and the mile .csv files have parity.

In future iterations of this project, I would like to see a more standardized method for presenting the data
for ease of parsing.

O(n)
"""
def parse_address_file():
    with open('WGUPS Distance Table Addresses.csv', encoding='utf-8-sig') as delivery_locations:
        addresses = csv.reader(delivery_locations, delimiter=',')
        for i in addresses:

            """
            For unknown reasons, the addresses in the .csv file ALL have a blank space before their first character.
            For uniformity throughout the program, this whitespace as well as any other white space around the 
            addresses is stripped off BEFORE adding it to the map.
            """
            label = i[0].strip()

            """
             I added the below line to strip the encoding artifacts that were attached to the beginning of the .csv 
             file. Through internet research, I was able to avoid the symbol by declaring the encoding of the .csv 
             file itself.
             
             I have left it in if there is ever the case that the encoding is not declared correctly at any point
             through the creation of the program to remind me of the work-around I had.
            """
            # label = label.strip('ï»¿ ')

            """
            As the "reader" goes through each line in the .csv file, it will put that line's data (which is held
            in the "label" variable and will contain the raw address of that line) into a Destination object,
            temporarily assign that object to the "addy" variable, put that variable into the utah_map using its
            own add_address function, and then add that variable into the locations list as well.
            """
            addy = Destination(label)
            utah_map.add_address(addy)
            locations.append(addy)

        """
        Since the first address in the original excel file is the "HUB" where the parcels are loaded from, then
        the hub object will be at index 0 in the locations list.
        
        This picks that Destination object and assigns it to the utah_map as the value for the "hub" variable.
        
        This will allow all addresses to know how far from the hub they are so when the trucks need to reload, the
        distance can be added to their odometer without having to pull the "hub" address each time.
        
        O(1)
        """
        utah_map.hub = locations[0]


"""
This function will parse the 'WGUPS Distance Table Miles.csv' file to pull the mileage between any 2 addresses
and use that data as the "edges" in the "graph"(the utah_map variable).

NOTE: The original course-provided Excel file needed to be converted to .csv for parsing, since without using outside
libraries, it is the easiest way to parse the data. HOWEVER, for ease of parsing and to get around some of the weird 
reads I was getting from the converted .csv file, I found it prudent to break it into 2 files - one with JUST the 
addresses, and the other with just the mileage between each address (the edges for the graph). Since none of the 
structure was edited, the indices for the address and the mile .csv files have parity.

In future iterations of this project, I would like to see a more standardized method for presenting the data
for ease of parsing.

O(n^2)
"""
def parse_miles_file():
    with open('WGUPS Distance Table Miles.csv') as distance_file:
        miles = csv.reader(distance_file, delimiter=',')

        next(miles)  # Included to skip the header line

        """
        This first "for" loop will first take a look at each entry in each row from the miles file.
        Since the way the file was originally structured, the "row" in the miles file corresponds to a single
        address from the address file.
        
        The index(i) of each entry in the "row" equates to the "columns" of an excel file where each column is
        also associated with a single address. This creates a 2-D grid with addresses across the top and down
        one side, and their associated mileage filling in the spaces between them.
        
        O(n^2)
        """
        for i, row in enumerate(miles):

            """
            One-by-one, the first "for" loop will pull up a "row", and as each row is activated by the loop, the 
            program will then loop through the "locations" list as the index(l) of each location equates to the 
            index(i) of each mile.
            
            Once there is no more data in the row, it ignores the rest of the row. It puts 3 points of data into
            the bi-directional(add_two_way_rout) function of the graph. The data is:
                1) locations[i] - this is the index(i) from the above "for" loop that has index parity with the
                mileage in that specific index.
                2) locations[j] - This is the index(j) from the below enumeration. Together with the locations[i],
                it creates almost an (x, y) coordinate for the program to look at in the data file.
                3) row[j] - This is the raw mileage data that will be associated with the travel distance between the
                previous data points (the (x, y) coordinate created by data point 1(x) and 2(y))
                
            NOTE: The add_two_way_rout function will basically take locations[i] and locations[j], treat them like
            start and end points, put the mileage data as their edge, then swap them so the previous start is now the
            end and the previous end is now the start. This is done because we don't know which direction the truck
            needs to be going from and to and we have to have the options left open.
            
            O(n)
            """
            for j, location in enumerate(locations):
                if row[j] != '':
                    utah_map.add_two_way_rout(locations[i], locations[j], float(row[j]))



