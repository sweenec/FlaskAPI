class Node:
    def __init__(self, data=None, next_node=None):
        self.data = data
        self.next_node = next_node


class Data:
    def __init__(self, key, value):
        self.key = key
        self.value = value


# Practice purposes (not a hugely performant hash table)
class HashTable:
    def __init__(self, table_size):
        self.table_size = table_size
        self.hash_table = [None] * table_size  # declare an empty list of length = table_size

    # always returns same hash for a given key
    def custom_hash(self, key):
        hash_value = 0
        for i in key:
            hash_value += ord(i)  # integer representation of a unicode character
            hash_value = (hash_value * ord(i)) % self.table_size  # adds more randomness/uniqueness to hash_value
        return hash_value

    def add_key_value_pair(self, key, value):
        hashed_key = self.custom_hash(key)
        if self.hash_table[hashed_key] is None:  # index of the hash_table is empty (efficient)
            self.hash_table[hashed_key] = Node(Data(key, value), None)
        else:  # collision (inefficient)
            node = self.hash_table[hashed_key]  # acts as head of linked_list
            while node.next_node:  # traverse linked list
                node = node.next_node
            node.next_node = Node(Data(key, value), None)  # insert node at end which points to None

    def get_value(self, key):
        hashed_key = self.custom_hash(key)
        if self.hash_table[hashed_key] is not None:
            node = self.hash_table[hashed_key]
            if node.next_node is None:
                return node.data.value
            while node:
                if key == node.data.key:
                    return node.data.value
                node = node.next_node
        return None

    # for testing
    def print_table(self):
        print("{")
        for k, val in enumerate(self.hash_table):
            if val is not None:
                llist_string = ""
                node = val
                if node.next_node:
                    while node.next_node:
                        llist_string += (
                            str(node.data.key) + " : " + str(node.data.value) + " --> "
                        )
                        node = node.next_node
                    llist_string += (
                            str(node.data.key) + " : " + str(node.data.value) + " --> None"
                    )
                    print(f"    [{k}] {llist_string}")
                else:
                    print(f"    [{k}] {val.data.key} : {val.data.value}")
            else:
                print(f"    [{k}] {val}")
        print("}")


# test hash table
# ht = HashTable(4)
# ht.add_key_value_pair("hi", "there")
# ht.add_key_value_pair("hi", "there")
# ht.add_key_value_pair("yo", "sup")
# ht.print_table()
