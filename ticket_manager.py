from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from ticket import Ticket 

class TicketManager:
    def __init__(self):
        self.console = Console()
        # store all tickets
        self.ticket_list = []  
        self.high_priority_queue = [] 
        self.standard_queue = [] 

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

        for ticket in self.ticket_list:
            table.add_row(
                str(ticket.ticket_id),
                ticket.title,
                ticket.priority,
                ticket.status,
                ticket.created_by or "N/A"
            )
        self.console.print(table)

    def check_dependency(self, ticket):
        if not ticket.dependencies:
            #Since there is no dependency so can process
            return True  

        for dependency in ticket.dependencies:
            if dependency.status != "Resolved":
                return False
            # Recursively check dependencies of dependency
            if not self.check_dependency(dependency):
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
            self.console.print(f"[green]Ticket {ticket_id} priority updated to {new_priority}![/green]")
        else:
            self.console.print(f"[red]Ticket {ticket_id} not found.[/red]")
        
    def get_next_ticket(self):
        if self.high_priority_queue:
            return self.high_priority_queue.pop(0)
        elif self.standard_queue:
            return self.standard_queue.pop(0)
        else:
            return None
