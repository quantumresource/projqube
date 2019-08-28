
"""
A simple linked list implementation for the storage of gates.
This has the benefit of adding and removing element in O(1). This is a common
operation when performing commutation operators.
"""



class DLLNode(object):
    """
    Single node in the Doubly Linked List
    """
    def __init__(self, dataval=None):
        self.data = dataval
        self.next = None
        self.prev = None


class DoubleLinkedList(object):
    """
    Linked list for the storage of gates. This should be faster since many
    inserts and deletions will occur while applying permutation operations.
    """
    def __init__(self):
        self.head = None
        self.back = None

    def push_back(self,new_data):
        """
        appends a new element (at the back)
        """
        n = DLLNode(new_data)
        n.prev = self.back

        # check if DLList is empty
        if(self.back == None):
            self.head = n
        else:
            self.back.next = n

        self.back = n

        return

    def push_front(self, new_data):
        """
        pushes a new element to the front
        """
        n = DLLNode(new_data)
        n.next = self.head
        
        #check if DLL is empty
        if(self.head == None):
            self.back = n
        else:
            self.head.prev = n
        
        self.head = n
        return

    def pop_back(self):
        """
        Removes the last element from the Doubly Linked List and returns its
        data.
        """
        if (self.back == None):
            return None
        data = self.back.data
        self.back = self.back.prev
        return data

    def pop_front(self):
        """
        Removes the first element from the DoublyLinkedList and returns its
        data.
        """
        if (self.head == None):
            return None
        data = self.head.data
        self.head = self.head.next
        return data

    def remove_element(self, element):
        if(element.prev != None):
            element.prev.next = element.next
        else:
            self.head = element.next

        if(element.next != None):
            element.next.prev = element.prev
        else:
            self.back = element.prev
        return element.data

    def insert_before(self, element, new_data):
        n = DLLNode(new_data)
        n.prev = element.prev
        n.next = element
        
        if(n.prev != None):
            n.prev.next = n
        else:
            self.head = n
        element.prev = n
        return

    def insert_after(self, element, new_data):
        n = DLLNode(new_data)
        n.next = element.next
        n.prev = element
        
        if(n.next != None):
            n.next.prev = n
        else:
            self.back = n

        element.next = n
        return

    def count(self, func = lambda data: True):
        cur=self.head
        count = 1
        if(cur == None):
            return 0
        while(cur.next != None):
            if(func(cur.data)):
                count+=1
            cur = cur.next
        return count

    def swap_elements(self, elem1, elem2):
        assert(elem1 != elem2)
        elem1.next, elem2.next = elem2.next, elem1.next
        elem1.prev, elem2.prev = elem2.prev, elem1.prev

        if(elem1.next == elem1):
            elem2.prev, elem1.next = elem1.next, elem2.prev
        if(elem1.prev == elem1):
            elem2.next, elem1.prev = elem1.prev, elem2.next



        # adjust the elements before and after:
        if(elem1.prev != None):
            elem1.prev.next = elem1
        else:
            self.head = elem1

        if(elem1.next != None):
            elem1.next.prev = elem1
        else:
            self.back = elem1

        if(elem2.prev != None):
            elem2.prev.next = elem2
        else:
            self.head = elem2

        if(elem2.next != None):
            elem2.next.prev = elem2
        else:
            self.back = elem2
        return


    #iterator specific
    def __iter__(self):
        return NodeIterator(self.head)

    def __reversed__(self):
        #return ReverseNodeIterator(self.back)
        return reversed_ll(self.back)




#
# Helper functions: implement iterator for linked list
#

class reversed_ll(object):
    def __init__(self, start_node):
        self.start = start_node

    def __iter__(self):
        return ReverseNodeIterator(self.start)



class BaseIterator(object):
    def __init__(self, start_node):
        self.current = start_node

class NodeIterator(BaseIterator):
    def __next__(self):
        c = self.current
        if(self.current == None):
            raise StopIteration
        self.current = self.current.next
        return c

class ReverseNodeIterator(BaseIterator):
    def __next__(self):
        c = self.current
        if(self.current == None):
            raise StopIteration
        self.current = self.current.prev
        return c