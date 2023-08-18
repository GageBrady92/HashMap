# Name: Daniel Brady
# OSU Email: bradyda@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 6
# Due Date: 6/9/2023
# Description: Implement open addressing hashmap with supporting methods

from a6_include import (DynamicArray, DynamicArrayException, HashEntry,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses
        quadratic probing for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(None)

        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def _next_prime(self, capacity: int) -> int:
        """
        Increment from given number to find the closest prime number
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity % 2 == 0:
            capacity += 1

        while not self._is_prime(capacity):
            capacity += 2

        return capacity

    @staticmethod
    def _is_prime(capacity: int) -> bool:
        """
        Determine if given integer is a prime number and return boolean
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity == 2 or capacity == 3:
            return True

        if capacity == 1 or capacity % 2 == 0:
            return False

        factor = 3
        while factor ** 2 <= capacity:
            if capacity % factor == 0:
                return False
            factor += 2

        return True

    def get_size(self) -> int:
        """
        Return size of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    # ------------------------------------------------------------------ #

    def put(self, key: str, value: object) -> None:
        """
        Method to update key/value pairs in hash map. Use open addressing to find correct location
        """
        # Resize if needed
        if self.table_load() >= 0.5:
            self.resize_table(self._capacity*2)
        # Set hash value and set additional for using quad probe. Set count for quad probe as well
        hash = self._hash_function(key) % self._capacity
        oa_key = hash
        count = 1
        # Check if empty, if so increment and add key/value
        if self._buckets[hash] is None:
            self._size += 1
            self._buckets.set_at_index(hash, HashEntry(key, value))

        else:
            # Loop while location in the hash map
            while self._buckets[hash]:
                #Check if location has key or tombstone, if so we need to update
                if self._buckets[hash].key == key or self._buckets[hash].is_tombstone is True:
                    # Check if tombstone, if it is, we can increment size. If key present, only need to replace
                    if self._buckets[hash].is_tombstone is True:
                        self._size += 1
                    # replace and update tombstone to false. Return to ensure size not incremented again
                    self._buckets.set_at_index(hash, HashEntry(key, value))
                    self._buckets[hash].is_tombstone = False
                    return
                # update hash with quad probe formula and increment count for next loop
                else:
                    hash = (oa_key + count ** 2) % self._capacity
                    count += 1

            self._buckets.set_at_index(hash, HashEntry(key, value))
            self._size += 1


    def table_load(self) -> float:
        """
        Method to return load factor for hash map
        """
        return self._size / self._capacity

    def empty_buckets(self) -> int:
        """
        Method to return the number of empty buckets for the hash map
        """
        empty = 0
        # Loop through hash map checking for none or tombstone and tally empty buckets
        for x in range(self._capacity):
            if self._buckets[x] is None or self._buckets[x].is_tombstone is True:
                empty += 1
        return empty

    def resize_table(self, new_capacity: int) -> None:
        """
        Method to resize the hash table based on value given.
        """
        if new_capacity < self._size:
            return

        # Check if new capacity is prime. If not, update with next_prime
        if self._is_prime(new_capacity) is False:
            new_capacity = self._next_prime(new_capacity)

        # new hash map with capacity
        new_hash = HashMap(new_capacity, self._hash_function)

        # Catch for 2 or it will increase to 3 after creating new hash map
        if new_capacity == 2:
            new_hash._capacity = 2
        # Loop through hash map and place keys from old hash map in new one
        for x in self:
            if x is not None:
                new_hash.put(x.key, x.value)

        # Update capacity, size and the new hash map that has been resized
        self._capacity = new_hash._capacity
        self._buckets = new_hash._buckets
        self._size = new_hash._size

    def get(self, key: str) -> object:
        """
        Method to check for key in hash map and return its value if found
        """
        # Loop through hash map and check if location is not none
        for x in self:
            if x is not None:
                # If key matches location and not a tombstone, return value
                if x.key == key and x.is_tombstone is False:
                    return x.value
        return None

    def contains_key(self, key: str) -> bool:
        """
        Method to return True if a key is in the hash map
        """
        # Use get to determine if key in hash map
        if self.get(key) is not None:
            return True
        return False

    def remove(self, key: str) -> None:
        """
        Method to search and remove key in the hash map
        """
        # Loop through hash map
        for x in self:
            # Check truth value of x and then check if key matches and tombstone is false. Change location to tombstone
            if x:
                if x.key == key and x.is_tombstone is False:
                    x.is_tombstone = True
                    self._size -= 1

    def clear(self) -> None:
        """
        Method to clear the hash map
        """
        self._buckets = DynamicArray()
        # Loop through hash map and for each location, append none and set size to 0
        for x in range(self._capacity):
            self._buckets.append(None)
        self._size = 0
            

    def get_keys_and_values(self) -> DynamicArray:
        """
        Method to return a dynamic array with key/value pairs
        """
        da = DynamicArray()
        # Loop through hash map and check for
        for x in self:
            # Check value is assigned in location and not tombstone. Add the key/value to the array
            if x and x.is_tombstone is False:
                da.append((x.key, x.value))
        return da

    def __iter__(self):
        """
        Method to allow iteration through the hash map
        """
        self.index = 0
        return self

    def __next__(self):
        """
        Method to return next item in hash map
        """
        # Set initial value to none and begin the loop
        # If value is None or is a tombstone, update value to current index and increment index to move to next spot
        try:
            value = None
            while value is None or value.is_tombstone is True:
                value = self._buckets[self.index]
                self.index += 1
        except DynamicArrayException:
            raise StopIteration

        return value


# ------------------- BASIC TESTING ---------------------------------------- #

if __name__ == "__main__":

    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(41, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(101, hash_function_1)
    print(round(m.table_load(), 2))
    m.put('key1', 10)
    print(round(m.table_load(), 2))
    m.put('key2', 20)
    print(round(m.table_load(), 2))
    m.put('key1', 30)
    print(round(m.table_load(), 2))

    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(101, hash_function_1)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 30)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key4', 40)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(20, hash_function_1)
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(25, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        if m.table_load() > 0.5:
            print(f"Check that the load factor is acceptable after the call to resize_table().\n"
                  f"Your load factor is {round(m.table_load(), 2)} and should be less than or equal to 0.5")

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            # all inserted keys must be present
            result &= m.contains_key(str(key))
            # NOT inserted keys must be absent
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.get_size(), m.get_capacity(), round(m.table_load(), 2))

    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(31, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))

    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(151, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.get_size(), m.get_capacity())
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(11, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))

    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)

    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(53, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(101, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(53, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.get_size(), m.get_capacity())
    m.resize_table(100)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - get_keys_and_values example 1")
    print("------------------------")
    m = HashMap(11, hash_function_2)
    for i in range(1, 6):
        m.put(str(i), str(i * 10))
    print(m.get_keys_and_values())

    m.resize_table(2)
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(12)
    print(m.get_keys_and_values())

    print("\nPDF - __iter__(), __next__() example 1")
    print("---------------------")
    m = HashMap(10, hash_function_1)
    for i in range(5):
        m.put(str(i), str(i * 10))
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)

    print("\nPDF - __iter__(), __next__() example 2")
    print("---------------------")
    m = HashMap(10, hash_function_2)
    for i in range(5):
        m.put(str(i), str(i * 24))
    m.remove('0')
    m.remove('4')
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)

