from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from ticket import Ticket 
from connectDb import get_db
from bson import ObjectId

class TicketManager:
    def __init__(self):
        self.console = Console()
        self.ticket_list = []  
        self.high_priority_queue = [] 
        self.standard_queue = [] 
        self.db = get_db()
        self.ticket_collection = self.db["Tickets"]
        self.load_tickets_from_db()
    
    def load_tickets_from_db(self):
        tickets_data = list(self.ticket_collection.find({}))
        self.ticket_list = [] 
        self.high_priority_queue = []
        self.standard_queue = []

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
            if ticket.priority.lower() == "high":
                self.high_priority_queue.append(ticket)
            else:
                self.standard_queue.append(ticket)

    def create_ticket(self, title, description, created_by=None, assigned_to=None, dependencies=None):
        ticket = Ticket(title=title, description=description, created_by=created_by, assigned_to=assigned_to, dependencies=dependencies)
        self.ticket_list.append(ticket)
        if ticket.priority.lower() == "high":
            self.high_priority_queue.append(ticket)
        else:
            self.standard_queue.append(ticket)

        self.console.print(f"[green]Ticket {ticket.ticket_id} created with priority {ticket.priority}![/green]")
        return ticket

    def delete_ticket(self, ticket_id):
        found = False
        for ticket in self.ticket_list.copy():
            if ticket.ticket_id == ticket_id:
                confirm = input(f"Do you really want to delete Ticket {ticket_id}? (Y/N): ")
                if confirm.lower() == "y":
                    self.ticket_list.remove(ticket)
                    if ticket in self.high_priority_queue:
                        self.high_priority_queue.remove(ticket)
                    elif ticket in self.standard_queue:
                        self.standard_queue.remove(ticket)
                    
                    for ticket in self.ticket_list:
                        if ticket_id in ticket.dependencies:
                            ticket.dependencies.remove(ticket_id)
                            self.ticket_collection.update_one(
                                {"_id": ObjectId(ticket.ticket_id)},
                                {"$set": {"dependencies": ticket.dependencies}}
                            )

                    self.ticket_collection.delete_one({"_id": ObjectId(ticket_id)})
                    self.console.print(f"[red]Ticket {ticket_id} has been deleted![/red]")
                else:
                    self.console.print("[yellow]Deletion canceled.[/yellow]")
                found = True
                break
        if not found:
            self.console.print(f"[red]Ticket {ticket_id} not found.[/red]")

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

    def check_dependency(self, ticket):
        if not ticket.dependencies:
            #Since there is no dependency so can process
            return True  

        for dependency in ticket.dependencies:
            dep_ticket = None 
            for ticket in self.ticket_list:
                if ticket.ticket_id == dependency:
                    dep_ticket = ticket
                    break
            if dep_ticket is None or dep_ticket.status != "Resolved":
                return False
            # Recursively check dependencies of dependency
            if not self.check_dependency(dep_ticket):
                return False

        return True
    
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

    def update_ticket_priority(self, ticket_id, new_priority):
        ticket = None
        for new_ticket in self.ticket_list:
            if new_ticket.ticket_id == ticket_id:
                ticket = new_ticket
                break
        
        if ticket is not None:
            if ticket in self.high_priority_queue:
                self.high_priority_queue.remove(ticket)
            elif ticket in self.standard_queue:
                self.standard_queue.remove(ticket)
            ticket.priority = new_priority
            if new_priority.lower() == "high":
                self.high_priority_queue.append(ticket)
            else:
                self.standard_queue.append(ticket)
            self.ticket_collection.update_one(
                {"_id": ObjectId(ticket_id)},
                {"$set": {"priority": new_priority}}
            )
            self.console.print(f"[green]Ticket {ticket_id} priority updated to {new_priority}![/green]")
        else:
            self.console.print(f"[red]Ticket {ticket_id} not found.[/red]")
        
    def get_next_ticket(self):

        old_high_priority = self.high_priority_queue
        old_standard = self.standard_queue
        new_high_priority = []
        new_standard = []
        for ticket in old_high_priority:
            if ticket.status not in ["Resolved"]:
                new_high_priority.append(ticket)
        for ticket in old_standard:
            if ticket.status not in ["Resolved"]:
                new_standard.append(ticket)
        
        self.high_priority_queue = new_high_priority
        self.standard_queue = new_standard

        for ticket in self.high_priority_queue:
            if ticket.status in ["Open", "In-Progress"] and self.check_dependency(ticket):
                return ticket  

        def get_priority_value(ticket):
            priority_order = {"medium": 1, "low": 2}  
            return priority_order.get(ticket.priority.lower(), 3)  

        self.standard_queue.sort(key=get_priority_value)
        
        for ticket in self.standard_queue:
            if ticket.status in ["Open", "In-Progress"] and self.check_dependency(ticket):
                return ticket
        return None
