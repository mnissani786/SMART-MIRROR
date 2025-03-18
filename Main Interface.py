import customtkinter as ctk
import time
import calendar
from API_Data import temp
from API_Data import weather_color
from API_Data import clouds
from API_Data import quote
from goveeTest import *

# Initialize the main window
ctk.set_appearance_mode("dark")  # Optional: Dark mode
ctk.set_default_color_theme("blue")  # Optional: Default theme

root = ctk.CTk()
root.title("Reflective Assistant")

root.geometry("500x700")
# Create the clock label
clock = ctk.CTkLabel(root, font=("Aptos (Body)", 30), text_color="white")
clock.place(x=250, y=350, anchor="center")  # Exactly in the center of the screen

updating = False  # Flag to control time updates

#place qoute on screen
Quote_write = ctk.CTkLabel(root,text = "",font = ("Aptos (Body)", 30), text_color = "white", wraplength= 450)
Quote_write.place(x= 250, y= 350, anchor = "center")

#new Idle screen
def Idle_screen():
    Quote_write.configure(text = str(quote))
    root.after(10000, show_smile) #after 10 seconds show SMILE

# Function to show "SMILE" first
def show_smile():
    Quote_write.configure(text = "") #removes quote from screen (need to improve technique for this
    clock.configure(text="SMILE")
    root.after(3000, start_clock)  # After 3 seconds, show date and time

# Function to start showing date and time
def start_clock():
    global updating
    updating = True  # Enable updating
    update_time()
    root.after(3000, move_clock_up, 350)  # Move clock up after 3 seconds

# Function to update time (only if updating is enabled)
def update_time():
    if updating:
        current_time = time.strftime("%I:%M %p")
        current_date = time.strftime("%B %d")
        clock.configure(text=f"{current_time}\n{current_date}")
        clock.after(1000, update_time)  # Keep updating every second

# Function to move the clock up smoothly from y=350 to y=200
def move_clock_up(y):
    global updating
    updating = False  # Stop updating during movement to prevent flickering
    if y > 200:
        clock.place(y=y-1)
        root.after(5, move_clock_up, y-1)
    else:
        updating = True  # Resume updates after movement
        update_time()
        show_widgets()

# Function to handle "Ask Mirror" button click
def ask_mirror():
    print("Ask Mirror Clicked!")

# Function to move the selection box
def move_selection_box(frame, currentCol, currentRow, nextCol, nextRow):    
    nextWidget = frame.grid_slaves(row=nextRow, column=nextCol)    # locates the widget using corresponding row and column, returns a list
    nextWidget[0].configure(border_width=3, border_color='white')   # Accesses first widget in the list and turns the border white

    currentWidget = frame.grid_slaves(row=currentRow, column=currentCol) # Locates the current selected widget
    currentWidget[0].configure(border_width=3, border_color='black')  # Changes the border to black

    return currentCol, currentRow, nextCol, nextRow, nextWidget  #returns updated variables

