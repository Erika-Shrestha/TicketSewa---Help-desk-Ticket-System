from collections import deque
import heapq
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from ticket import Ticket 
from connectDb import get_db
from bson import ObjectId
from priority_queue import PriorityQueue

"""manages the logic to operate the tickets"""
class TicketManager:
    def __init__(self):
        self.console = Console()
        self.ticket_list = []  
        self.priority_queue = PriorityQueue() 
        self.current_ticket = None
        self.db = get_db()
        self.ticket_collection = self.db["Tickets"]
        self.load_tickets_from_db()
    
    """loads the tickets stored in database"""
    def load_tickets_from_db(self):
        tickets_data = list(self.ticket_collection.find({}))
        self.ticket_list = [] 
        self.priority_queue.heap.clear()
        self.priority_queue.counter = 0

        for data in tickets_data:
            dependencies_from_db = data.get("dependencies", [])
            dependencies_list = []
            for dep in dependencies_from_db:
                dependencies_list.append(str(dep))

            ticket = Ticket(
                title=data.get("title"),
                description=data.get("description"),
                created_by=data.get("created_by"),
                assigned_to=data.get("assigned_to"),
                dependencies=dependencies_list,
                ticket_id=str(data.get("_id"))
            )
            ticket.priority = data.get("priority", "Medium")
            ticket.status = data.get("status", "Open")

            self.ticket_list.append(ticket)
            self.priority_queue.enqueue(ticket)

    """creates the ticket and stores in respective lists"""
    def create_ticket(self, title, description, created_by=None, assigned_to=None, dependencies=None):
        ticket = Ticket(title=title, description=description, created_by=created_by, assigned_to=assigned_to, dependencies=dependencies)
        self.ticket_list.append(ticket)
        self.priority_queue.enqueue(ticket)
        self.console.print(f"[green]Ticket {ticket.ticket_id} created with priority {ticket.priority}![/green]")
        return ticket
    """deletes the ticket in respective lists"""
    def delete_ticket(self, ticket_id):
        found = False
        for ticket in self.ticket_list.copy():
            if ticket.ticket_id == ticket_id:
                confirm = input(f"Do you really want to delete Ticket {ticket_id}? (Y/N): ")
                if confirm.lower() == "y":
                    self.ticket_list.remove(ticket)
                    # Remove from priority queue
                    new_heap = []
                    for item in self.priority_queue.heap:
                        ticket_in_item = item[2]  # the actual ticket
                        if ticket_in_item != ticket:
                            new_heap.append(item)
                    self.priority_queue.heap = new_heap
                    heapq.heapify(self.priority_queue.heap)
                    
                    for t in self.ticket_list:
                        if ticket_id in t.dependencies:
                            t.dependencies.remove(ticket_id)
                            self.ticket_collection.update_one(
                                {"_id": ObjectId(t.ticket_id)},
                                {"$set": {"dependencies": t.dependencies}}
                            )

                    self.ticket_collection.delete_one({"_id": ObjectId(ticket_id)})
                    self.console.print(f"[red]Ticket {ticket_id} has been deleted![/red]")
                else:
                    self.console.print("[yellow]Deletion canceled.[/yellow]")
                found = True
                break
        if not found:
            self.console.print(f"[red]Ticket {ticket_id} not found.[/red]")
    """shows all the tickets in a table"""
    def show_all_tickets(self):
        if not self.ticket_list:
            self.console.print(
                Panel(
                    "[bold blue]No tickets available![/bold blue]",
                    title="[bold blue]INFORMATION[/bold blue]",
                    border_style="blue",
                    padding=(1, 4),
                    width=50
                )
            )
            return
        
        table = Table(title="All Tickets", show_lines=True)
        table.add_column("ID", justify="center", style="cyan")
        table.add_column("Title", style="magenta")
        table.add_column("Priority", justify="center", style="red")
        table.add_column("Status", justify="center", style="green")
        table.add_column("Created By", style="yellow")
        table.add_column("Assigned to", style="blue")
        table.add_column("Dependencies", style="purple")
        
        for ticket in self.ticket_list:
            if ticket.dependencies:
                dependency = ", ".join(ticket.dependencies)
            else:
                dependency = "N/A"

            table.add_row(
                str(ticket.ticket_id),
                ticket.title,
                ticket.priority,
                ticket.status,
                ticket.created_by,
                ticket.assigned_to,
                dependency
            )
        self.console.print(table)

    """checks the dependency of the ticket recursively to see unresolved dependencies"""
    def check_dependency(self, ticket):
        if not ticket.dependencies:
            #Since there is no dependency so can process
            return True  

        for dependency in ticket.dependencies:
            dep_ticket = None 
            for t in self.ticket_list:
                if t.ticket_id == dependency:
                    dep_ticket = t
                    break
            if dep_ticket is None or dep_ticket.status != "Resolved":
                return False
            # Recursively check dependencies of dependency
            if not self.check_dependency(dep_ticket):
                return False

        return True
    """updates the ticket status to the choices"""
    def update_ticket_status(self, ticket_id, new_status):
        ticket = None
        for new_ticket in self.ticket_list:
            if new_ticket.ticket_id == ticket_id:
                ticket = new_ticket
                break
        
        if ticket is not None:
            ticket.status = new_status
            self.ticket_collection.update_one(
                {"_id": ObjectId(ticket_id)},
                {"$set": {"status": new_status}}
            )
            self.console.print(f"[green]Ticket {ticket_id} status updated to {new_status}![/green]")
        else:
            self.console.print(f"[red]Ticket {ticket_id} not found.[/red]")
    """updates the ticket priority to the choices"""
    def update_ticket_priority(self, ticket_id, new_priority):
        ticket = None
        for new_ticket in self.ticket_list:
            if new_ticket.ticket_id == ticket_id:
                ticket = new_ticket
                break
        
        if ticket is not None:
            # Remove the ticket from the priority queue first
            new_heap = []
            for item in self.priority_queue.heap:
                ticket_in_item = item[2]
                if ticket_in_item != ticket:
                    new_heap.append(item)
            self.priority_queue.heap = new_heap
            heapq.heapify(self.priority_queue.heap)
            #updates the priority
            ticket.priority = new_priority
            #adds back to the priority queue so it is in the correct order
            self.priority_queue.enqueue(ticket)
            self.ticket_collection.update_one(
                {"_id": ObjectId(ticket_id)},
                {"$set": {"priority": new_priority}}
            )
            self.console.print(f"[green]Ticket {ticket_id} priority updated to {new_priority}![/green]")
        else:
            self.console.print(f"[red]Ticket {ticket_id} not found.[/red]")
    """process the ticket according to priority and dependency resolved"""
    def get_next_ticket(self):
        if self.current_ticket and self.current_ticket.status in ["Open", "In-Progress"]:
            if self.check_dependency(self.current_ticket):
                return self.current_ticket
            else:
                # If dependencies are now unresolved, skip it
                self.current_ticket = None

        # Otherwise, pick the next available ticket from the priority queue
        while not self.priority_queue.is_empty():
            ticket = self.priority_queue.dequeue()
            if ticket.status in ["Open", "In-Progress"] and self.check_dependency(ticket):
                self.current_ticket = ticket
                return ticket

        # No ticket available
        self.current_ticket = None
        return None