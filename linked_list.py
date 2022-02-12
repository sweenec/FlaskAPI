# contains data and pointer to next node
class Node:
    def __init__(self, data=None, next_node=None):
        self.data = data
        self.next_node = next_node


# wrapper class to keep track of head/tail of linked list
class LinkedList:
    def __init__(self):
        self.head = None
        self.tail = None

    def to_list(self):
        l = []
        if self.head is None:
            return l
        
        node = self.head
        while node.next_node:
            l.append(node.data)   # add data from each node to array
            node = node.next_node
        return l

    def print_llist(self):
        llist_string = ""
        node = self.head
        if node is None:
           print(None)
        while node:     # while node is NOT None
            llist_string += f"{str(node.data)} -> "   
            node = node.next_node
        
        llist_string += "None" # always an empty node at the end of linked list
        print(llist_string)

    def insert_head(self, data):
        if self.head is None:
            self.head = Node(data, self.head)
            self.tail = self.head
            return
        new_node = Node(data, self.head)
        self.head = new_node

    def insert_tail(self, data):
        # check if linked ;ist is empty
        if self.head is None:
            self.insert_head(data)
            return
        # handles instance when we aren't keeping track of the tail (inefficient (takes ON time))
        if self.tail is None:
            node = self.head
            # traverse linked list until a node points to None
            while node.next_node:
                node = node.next_node
            
            node.next_node = Node(data, None)   # set next node of current tail to new Node instance
            self.tail = node.next_node          # update linked list tail
        
        # otherwise just find last node and point it to new Node then reset tail (Much more efficient (takes O1 time))
        else:
            self.tail.next_node = Node(data, None)
            self.tail = self.tail.next_node

    
    def get_user_by_id(self, user_id):
        node = self.head
        while node:
            if node.data["id"] is int(user_id):
                return node.data
            node = node.next_node
        return None