# Function to ask the user to enter a command for the selection box
def selection_box_commands(frame):
    currentCol = 0
    currentRow = 1
    nextCol = 0
    nextRow = 0

    gridSize = frame.grid_size() # gets grid size
    print(f"Size of grid: rows={gridSize[1]}, columns={gridSize[0]}") #for debugging

    currentSelectedWidget = frame.grid_slaves(row=currentRow, column=currentCol) #retrives button widget in top left corner
    currentSelectedWidget[0].configure(border_width=3, border_color='white') #Visually selects it using a white border

    print(f"Enter a command: up(u), down(d), left(l), right(r), select(s), exit(e): ") # Asks user for command input
    while (True):
        command = input(f"command: ")
        if (command == 'up' or command == 'u'):
            print(f"Command entered: up")
            try: 
                nextRow = currentRow -2 # moves selection to upper row, specific for smart home widget
                currentCol, currentRow, nextCol, nextRow, currentSelectedWidget = move_selection_box(frame, currentCol, currentRow, nextCol, nextRow)
                currentRow = nextRow
            except:
                if (nextRow < 0): 
                    print(f"Out of grid range")
            
        elif(command == 'down' or command == 'd'):
            print(f"Command entered: down")
            try: 
                nextRow = currentRow +2 # moves selection to lower row, specific for smart home widget
                currentCol, currentRow, nextCol, nextRow, currentSelectedWidget = move_selection_box(frame, currentCol, currentRow, nextCol, nextRow)
                currentRow = nextRow                
            except:
                if (nextRow > gridSize[1]-1): 
                    print(f"Out of grid range")    

        elif(command == 'left' or command == 'l'):
            print(f"Command entered: left")            
            try:     
                nextCol = currentCol -1 # moves selection to left column
                currentCol, currentRow, nextCol, nextRow, currentSelectedWidget = move_selection_box(frame, currentCol, currentRow, nextCol, nextRow)
                currentCol = nextCol
            except:
                if (nextCol < 0): 
                    print(f"Out of grid range")

        elif(command == 'right' or command == 'r'):
            print(f"Command entered: right")
            try:
                nextCol = currentCol +1  # moves selection to right column
                currentCol, currentRow, nextCol, nextRow, currentSelectedWidget = move_selection_box(frame, currentCol, currentRow, nextCol, nextRow)
                currentCol = nextCol            
            except:
                if (nextCol > gridSize[0]-1): 
                    print(f"Out of grid range")

        elif(command == 'select' or command == 's'):
            print(f"Command entered: select")
            currentSelectedWidget[0].invoke()  # runs command associated with the currently selected button

        elif(command == 'exit' or command == 'e'):
            print(f"Exiting loop")
            break

        else:
            print(f"not a command")   


# Closes the interactive pop-up widget, can be used for other interactive widgets
def close_widget(frame):
    frame.place_forget()    

