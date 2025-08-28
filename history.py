from datetime import datetime

class HistoryNode:
    def __init__(self, ticket_id, title, status, priority, timestamp=None):
        self.ticket_id = ticket_id
        self.title = title
        self.status = status
        self.priority = priority
        self.timestamp = timestamp or datetime.now()
        self.next = None

class TicketHistory:
    def __init__(self):
        self.head = None
        self.tail = None

    def add_record(self, ticket):
        node = HistoryNode(ticket.ticket_id, ticket.title, ticket.status, ticket.priority)
        if self.head is None:
            self.head = node
            self.tail = node
        else:
            self.tail.next = node
            self.tail = node

    def show_history(self, ticket_id=None):
        current = self.head
        while current:
            if ticket_id is None or current.ticket_id == ticket_id:
                print(f"[{current.timestamp}] Ticket ID {current.ticket_id} | Title: {current.title} | Status: {current.status} | Priority: {current.priority}")
            current = current.next
