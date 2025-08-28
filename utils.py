from rich.console import Console

console = Console()

class InputValidator:

    def get_int_input(prompt):
        while True:
            user_input = input(prompt).strip()
            if not user_input.isdigit():
                console.print("[bold red]\u274CPlease enter a valid number.[/bold red]")
                continue
            return int(user_input)

    def get_non_empty_string(prompt):
        while True:
            value = input(prompt).strip()
            if value == "":
                console.print("[bold red]\u274CInput cannot be empty.[/bold red]")
            else:
                return value

    def get_choice_input(prompt, choices):
        choices_lower = []
        for choice in choices:
            lower_choice = choice.lower()
            choices_lower.append(lower_choice)
        while True:
            value = input(prompt).strip().lower()
            if value not in choices_lower:
                console.print(f"[bold red]\u274CPlease enter one of [cyan]{choices}[/cyan].[/bold red]")
            else:
                for choice in choices:
                    if choice.lower() == value:
                        return choice

    def get_ticket_id_input(prompt, ticket_list):
        while True:
            user_input = input(prompt).strip()
            if not user_input.isdigit():
                console.print("[bold red]\u274CTicket ID must be a number.[/bold red]")
                continue
            ticket_id = int(user_input)
            ticket_exists = False
            for ticket in ticket_list:
                if ticket.ticket_id == ticket_id:
                    ticket_exists = True
                    break
                
            if not ticket_exists:
                console.print(f"[bold red]\u274C Ticket ID {ticket_id} does not exist.[/bold red]")
                continue

            return ticket_id
