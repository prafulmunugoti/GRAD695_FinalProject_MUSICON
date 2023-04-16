class Node(object): ## Create node class with data and next and previous pointers vars
    def __init__(self, data=None, next=None, prev=None):
        self.data = data
        self.next = next
        self.prev = prev
