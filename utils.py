from rich.console import Console

console = Console()

"""all the validations for the user prompts"""
class InputValidator:

    def get_int_input(prompt):
        while True:
            user_input = input(prompt).strip()
            if not user_input.isdigit():
                console.print("[bold red]\u274C  Please enter a valid number.[/bold red]")
                continue
            return int(user_input)

    def get_non_empty_string(prompt, min_length=1, max_length=None):
        while True:
            value = input(prompt).strip()
            if not value:
                console.print("[bold red]\u274C  Input cannot be empty.[/bold red]")
                continue
            if len(value) < min_length:
                console.print(f"[bold red]\u274C  Input must be at least {min_length} characters long.[/bold red]")
                continue
            if max_length and len(value) > max_length:
                console.print(f"[bold red]\u274C  Input cannot exceed {max_length} characters.[/bold red]")
                continue
            if value.isdigit(): 
                console.print(f"[bold red]\u274C  Input cannot be only numbers. Please enter valid text.[/bold red]")
                continue
            return value

    def get_choice_input(prompt, choices):
        choices_lower = []
        for choice in choices:
            lower_choice = choice.lower()
            choices_lower.append(lower_choice)
        while True:
            value = input(prompt).strip().lower()
            if value not in choices_lower:
                console.print(f"[bold red]\u274C  Please enter one of [cyan]{choices}[/cyan].[/bold red]")
            else:
                for choice in choices:
                    if choice.lower() == value:
                        return choice

    def get_ticket_id_input(prompt, ticket_list):
        while True:
            user_input = input(prompt).strip()
            if user_input.lower() == "cancel":
                return "cancel"
            
            if not user_input:
                console.print("[bold red]\u274C  Enter valid Ticket Id.[/bold red]")
                continue
            ticket_id = str(user_input)
            ticket_exists = False
            for ticket in ticket_list:
                if ticket.ticket_id == ticket_id:
                    ticket_exists = True
                    break
                
            if not ticket_exists:
                console.print(f"[bold red]\u274C  Ticket ID {ticket_id} does not exist.[/bold red]")
                continue

            return ticket_id