def smart_home_widget():
    frame = ctk.CTkFrame(master=root, width = 200, height=200, fg_color="black", border_width=3, border_color="white")

    #This places the smart home frame and all its widgets
    frame.place(relx=.5, rely=.5, anchor="center", bordermode = 'outside')
    for i in range(9):
        frame.rowconfigure(i, weight=1)
    for i in range(6):
        frame.columnconfigure(i, weight=1)
    
    titleLabel = ctk.CTkLabel(frame, text="Govee Devices:", font=("Arial", 12), text_color="white", fg_color="black")
    closeWindow = ctk.CTkButton(frame, text="X", font=("Arial", 12), text_color="white", fg_color="black", width=10, command=lambda: close_widget(frame))
    devicesButton = ctk.CTkButton(frame, text="Lamp", font=("Arial", 10), text_color="white", fg_color="black", width=10)

    powerLabel = ctk.CTkLabel(frame, text="Power:", font=("Arial", 12), text_color="white", fg_color="black")
    onButton = ctk.CTkButton(frame, text="ON", font=("Arial", 10), text_color="white", fg_color="black", width=10, command=lambda: changeLight("devices.capabilities.on_off", "powerSwitch", 1))        
    offButton = ctk.CTkButton(frame, text="OFF", font=("Arial", 10), text_color="white", fg_color="black", width=10, command=lambda: changeLight("devices.capabilities.on_off", "powerSwitch", 0))        

    brightnessLabel = ctk.CTkLabel(frame, text="Brightness:", font=("Arial", 12), text_color="white", fg_color="black")
    percent1Button = ctk.CTkButton(frame, text="1%", font=("Arial", 10), text_color="white", fg_color="black", width=10, command=lambda: changeLight("devices.capabilities.range", "brightness", 1))
    percent25Button = ctk.CTkButton(frame, text="25%", font=("Arial", 10), text_color="white", fg_color="black", width=10, command=lambda: changeLight("devices.capabilities.range", "brightness", 25))
    percent50Button = ctk.CTkButton(frame, text="50%", font=("Arial", 10), text_color="white", fg_color="black", width=10, command=lambda: changeLight("devices.capabilities.range", "brightness", 50))
    percent75Button = ctk.CTkButton(frame, text="75%", font=("Arial", 10), text_color="white", fg_color="black", width=10, command=lambda: changeLight("devices.capabilities.range", "brightness", 75))
    percent100Button = ctk.CTkButton(frame, text="100%", font=("Arial", 10), text_color="white", fg_color="black", width=10, command=lambda: changeLight("devices.capabilities.range", "brightness", 100))

    whiteTempLabel = ctk.CTkLabel(frame, text="White Temperature:", font=("Arial", 12), text_color="white", fg_color="black")
    coolTempButton = ctk.CTkButton(frame, text="Cool", font=("Arial", 10), text_color="white", fg_color="black", width=10, command=lambda: changeLight("devices.capabilities.color_setting", "colorTemperatureK", 9000))
    pureTempButton = ctk.CTkButton(frame, text="Pure", font=("Arial", 10), text_color="white", fg_color="black", width=10, command=lambda: changeLight("devices.capabilities.color_setting", "colorTemperatureK", 5500))
    warmTempButton = ctk.CTkButton(frame, text="Warm", font=("Arial", 10), text_color="white", fg_color="black", width=10, command=lambda: changeLight("devices.capabilities.color_setting", "colorTemperatureK", 2000))

    colorLabel = ctk.CTkLabel(frame, text="Color:", font=("Arial", 12), text_color="white", fg_color="black")
    redButton = ctk.CTkButton(frame, text="Red", font=("Arial", 10), text_color="white", fg_color="black", width=10, command=lambda: changeLight("devices.capabilities.color_setting", "colorRgb", int(colorConversion(255, 0, 0))))
    orangeButton = ctk.CTkButton(frame, text="Orange", font=("Arial", 10), text_color="white", fg_color="black", width=10, command=lambda: changeLight("devices.capabilities.color_setting", "colorRgb", int(colorConversion(255, 127, 0))))
    yellowButton = ctk.CTkButton(frame, text="Yellow", font=("Arial", 10), text_color="white", fg_color="black", width=10, command=lambda: changeLight("devices.capabilities.color_setting", "colorRgb", int(colorConversion(255, 255, 0))))
    greenButton = ctk.CTkButton(frame, text="Green", font=("Arial", 10), text_color="white", fg_color="black", width=10, command=lambda: changeLight("devices.capabilities.color_setting", "colorRgb", int(colorConversion(0, 255, 0))))
    blueButton = ctk.CTkButton(frame, text="Blue", font=("Arial", 10), text_color="white", fg_color="black", width=10, command=lambda: changeLight("devices.capabilities.color_setting", "colorRgb", int(colorConversion(0, 0, 255))))
    purpleButton = ctk.CTkButton(frame, text="Purple", font=("Arial", 10), text_color="white", fg_color="black", width=10, command=lambda: changeLight("devices.capabilities.color_setting", "colorRgb", int(colorConversion(160, 0, 255))))

    titleLabel.grid(column = 0, row = 0, columnspan = 3, sticky='sw', pady = 3, padx = 13)
    closeWindow.grid(column = 5, row = 0,  pady = 3, padx = 3)
    devicesButton.grid(column = 0, row = 1, sticky='n', pady = 3, padx = 7)

    powerLabel.grid(column = 0, row = 2, columnspan = 3, sticky='sw', padx = 13)
    onButton.grid(column = 0, row = 3, sticky='n', pady = 3, padx = 3)
    offButton.grid(column = 1, row = 3, sticky='n', pady = 3, padx = 3)

    brightnessLabel.grid(column = 0, row = 4, columnspan = 3, sticky='sw', padx = 13)
    percent1Button.grid(column = 0, row = 5, sticky='n', pady = 3, padx = 3)
    percent25Button.grid(column = 1, row = 5, sticky='n', pady = 3, padx = 3)
    percent50Button.grid(column = 2, row = 5, sticky='n', pady = 3, padx = 3)
    percent75Button.grid(column = 3, row = 5, sticky='n', pady = 3, padx = 3)
    percent100Button.grid(column = 4, row = 5, sticky='n', pady = 3, padx = 3)

    whiteTempLabel.grid(column = 0, row = 6, columnspan = 3, sticky='sw', padx = 13)
    coolTempButton.grid(column = 0, row = 7, sticky='n', pady = 3, padx = 3)
    pureTempButton.grid(column = 1, row = 7, sticky='n', pady = 3, padx = 3)
    warmTempButton.grid(column = 2, row = 7, sticky='n', pady = 3, padx = 3)

    colorLabel.grid(column = 0, row = 8, columnspan = 3, sticky='sw', padx = 13)
    redButton.grid(column = 0, row = 9, sticky='n', pady = 3, padx = 3)
    orangeButton.grid(column = 1, row = 9, sticky='n', pady = 3, padx = 3)
    yellowButton.grid(column = 2, row = 9, sticky='n', pady = 3, padx = 3)
    greenButton.grid(column = 3, row = 9, sticky='n', pady = 3, padx = 3)
    blueButton.grid(column = 4, row = 9, sticky='n', pady = 3, padx = 3)
    purpleButton.grid(column = 5, row = 9, sticky='n', pady = 3, padx = 3)   

    #Figuring out selection box
    selection_box_commands(frame)
        

