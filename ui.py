from rich.console import Console
from rich.layout import Layout
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from rich.align import Align
from rich import box
from rich.padding import Padding
from time import sleep
from rich.live import Live

class TicketSewaUI:

    def __init__(self):
        self.console = Console()
        self.layout = Layout()
        self.sub_bottom = None

    def display_page(self):
        self.layout.split_column(
            Layout(name="upper", ratio=4),
            Layout(name="lower", ratio=15) 
        )

        inner_panel1 = Panel(Align.center("\t\t[bold blue]TICKETSEWA[/bold blue]\n\u00A0\u00A0\u00A0\u00A0\u00A0\u00A0Kamalpokhari, Kathmandu, Nepal\n+977 9823738292 helpdesk@.ticketsewa.com"), border_style="yellow")
        inner_panel2 = Panel(Text("This system shows all customer tickets, including their status, priority, and history. Staff and admin can view, manage, and track tickets to solve customer problems efficiently, ensuring smooth operations and effective communication throughout the support process. All updates and changes are logged to provide a clear and accessible record for future reference.", justify="center", style="magenta"), border_style="yellow")
        grid = Table.grid(expand=True)
        grid.add_column()  
        grid.add_row(inner_panel1)
        grid.add_row(inner_panel2)
        upper_panel = Panel(grid, border_style="green")
        self.layout["upper"].update(upper_panel) 
        lower_panel_layout = Layout(name="lower_panel_layout")
        lower_panel = Panel(lower_panel_layout, border_style="yellow")
        self.layout["lower"].update(lower_panel)
        lower_panel_layout.split_column(
            Layout(name="sub_top", ratio=1),
            Layout(name="sub_bottom", ratio=2)
        )
        lower_panel_layout["sub_top"].split_row( 
            Layout(name="left"), 
            Layout(name="right") 
        )
        lower_panel_layout["sub_top"]["left"].update(
            Padding(
                Panel(
                    Align.left("[bold black]Choose the following options :-[/bold black]\n\n"
                                "[bold yellow][1][/bold yellow] Create Tickets\n"
                                "[bold yellow][2][/bold yellow] Process Tickets\n"
                                "[bold yellow][3][/bold yellow] View Tickets\n"
                                "[bold yellow][4][/bold yellow] Check Ticket Histories\n"
                                "[bold yellow][5][/bold yellow] Undo Ticket Changes\n"
                                "[bold yellow][6][/bold yellow] View Analytics\n"
                                "[bold yellow][7][/bold yellow] Exit"
                            ),
                    box=box.MINIMAL,                   
                    style="black on green",           
                    padding=(0,0)
                ),
                (1, 2, 1, 2)
            )
        )

        ascii_image="""
        .---------------------------------.  ヅ
        |         SUPPORT TICKET          |----> .-------------------------.
        |---------------------------------|      |         NOTICE          |
        |  ID:    _______                 |      |-------------------------|    
        |  Status: _________              |      | We listen to your issue |
        |  Priority: _________            |      '-------------------------'
        |---------------------------------|                   ||
        |  Issue: ______                  |                   ||
        |                                 |                   ||
        '---------------------------------'                   ''

        """
        lower_panel_layout["sub_top"]["right"].update(
            Padding(
                Panel(
                    Align.center(ascii_image), 
                    padding=(0,0)
                ),
                (0, 2, 0, 2)
            )
        )
        self.sub_bottom = lower_panel_layout["sub_bottom"] 
        self.sub_bottom.split_column(
            Layout(name="top", ratio=2),
            Layout(name="bottom", ratio=1)
        )
        self.sub_bottom["top"].update(
            Panel(
                Align.left("[bold red]Reasons to choose process ticket option[/bold red]\n\n"
                            "\u2713   Update Ticket Status: Keep ticket progress up to date.\n\n"
                            "\u2713   Track Dependencies: Ensure tasks are assigned correctly and tracked.\n\n"
                            "\u2713   Prioritize Tickets: Focus on urgent or high-impact issues first.\n\n"
                            "\u2713   Resolve Issues Faster: Streamline workflow to minimize delays.\n\n"
                            "\u2713   Maintain Accountability: Track who is working on which ticket.\n\n"
                        ),
                        padding=(3, 4),
            )
        )
        with Live(self.layout, refresh_per_second=20, console=self.console): 
            for i in range(101): 
                sleep(0.02) 
                self.sub_bottom["bottom"].update(
                    Panel(
                        Align.center(f"[bold cyan]Loading... {i}%[/bold cyan]"),
                        padding=(3, 2),
                    )
                )

            self.sub_bottom["bottom"].update(
                    Panel(
                        Align.center("[bold green]System ready. Select an option.[/bold green]"), 
                        border_style="green",
                        padding=(3,2)
                    )
            )

        return self.layout

