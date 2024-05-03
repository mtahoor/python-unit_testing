from __future__ import annotations
from typing import Generic, TypeVar, List

from data_structures.referential_array import ArrayR

K = TypeVar("K")
V = TypeVar("V")


class InfiniteHashTable(Generic[K, V]):
    TABLE_SIZE = 27

    def __init__(self, level: int = 0) -> None:
        self.array: ArrayR[tuple[K, V] | None] = ArrayR(self.TABLE_SIZE)
        self.count = 0
        self.level = level

    def hash(self, key: K) -> int:
        if self.level < len(key):
            return ord(key[self.level]) % (self.TABLE_SIZE - 1)
        return self.TABLE_SIZE - 1

    def __getitem__(self, key: K) -> V:
        """
        Get the value at a certain key

        :raises KeyError: when the key doesn't exist.
        """
        position = self.hash(key)
        if position is None:
            raise KeyError("Key not found")
        else:
            return self.array[position]
        
    def __setitem__(self, key: K, value: V) -> None:
        """
        Set a (key, value) pair in our hash table.
        """
        if not isinstance(key, str):
            raise TypeError("Key must be a string")

        position = self.hash(key)
        if self.array[position] is None:
            print(f"Inserted root {position} ----- {key} - {value}")
            self.array[position] = (key, value)
            self.count += 1
        else:
            # Handle collision
            if isinstance(self.array[position], InfiniteHashTable):
                # If the current slot is another hash table, recurse
                print("Recurse")
                self.array[position][key] = value
            else:
                common_prefix_length = self.get_common_prefix_length(key, self.array[position][0])
                if common_prefix_length > 0:
                    # Create a new table for the common prefix if not already created
                    if not isinstance(self.array[position], InfiniteHashTable):
                        self.array[position] = InfiniteHashTable(self.level + 1)
                    
                    # Extract the common prefix
                    common_prefix = key[:common_prefix_length]
                    
                    # Insert the common prefix into the current position
                    self.array[position] = (common_prefix, None)
                    
                    # Extract the remaining part of the existing key after the common prefix
                    existing_key_suffix = self.array[position][0][common_prefix_length:]
                    
                    # Create a new table for the existing key suffix if not already created
                    if not isinstance(self.array[position][1], InfiniteHashTable):
                        self.array[position][1] = InfiniteHashTable(self.level + 1)
                    
                    # Insert the existing key into the new sub-table
                    self.array[position][1][existing_key_suffix] = None
                    
                    # Extract the remaining part of the incoming key after the common prefix
                    new_key_suffix = key[common_prefix_length:]
                    
                    # Insert the new key into the new sub-table
                    self.array[position][1][new_key_suffix] = value
                else:
                    # Handle collision using linear probing
                    next_position = (position + 1) % self.TABLE_SIZE
                    while next_position != position:
                        if self.array[next_position] is None:
                            print(f"Inserted at {next_position} ----- {key} - {value}")
                            self.array[next_position] = (key, value)
                            self.count += 1
                            return
                        elif isinstance(self.array[next_position], InfiniteHashTable):
                            print("Recurse")
                            self.array[next_position][key] = value
                            return
                        next_position = (next_position + 1) % self.TABLE_SIZE
                    # If no empty slot found after probing entire array
                    raise RuntimeError("Hash table is full")


   
      
    def get_common_prefix_length(self, key1: str, key2: str) -> int:
        """
        Get the length of the common prefix between two keys.
        """
        common_length = 0
        min_length = min(len(key1), len(key2))
        for i in range(min_length):
            if key1[i] == key2[i]:
                common_length += 1
            else:
                break
        print(f"Common prefix length between '{key1}' and '{key2}': {common_length}")
        return common_length



    def __delitem__(self, key: K) -> None:
        """
        Deletes a (key, value) pair in our hash table.

        :raises KeyError: when the key doesn't exist.
        """
        position = self.hash(key)
        
        
        self.array[position] = None

    def __len__(self) -> int:
        """
        Returns the number of elements in the hash table.
        """
        return sum(1 for item in self.array if item is not None)

    def __str__(self) -> str:
        """
        String representation.

        Not required but may be a good testing tool.
        """
        return str([item for item in self.array if item is not None])

    def get_location(self, key: K) -> List[int]:
        """
        Get the sequence of positions required to access this key.

        :raises KeyError: when the key doesn't exist.
        """
        def get_location(self, key: K) -> List[int]:
            """
            Get the sequence of positions required to access this key.

            :raises KeyError: when the key doesn't exist.
            """
            positions = []
            try:
                current_level = 0
                current_key = key
                while True:
                    position = self.hash(current_key)
                    if self.array[position] is None or self.array[position][0] != key:
                        break
                    else:
                        positions.append(position)
                        if isinstance(self.array[position], InfiniteHashTable):
                            # If the current slot is another hash table, recurse
                            positions.extend(self.array[position].get_location(current_key[len(key) - len(current_key) + current_level:]))
                        current_level += 1
            except KeyError:
                raise KeyError("Key not found")
            if not positions:
                raise KeyError("Key not found")
            return positions

    def __contains__(self, key: K) -> bool:
        """
        Checks to see if the given key is in the Hash Table

        :complexity: See linear probe.
        """
        try:
            _ = self[key]
        except KeyError:
            return False
        else:
            return True

    def sort_keys(self, current=None) -> list[str]:
        """
        Returns all keys currently in the table in lexicographically sorted order.
        """
        keys = []
        for item in self.array:
            if item is not None:
                keys.append(item[0])
        keys.sort()
        return keys
