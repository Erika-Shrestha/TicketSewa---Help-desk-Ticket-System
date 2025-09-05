import heapq

"""priority-based queue"""
class PriorityQueue:
    def __init__(self):
        self.heap = []
        #to preserve insertion order for same-priority tickets
        self.counter = 0  
        self.priority_map = {"high": 0, "medium": 1, "low": 2}

    """compares and adds the smallest element at root"""
    def enqueue(self, ticket):
        #getting the numerical value where default is 3 if unknown
        priority_value = self.priority_map.get(ticket.priority.lower(), 3)
        # Use counter to maintain insertion order for same-priority tickets
        heapq.heappush(self.heap, (priority_value, self.counter, ticket))
        self.counter += 1

    """removes the ticket from heap tuple"""
    def dequeue(self):
        if not self.heap:
            return None
        #returns the ticket with highest priority (lowest numeric value)
        return heapq.heappop(self.heap)[2]

    def is_empty(self):
        return len(self.heap) == 0
