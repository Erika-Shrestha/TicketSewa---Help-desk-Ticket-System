class UndoTicket:
    def __init__(self):
        self.stack = []

    def push(self, action):
        self.stack.append(action)

    def pop(self):
        if self.stack:
            return self.stack.pop()
        return None

    def is_empty(self):
        return len(self.stack) == 0
