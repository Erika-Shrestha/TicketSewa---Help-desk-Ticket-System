from rich.console import Console
from rich.panel import Panel

class TicketAnalytics:
    def __init__(self, tickets_list):
        self.tickets_list = tickets_list
        self.console = Console()

    def ticket_summary(self):
        # Initialize counts
        total = len(self.tickets_list)
        open_tickets = 0
        closed_tickets = 0
        low = 0
        medium = 0
        high = 0

        for ticket in self.tickets_list:
            # Count by status
            if ticket.status == "Open":
                open_tickets += 1
            else:
                closed_tickets += 1

            if ticket.priority == "Low":
                low += 1
            elif ticket.priority == "Medium":
                medium += 1
            elif ticket.priority == "High":
                high += 1

        stats = [
            ["Total Tickets", total],
            ["Open Tickets", open_tickets],
            ["Closed Tickets", closed_tickets],
            ["Low Priority", low],
            ["Medium Priority", medium],
            ["High Priority", high]
        ]

        return stats

    def display_dashboard(self):
        stats = self.ticket_summary()

        colored_stats = []
        for key_metric, count in stats:

            if key_metric == "Total Tickets":
                count_color = "yellow"
            elif "Open" in key_metric or "Low" in key_metric:
                count_color = "green"
            else:
                count_color = "red"

            colored_stats.append(
                f"[bold cyan]{key_metric}:[/bold cyan] [bold {count_color}]{count}[/bold {count_color}]"
            )

        stats_text = "\n".join(colored_stats)

        self.console.print(
            Panel(
                stats_text,
                title="[bold magenta]Ticket Dashboard[/bold magenta]",
                border_style="bright_blue",
                padding=(1, 2),
            )
        )