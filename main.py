from time import sleep
from bson import ObjectId
from rich.console import Console
from rich.panel import Panel
from rich.align import Align
from rich.live import Live
from ui import TicketSewaUI
from rich.table import Table
from ticket_manager import TicketManager
from analytics import TicketAnalytics
from history import TicketHistory
from undo import UndoTicket
from utils import InputValidator

console = Console()

ui = TicketSewaUI()
manager = TicketManager()
history = TicketHistory()
undo = UndoTicket()

for ticket in manager.ticket_list:
    history.add_record(ticket)

layout = ui.display_page()

with Live(layout, refresh_per_second=20, console=console):
    for i in range(101):
        sleep(0.02)
        ui.sub_bottom["bottom"].update(
            Panel(Align.center(f"[bold cyan]Loading... {i}%[/bold cyan]"))
        )

    # Final state after loading completes
    ui.sub_bottom["bottom"].update(
        Panel(
            Align.center("[bold green]System ready. Select an option.[/bold green]"),
            border_style="green"
        )
    )

def choose_operation():
    console.print(" " + "\u2501" * 160, style="red") 
    loop=True
    while loop:
        try:
            input_option = InputValidator.get_int_input("Enter your desired option: ")
            if(input_option==1):
                console.print("[bold yellow]Enter Ticket Details[/bold yellow]")
                title = InputValidator.get_non_empty_string("Enter Ticket Title: ", min_length=5)
                description =  InputValidator.get_non_empty_string("Enter Ticket Description: ", min_length=10)
                created_by =  InputValidator.get_non_empty_string("Created by: ", min_length=5)
                assigned_to =  InputValidator.get_non_empty_string("Assign to: ", min_length=5)
                console.print("\n[bold cyan]Existing Tickets:[/bold cyan]")
                for ticket in manager.ticket_list:
                    console.print(f"[bold green]Ticket ID: {ticket.ticket_id}[/bold green] | [bold yellow]Title: {ticket.title}[/bold yellow]")
                print("\n")
                dependencies =  input("Dependencies (enter Ticket IDs separated by comma): ")
                dependencies_list = [] 
                if dependencies.strip():  
                    for dep_id in dependencies.split(","):
                        dep_id = dep_id.strip()
                        if dep_id:  
                            dep_id_str = str(dep_id)
                            dep_ticket = None
                            for ticket in manager.ticket_list:
                                if ticket.ticket_id == dep_id_str:
                                    dep_ticket = ticket
                                    break
                            if dep_ticket:
                                dependencies_list.append(str(dep_ticket.ticket_id))
                                console.print(f"[green]Ticket ID {dep_id_str} found, assigning.[/green]")
                            else:
                                console.print(f"[red]Ticket ID {dep_id_str} not found, ignoring.[/red]")
                        else:
                            console.print(f"[red]Invalid Ticket ID '{dep_id}', ignoring.[/red]")
                ticket = manager.create_ticket(title, description, created_by, assigned_to, dependencies_list)
                undo.push({"type": "create", "ticket": ticket})
                history.add_action(ticket.ticket_id, ticket.title, f"The ticket is created by {ticket.created_by}")

            elif(input_option==2):
                ticket_to_process = manager.get_next_ticket()
                if not ticket_to_process:
                    console.print("[yellow]No tickets available to process![/yellow]")
                    continue

                console.print(f"[cyan]Processing Ticket ID {ticket_to_process.ticket_id}: {ticket_to_process.title}[/cyan]")

                while True:
                    ui.show_process_ticket_menu()
                    sub_option = input("Enter the process you would like to operate: ").strip().lower()

                    if sub_option == "a":
                        if not manager.check_dependency(ticket_to_process):
                            console.print(f"[red]Cannot update status. Dependencies are unresolved.[/red]")
                            continue
                        prev_status = ticket_to_process.status
                        new_status = InputValidator.get_choice_input(
                            "Enter new status (Open/In-Progress/Resolved/Closed): ",
                            ["Open", "In-Progress", "Resolved", "Closed"]
                        )
                        if new_status != ticket_to_process.status:
                            manager.update_ticket_status(ticket_to_process.ticket_id, new_status)
                            history.add_action(ticket_to_process.ticket_id, ticket_to_process.title, f"The ticket status updated by {ticket_to_process.assigned_to} to {new_status}")
                            undo.push({"type": "update_status", "ticket": ticket_to_process, "previous_status": prev_status})
                        else:
                            console.print(f"[red]No changes Made[/red]")
                    elif sub_option == "b":
                        prev_priority = ticket_to_process.priority
                        new_priority = InputValidator.get_choice_input(
                            "Enter new priority (Low/Medium/High): ",
                            ["Low", "Medium", "High"]
                        )
                        if new_priority != ticket_to_process.priority:
                            manager.update_ticket_priority(ticket_to_process.ticket_id, new_priority)
                            history.add_action(ticket_to_process.ticket_id, ticket_to_process.title, f"The ticket priority updated by {ticket_to_process.assigned_to} to {new_priority}")
                            undo.push({"type": "update_priority", "ticket": ticket_to_process, "previous_priority": prev_priority})
                        else:
                            console.print(f"[red]No changes Made[/red]")
                    elif sub_option == "c":
                        if manager.check_dependency(ticket_to_process):
                            console.print(f"[green]All dependencies of Ticket {ticket_to_process.ticket_id} are resolved.[/green]")
                        else:
                            console.print(f"[red]Some dependencies of Ticket {ticket_to_process.ticket_id} are still unresolved.[/red]")

                    elif sub_option == "d":
                        break  

                    else:
                        console.print("[red]Please enter a correct process option.[/red]")

            elif(input_option==3):
                console.print("\n[bold cyan]Existing Tickets:[/bold cyan]")
                for ticket in manager.ticket_list:
                    console.print(f"[bold green]Ticket ID: {ticket.ticket_id}[/bold green] | [bold yellow]Title: {ticket.title}[/bold yellow]")
                print("\n")
                delete_ticket_id = InputValidator.get_ticket_id_input("Enter the Ticket ID you want to delete or enter 'cancel' to go back: ", manager.ticket_list).strip()
                if delete_ticket_id.lower() == "cancel":
                    console.print("[yellow]Deletion canceled.[/yellow]")
                    continue
                ticket_to_delete = None
                for ticket in manager.ticket_list:
                    if ticket.ticket_id == delete_ticket_id:
                        ticket_to_delete = ticket
                        break
                if ticket_to_delete is not None:
                    manager.delete_ticket(delete_ticket_id)
                    undo.push({"type": "delete", "ticket": ticket_to_delete})
            elif(input_option==4):
                manager.show_all_tickets()
            elif(input_option==5):
                console.print("[bold yellow]history of ticket method[/bold yellow]")
                ticket_id_input = input("Enter Ticket ID to see history or Enter All to see all ticket history: ").strip()
                if (ticket_id_input.lower()=="all"):
                    history.show_history() 
                else:
                    ticket_id_int = str(ticket_id_input)
                    history.show_history(ticket_id_int) 
            elif(input_option==6):
                if undo.is_empty():
                    console.print("[yellow]Nothing to undo![/yellow]")
                else:
                    last_action = undo.pop()
                    action_type = last_action["type"]
                    ticket = last_action["ticket"]

                    if action_type == "create":
                        manager.delete_ticket(ticket.ticket_id)
                        console.print(f"[green]Undo: Ticket {ticket.ticket_id} creation reverted.[/green]")

                    elif action_type == "delete":
                        manager.ticket_list.append(ticket)
                        manager.ticket_collection.insert_one(ticket.to_dict())
                        console.print(f"[green]Undo: Ticket {ticket.ticket_id} deletion reverted.[/green]")

                    elif action_type == "update_status":
                        ticket.status = last_action["previous_status"]
                        manager.ticket_collection.update_one(
                            {"_id": ObjectId(ticket.ticket_id)},
                            {"$set": {"status": ticket.status}}
                        )
                        console.print(f"[green]Undo: Ticket {ticket.ticket_id} status reverted to {ticket.status}.[/green]")

                    elif action_type == "update_priority":
                        ticket.priority = last_action["previous_priority"]
                        manager.ticket_collection.update_one(
                            {"_id": ObjectId(ticket.ticket_id)},
                            {"$set": {"priority": ticket.priority}}
                        )
                        console.print(f"[green]Undo: Ticket {ticket.ticket_id} priority reverted to {ticket.priority}.[/green]")

                    history.add_action(ticket.ticket_id, ticket.title, f"The ticket latest action has been undone by {ticket.created_by}")
            elif(input_option==7):
                console.print("display dashboard analytics method")
                analytics_dashboard = TicketAnalytics(manager.ticket_list)
                analytics_dashboard.display_dashboard()
            elif(input_option==8):
                console.print("[bold green]THE SYSTEM IS EXITING.....[/bold green]")
                console.print("[bold green]THANK YOU FOR YOUR VISIT! :)[/bold green]")
                break
            else:
                console.print("[bold red]Please enter only the options that are offered[/bold red]")
        except Exception as e:
                console.print(f"[red]Error: {e}[/red]")

choose_operation()
