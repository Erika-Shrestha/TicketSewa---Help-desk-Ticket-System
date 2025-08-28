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
            Layout(name="upper", ratio=7),
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
            Layout(name="sub_top"),
            Layout(name="sub_bottom", size=12)
        )
        lower_panel_layout["sub_top"].split_row( 
            Layout(name="left", ratio=17), 
            Layout(name="right", ratio=22) 
        )
        lower_panel_layout["sub_top"]["left"].update(
            Padding(
                Panel(
                    Align.left("[bold black]Choose the following options :-[/bold black]\n\n"
                                "[bold yellow][1][/bold yellow] Create Tickets\n"
                                "[bold yellow][2][/bold yellow] Process Tickets\n"
                                "[bold yellow][3][/bold yellow] Delete Tickets\n"
                                "[bold yellow][4][/bold yellow] View Tickets\n"
                                "[bold yellow][5][/bold yellow] Check Ticket Histories\n"
                                "[bold yellow][6][/bold yellow] Undo Ticket Changes\n"
                                "[bold yellow][7][/bold yellow] View Analytics\n"
                                "[bold yellow][8][/bold yellow] Exit"
                            ),
                    box=box.MINIMAL,                   
                    style="black on green",           
                    padding=(0,0)
                ),
                (0, 2, 0, 2)
            )
        )

        ascii_image="""
        .------------------------------.  ヅ
        |      SUPPORT TICKET          |----> .-------------------------.
        |------------------------------|      |         NOTICE          |
        |  ID:    _______              |      |-------------------------|    
        |  Status: _________           |      | We listen to your issue |
        |  Priority: _________         |      '-------------------------'
        |------------------------------|                   ||
        |  Issue: ______               |                   ||                             
        '------------------------------'                   ''
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
            Layout(name="top", ratio=4),
            Layout(name="bottom", ratio=1)
        )
        self.sub_bottom["top"].update(
            Panel(
                Align.left("[bold red]Reasons to choose process ticket option[/bold red]\n\n"
                            "\u2713   Update Ticket Status: Keep ticket progress up to date.\n"
                            "\u2713   Track Dependencies: Ensure tasks are assigned correctly and tracked.\n"
                            "\u2713   Prioritize Tickets: Focus on urgent or high-impact issues first.\n"
                            "\u2713   Resolve Issues Faster: Streamline workflow to minimize delays.\n"
                            "\u2713   Maintain Accountability: Track who is working on which ticket.\n"
                        ),
            )
        )
        
        self.sub_bottom["bottom"].update(
            Panel(Align.center("[bold cyan]Loading... 0%[/bold cyan]"))
        )
        return self.layout
    
    def show_process_ticket_menu(self):
        table = Table(show_header=False, box=None, padding=(0, 2))
        table.add_row("[bold yellow]a)[/bold yellow] Change Ticket Status")
        table.add_row("[bold yellow]b)[/bold yellow] Change Ticket Priority")
        table.add_row("[bold yellow]c)[/bold yellow] Check Dependencies")
        table.add_row("[bold yellow]d)[/bold yellow] Process Priority Tickets")
        table.add_row("[bold yellow]e)[/bold yellow] Go Back")

        panel = Panel(
            table,
            title="[bold cyan]Ticket Processing Menu[/bold cyan]",
            border_style="magenta",
            padding=(1, 2)
        )
        self.console.print(panel)
