from datetime import datetime
from rich.console import Console

console = Console()

"""the node structure of the ticket history"""
class HistoryNode:
    def __init__(self, ticket_id, title,  action_type="No Action", timestamp=None):
        self.ticket_id = str(ticket_id)
        self.title = title
        self.action_type = action_type 
        self.timestamp = timestamp or datetime.now()
        self.next = None

"""the actual linkedlist concept for the ticket history"""
class TicketHistory:
    def __init__(self):
        self.head = None
        self.tail = None

    """assigning action type to the linkedlist node"""
    def add_action(self, ticket_id, title, action_type, timestamp=None):
        timestamp = timestamp or datetime.now()
        new_node = HistoryNode(ticket_id, title, action_type, timestamp)
        if not self.head:
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node
    
    """insertion of new ticket history as node in the linkedlist"""
    def add_record(self, ticket):
        node = HistoryNode(ticket.ticket_id, ticket.title)
        if not self.head:
            self.head = node
            self.tail = node
        else:
            self.tail.next = node
            self.tail = node

    def show_history(self, ticket_id=None):
        current = self.head
        while current:
            if ticket_id is None or current.ticket_id == ticket_id:
                console.print(f"[dim cyan][{current.timestamp}] [/dim cyan][bold yellow]Ticket ID {current.ticket_id} [/bold yellow][bold green]| {current.title}: [/bold green][magenta]{current.action_type}[/magenta]")
            current = current.next
