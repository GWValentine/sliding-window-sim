from collections import deque

class Buffer:
    def __init__(self, capacity):
        self.capacity = capacity
        self.q = deque()

    def is_full(self):
        return len(self.q) >= self.capacity
    
    def is_empty(self):
        return len(self.q) == 0
    
    def add(self, item):
        if not self.is_full():
            self.q.append(item)
            return True
        return False
    
    def remove(self):
        if not self.is_empty():
            return self.q.popleft()
        return None
    
    def peek(self):
        return self.q[0] if not self.is_empty() else None