# Function to show widgets using CustomTkinter
def show_widgets():
    # Adjusting coordinates based on window size
    widgets = [
        {"text": "Calendar", "x": 50, "y": 50},
        {"text": "Weather", "x": 250, "y": 50},
        {"text": "To-Do List", "x": 50, "y": 200},
        {"text": "Music", "x": 50, "y": 400},
        {"text": "Settings", "x": 50, "y": 600},
    ]

    for widget in widgets:
        label = ctk.CTkLabel(root, text=widget["text"], font=("Arial", 20), text_color="white")
        label.place(x=widget["x"], y=widget["y"])

    # Creating functional widgets with adjusted coordinates
    calendar_widget = ctk.CTkLabel(root, text=calendar.month_name[time.localtime().tm_mon], font=("Arial", 15))
    calendar_widget.place(x=50, y=80)

    #weather_widget = ctk.CTkLabel(root, text="Sunny, 25°C", font=("Arial", 15))
    #updated weather widget
    weather_widget = ctk.CTkLabel(root, text= str(temp) + " Degrees Celsius\n" + str(clouds) + "% Cloudy", font=("Arial", 15), fg_color= weather_color, text_color= ("Black"))
    weather_widget.place(x=250, y=120)  # Positioned higher to prevent overlap with the clock

    todo_widget = ctk.CTkLabel(root, text="1. Study\n2. Work on Project\n3. Exercise", font=("Arial", 15))
    todo_widget.place(x=50, y=230)

    music_widget = ctk.CTkLabel(root, text="Playing: Song XYZ", font=("Arial", 15))
    music_widget.place(x=50, y=430)

    smart_home_button = ctk.CTkButton(root, text="Smart Home", font=("Arial", 15), command=lambda: smart_home_widget())
    smart_home_button.place(x=50, y=530)

    settings_widget = ctk.CTkLabel(root, text="Volume: 50%\nBrightness: 80%", font=("Arial", 15))
    settings_widget.place(x=50, y=630)
    

    # Adjusted position for the "Ask Mirror" button to fit within the display
    ask_mirror_button = ctk.CTkButton(root, text="Ask Mirror", font=("Arial", 20), command=ask_mirror)
    ask_mirror_button.place(x=250, y=630)  # Positioned near the bottom but within the window    


# Changed from 'Start by showing "SMILE"' to start by showing QUOTE
Idle_screen()

root.mainloop()
 
