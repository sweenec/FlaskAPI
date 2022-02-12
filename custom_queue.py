# First in First out order of insertions and removals

class Node:
    def __init__(self, data=None, next_node=None):
        self.data = data
        self.next_node = next_node


class Queue:
    def __init__(self):
        self.head = None
        self.tail = None

    def enqueue(self, data):    # adds to tail of list
        if self.head is None and self.tail is None:  # if queue is empty
            self.head = self.tail = Node(data, None)    # insert new node as both head and tail
            return

        self.tail.next_node = Node(data, None)
        self.tail = self.tail.next_node
        return

    def dequeue(self):  # removes head of the list
        if self.head is None:  # if queue is empty
            return None
        removed = self.head
        self.head = self.head.next_node  # head/tail pointing to same place (previous Node will be garbage collected)
        if self.head is None:   # if queue has been emptied (but tail is still pointing to data)
            self.tail.next_node = None  # point tail to none
        return removed

