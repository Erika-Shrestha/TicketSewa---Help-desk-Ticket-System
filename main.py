from time import sleep
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
    console.print(" " + "\u2501" * 155, style="red") 
    loop=True
    while loop:
        try:
            input_option = InputValidator.get_int_input("Enter your desired option: ")
            if(input_option==1):
                console.print("[bold yellow]Enter Ticket Details[/bold yellow]")
                title = InputValidator.get_non_empty_string("Enter Ticket Title: ")
                description =  InputValidator.get_non_empty_string("Enter Ticket Description: ")
                created_by =  InputValidator.get_non_empty_string("Created by: ")
                assigned_to =  InputValidator.get_non_empty_string("Assign to: ")
                dependencies =  InputValidator.get_non_empty_string("Dependencies (enter Ticket IDs separated by comma): ")
                dependencies_list = [] 
                if dependencies.strip() != "":
                    for dep_id in dependencies.split(","):
                        dep_id_clean = dep_id.strip()   
                        dep_id_int = int(dep_id_clean)       
                        dep_ticket = None
                        for ticket in manager.ticket_list:
                            if ticket.ticket_id == dep_id_int:
                                dep_ticket = ticket
                                break
                        if dep_ticket is not None:
                            dependencies_list.append(dep_ticket)
                ticket = manager.create_ticket(title, description, created_by, assigned_to, dependencies_list)
                undo.push({"type": "create", "ticket": ticket})
                history.add_record(ticket)

            elif(input_option==2):
                console.print("Ticket process sub method")
                ticket_to_process = manager.get_next_ticket()
                if not ticket_to_process:
                    console.print("[yellow]No tickets available to process![/yellow]")
                    continue
                console.print(f"[cyan]Next ticket to process: ID {ticket_to_process.ticket_id}, Title: {ticket_to_process.title}, Priority: {ticket_to_process.priority}[/cyan]")
                loop_sub=True
                while loop_sub:
                    ui.show_process_ticket_menu()
                    sub_option = input("Enter the process you would like to operate: ")
                    if(sub_option=='a'):
                        console.print("[bold yellow]Change Ticket Status[/bold yellow]")
                        new_status = InputValidator.get_choice_input("Enter new status (Open/In-Progress/Resolved/Closed): ",["Open", "In-Progress", "Resolved", "Closed"])
                        prev_status = ticket_to_process.status
                        manager.update_ticket_status(ticket_to_process.ticket_id, new_status)
                        history.add_record(ticket_to_process)
                        undo.push({"type": "update_status", "ticket": ticket_to_process, "previous_status": prev_status})
                    elif(sub_option=='b'):
                        console.print("[bold yellow]Change Ticket Priority[/bold yellow]")
                        prev_priority = ticket_to_process.priority
                        new_priority = InputValidator.get_choice_input("Enter new priority (Low/Medium/High): ", ["Low", "Medium", "High"])
                        manager.update_ticket_priority(ticket_to_process.ticket_id, new_priority)
                        history.add_record(ticket_to_process)
                        undo.push({"type": "update_priority", "ticket": ticket_to_process, "previous_priority": prev_priority})
                    elif(sub_option=='c'):
                        console.print("[bold yellow]Check Dependencies[/bold yellow]")
                        if manager.check_dependency(ticket_to_process):
                            console.print(f"[green]All dependencies of Ticket {ticket_to_process.ticket_id} are resolved.[/green]")
                        else:
                            console.print(f"[red]Some dependencies of Ticket {ticket_to_process.ticket_id} are still unresolved.[/red]")
                    elif(sub_option=='d'):
                        console.print("[bold yellow]Go Back[/bold yellow]")
                        loop_sub=False
                    else:
                        console.print("Please enter correct process option.")

            elif(input_option==3):
                delete_ticket_id = InputValidator.get_ticket_id_input("Enter the Ticket ID you want to delete: ", manager.ticket_list) 
                ticket_to_delete = None
                for ticket in manager.ticket_list:
                    if ticket.ticket_id == delete_ticket_id:
                        ticket_to_delete = ticket
                        break
                if ticket_to_delete is not None:
                    manager.delete_ticket(delete_ticket_id)
                    undo.push({"type": "delete", "ticket": ticket_to_delete})
            elif(input_option==4):
                console.print("Show all tickets list method")
                manager.show_all_tickets()
            elif(input_option==5):
                console.print("history of ticket method")
                ticket_id_input = input("Enter Ticket ID to see history or Enter All to see all ticket history: ").strip()
                if (ticket_id_input.lower()=="all"):
                    history.show_history() 
                else:
                    ticket_id_int = int(ticket_id_input)
                    history.show_history(ticket_id_int) 
            elif(input_option==6):
                console.print("Undo of steps in ticket method")
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
                        console.print(f"[green]Undo: Ticket {ticket.ticket_id} deletion reverted.[/green]")

                    elif action_type == "update_status":
                        ticket.status = last_action["previous_status"]
                        console.print(f"[green]Undo: Ticket {ticket.ticket_id} status reverted to {ticket.status}.[/green]")

                    elif action_type == "update_priority":
                        ticket.priority = last_action["previous_priority"]
                        console.print(f"[green]Undo: Ticket {ticket.ticket_id} priority reverted to {ticket.priority}.[/green]")

                    history.add_record(ticket)
            elif(input_option==7):
                console.print("display dashboard analytics method")
                analytics_dashboard = TicketAnalytics(manager.ticket_list)
                analytics_dashboard.display_dashboard()
            elif(input_option==8):
                console.print("THE SYSTEM IS EXITING.....")
                console.print("THANK YOU FOR YOUR VISIT! :)")
                break
            else:
                console.print("Please enter only the options that are offered")
        except:
            console.print("Please enter correct input as an option")

choose_operation()
