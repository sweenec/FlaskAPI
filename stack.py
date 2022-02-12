# Last in First out order of insertions and removals

class Node:
    def __init__(self, data=None, next_node=None):
        self.data = data
        self.next_node = next_node


class Stack:
    def __init__(self):
        self.top = None     # only need to keep track of the top of the stack

    def check_top(self):
        return self.top

    def push(self, data):
        new_next = self.top
        new_top = Node(data, new_next)
        self.top = new_top

    def pop(self):
        if self.top is None:
            return None
        removed = self.top
        self.top = self.top.next_node
        return removed

