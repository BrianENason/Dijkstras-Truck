"""
Brian Nason
Student Number: xxxxxxx
"""

"""
This will create a HashTable with Chaining to handle collisions.

Since parcel id's will be used as the key AND they are in a base-10 numbering system, it is prudent (for now) to use
a length of 10.

NOTE: Future iterations MAY need to expand when handling 100's or even 1000's of parcels each day.

SUGGESTION: When the parcel numbers(p_id) hit the triple digits, it would be prudent to up the length by a factor of 10
for every added digit - ie. 3 digits (100-999) should be length 100, 4 digits (1000 - 9999) should be length 1000, etc.,
this way there are only about 10 or so collisions at most per bucket.

NOTE: If the parcel id numbering system is ever changed to a random assortment of digits, this table will have to be
reworked depending on the FLOWTHROUGH of the "company" (10 digit id's with only 500 parcels per day would not
be practical to hold in a HashTable of length 1,000,000,000 if the factor of 10 is observed)

Reference for code solution was found in the readings as well as the supplemental material videos posted on the course
website. The specific presentation/video that was of the most help in the creation of the hash table is:
    "C950 - Webinar-1 - Let's Go Hashing - Recording (30 min)"

O(n)
"""
class ChainingHashTable:
    def __init__(self, length=10):
        self.table = []
        for i in range(length):
            self.table.append([])

    """
    This will insert and/or update parcels in the hash table. One of two things will happen when this is called
    and a parcel ID(key) and a Parcel Object(p_item) is passed in:
    1) It will not find a matching key, so it will create a new parcel object inside the hash table in the appropriate
    list and in the appropriate bucket.
    2) it will update the parcel object that is already associated with the key with the new parcel object that is
    being passed in to it. Basically, it will delete the associated object and replace it with the new (updated) 
    parcel object.
    
    NOTE: In future iterations, the code for insert, search, and delete are almost similar and can be handled by a
    single function that is called to locate the key, then each of the three(insert, search, and delete) can do with
    the return whatever their intended job is.
    
    O(n)
    """
    def insert(self, key, p_item):
        # Finds the correct parcel bucket to place the p_item into
        p_bucket = hash(key) % len(self.table)
        p_bucket_list = self.table[p_bucket]

        # If key is already in bucket, the parcel value attached to that key will be updated
        # p_kv = 'parcel key value' - the key/value pair for the item we're updating
        for p_kv in p_bucket_list:
            if p_kv[0] == key:
                p_kv[1] = p_item
                return True

        # If the key is NOT already in the bucket, the p_item is then inserted to the end of the list
        p_key_value = [key, p_item]
        p_bucket_list.append(p_key_value)
        return True

    """
    This will search the Hash Table for a specific parcel, using the parcel ID passed into it when the function
    is called as the Parcel ID is the Key for the Chaining Hash Table.
    
    It first retrieves the p_bucket_list where the parcel should be kept based on the 9key mod len(10 in this case))]
    Next it takes a copy of the list INSIDE the bucket the parcel is supposed to be in and assigns it to a variable.
    It will iterate through the list, look for the matching key, and return the value(parcel object) associated with 
    that key for the calling function to do stuff with.
    
    NOTE: If no matching key is found, None is returned. The calling function will handle a None return and display
    the appropriate error message to the user.
    
    O(n)
    """
    def search(self, key):
        # Retrieve the p_bucket_list where the parcel should be by key value MOD 10(table length).
        p_bucket = hash(key) % len(self.table)
        p_bucket_list = self.table[p_bucket]

        # Once p_bucket_list has been found, we search it for the matching key.
        for p_kv in p_bucket_list:
            # For when key is found, its value (the parcel's data) is returned
            if p_kv[0] == key:
                value = p_kv[1]
                return value
        # When key is not found, None is returned.
        return None

    """
    Used to remove a parcel from the hash table based on the parcels id number (p_id) as the key.
    
    It first retrieves the bucket that the parcel is supposed to be in based on the [key mod len(10 in this case)].
    Next it takes a copy of the list INSIDE the bucket the parcel is supposed to be in and assigns it to a variable.
    It finally iterates through the list, looking for the matching key, returning and removing the correct parcel.
    
    NOTE: This is not really used in the simulation and is more for future iterations of the program. Can be used
    for functions such as clearing a day, etc.
    
    O(n)
    """
    def remove(self, key):
        # Retrieve the p_bucket_list where the parcel should be by key value MOD 10(table length).
        p_bucket = hash(key) % len(self.table)
        p_bucket_list = self.table[p_bucket]

        # If parcel is found, its key and value will be removed from the table.
        # If parcel is NOT found, None will be returned.
        for p_kv in p_bucket_list:
            if p_kv[0] == key:
                p_bucket_list.remove([p_kv[0], p_kv[1]])
        # If key is not found, None is returned.
        return None

    """
    Creates a more user-friendly way of viewing the table - tells the user what "bucket" the parcel is being held in
    as well as the details of the parcels inside that bucket.
    
    NOTE: This is more for debug than anything, but is included as it CAN be useful in future iterations to look at
    what parcels are needed to be delivered.
    
    O(n)
    """
    def display_table(self):
        for i in range(len(self.table)):
            print("Parcel Bucket Number:", i)
            for j in self.table[i]:
                print(j)
            print()
