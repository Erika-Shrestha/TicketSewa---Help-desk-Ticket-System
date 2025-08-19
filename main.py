from rich.console import Console
from ui import TicketSewaUI


console = Console()

ui = TicketSewaUI()

layout = ui.display_page()

def choose_operation():
    console.print(" " + "\u2501" * 196, style="red") 

    loop=True
    while loop:
        try:
            input_option =int(input("Enter your desired option: "))
            if(input_option==1):
                console.print("Ticket details entry method")
            elif(input_option==2):
                console.print("Ticket process sub method")
            elif(input_option==3):
                console.print("Show all tickets list method")
            elif(input_option==4):
                console.print("history of ticket method")
            elif(input_option==5):
                console.print("Undo of steps in ticket method")
            elif(input_option==6):
                console.print("display dashboard analytics method")
            elif(input_option==7):
                console.print("THE SYSTEM IS EXITING.....")
                console.print("THANK YOU FOR YOUR VISIT! :)")
                break
            else:
                console.print("Please enter only the options that are offered")
        except:
            console.print("Please enter correct input as an option")

choose_operation()
