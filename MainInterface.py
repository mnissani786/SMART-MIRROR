import customtkinter as ctk
import time
import calendar
from API_Data import *
from itertools import count
import math
from PIL import Image, ImageTk
import imageio  # For video playback
from goveeTest import *
import asyncio
from VoiceAgent import ConversationManager
from Vivi import ViviAnimation
from Smile import SmileAnimation
from event_manager import event_manager
from smarthome import SmartHome
import musicTest
from musicTest import MusicPlayer 

# Utility Classes
class AnimatedGIF:
    def __init__(self, gif_path, size):
        self.gif = Image.open(gif_path)
        self.frames = []
        self.size = size

        # Extract all frames from the GIF
        try:
            for frame in count(0):
                self.gif.seek(frame)
                frame_image = self.gif.copy().resize(self.size, Image.Resampling.LANCZOS)
                self.frames.append(ImageTk.PhotoImage(frame_image))
        except EOFError:
            pass

        self.current_frame = 0

    def get_next_frame(self):
        frame = self.frames[self.current_frame]
        self.current_frame = (self.current_frame + 1) % len(self.frames)
        return frame

# Constants and Global Variables
inactivity_timeout = 30  # seconds
turn_off_timeout = 30  # seconds after inactivity
last_activity_time = time.time()

# Function to activate the smart home
def activate_smart_home():
    global smarthome
    smarthome = SmartHome(root)  # Create an instance of the SmartHome class

def deactivate_smart_home():
    global smarthome
    if smarthome:
        smarthome.close_widget()
        smarthome = None  # Set to None to indicate it's closed
    # find a way to destroy/hide the smarthome widget.


# Register music-related events
def play_music():
    handle_music_widget_action("play", music_label)

def pause_music():
    handle_music_widget_action("pause", music_label)

def skip_music():
    handle_music_widget_action("skip", music_label)

def shuffle_music():
    handle_music_widget_action("shuffle", music_label)

def open_music_widget():
    music_widget()  # Open the music widget

def close_music_widget():
    global music_widget_frame
    if music_widget_frame is not None:
        music_widget_frame.place_forget()  # Hide the frame
        music_widget_frame = None  # Reset the global variable

# Register events with the event manager
event_manager.register_event("music_play", play_music)
event_manager.register_event("music_pause", pause_music)
event_manager.register_event("music_skip", skip_music)
event_manager.register_event("music_shuffle", shuffle_music)
event_manager.register_event("open_music_widget", open_music_widget)
event_manager.register_event("close_music_widget", close_music_widget)


def activate_music():
    global music_player
    music_player = MusicPlayer(root)  # Create an instance of the MusicPlayer class

event_manager.register_event("smart_home_activate", activate_smart_home)
event_manager.register_event("smart_home_deactivate", deactivate_smart_home)

# Initialize the conversation manager with the smart home activation callback
conversation_manager = ConversationManager()

# Function to start the conversation manager in the background
async def start_conversation():
    await conversation_manager.main()

# Function to integrate asyncio with the tkinter main loop
def run_asyncio_loop():
    loop = asyncio.get_event_loop()
    loop.create_task(start_conversation())  # Run the conversation manager as a background task

    # Periodically run the asyncio event loop while keeping the GUI responsive
    def poll():
        loop.stop()  # Stop the loop if it's already running
        loop.run_forever()  # Run the asyncio loop
        root.after(100, poll)  # Schedule the next poll

    root.after(100, poll)  # Start polling

# Initialize the main window
ctk.set_appearance_mode("dark")  # Optional: Dark mode
ctk.set_default_color_theme("blue")  # Optional: Default theme

# Making a hashmap that stores the positions and sizes of the widgets and fonts
size = {
    "screen_width": 1080,
    "screen_height": 1920,
    "font_size": 72,
    "font_wrapLength": 1000,
    "weather_symbol_size": 160,
    "weather_symbol_x": 900,
    "weather_symbol_y": 110,
    "clock_start_y": 960,
    "clock_end_y": 549,
    "todo_frame_x": 324,
    "todo_frame_y": 631,
    "calendar_x": 108,
    "calendar_y": 137,
    "calendar_content_y": 219,
    "weather_x": 540,
    "weather_y": 137,
    "weather_content_y": 329,
    "todo_x": 108,
    "todo_y": 549,
    "todo_content_y": 631,
    "music_x": 108,
    "music_y": 1097,
    "music_content_y": 1180,
    "smart_home_x": 108,
    "smart_home_y": 1454,
    "settings_x": 108,
    "settings_y": 1646,
    "settings_content_y": 1728,
    "label_font_size": 48,
    "ask_mirror_x": 540,
    "ask_mirror_y": 1728,
    "vivi_x": 800,
    "vivi_y": 1728
}

Small = True  # Flag to determine if small mode is enabled

if Small:
    size = {key: math.floor(value / 2) for key, value in size.items()}  # Halve the values for small mode

root = ctk.CTk()
# uncomment the line below this to get the title bar back
#root.overrideredirect(True)
root.title("Reflective Assistant")
root.geometry(f"{size['screen_width']}x{size['screen_height']}")

#setting the background to actually be black
root.configure(fg_color="#000000")

# Start the asyncio loop alongside the GUI
run_asyncio_loop()

# variables for Maria's code
news = str(news_list)
curr_temp = str(temp) + "° C"
cloudy = "Cloud Coverage: " + str(clouds) +"% "
wind_speed = "Wind Speed: " + str(wind_mph) + "mph"
humidity = "Humidity:" + str(humid) + "%"
High = "H: " + str(high_temp) + " || "
Low = "L: " + str(low_temp)
sunrisetime = "🌅 Sunrise: " + str(sunrisetime) + " EST"
sunsettime = "🌇 Sunset: " + str(sunsettime) + " EST"

# Create a label to display the current song (used in the music widget)
music_label = ctk.CTkLabel(root, text="No song playing", font=("Arial", 24), text_color="white", fg_color="black")


# Sample list of tasks for the To-Do widget
tasks = [
    "1. Study",
    "2. Work on Project",
    "3. Exercise",
    "4. Read a book",
    "5. Attend meeting"
]

# Create the clock label
clock = ctk.CTkLabel(root, font=("Aptos (Body)", size["font_size"]), text_color="white", fg_color="#000000")
clock.place(x=size["screen_width"]/2, y=size["screen_height"]/2, anchor="center")  # Exactly in the center of the screen

updating = False  # Flag to control time updates

# Place quote on screen
Quote_write = ctk.CTkLabel(root, text="", font=("Aptos (Body)", size["font_size"]), text_color="white", fg_color="#000000", wraplength=size["font_wrapLength"])
Quote_write.place(x=size["screen_width"]/2, y=size["screen_height"]/2, anchor="center")

# Inactivity functions
def reset_inactivity_timer(event=None):
    global last_activity_time
    last_activity_time = time.time()
    if Quote_write.cget("text") != "":
        Quote_write.configure(text="")
        show_widgets()
        update_time()

root.bind("<Motion>", reset_inactivity_timer)
root.bind("<KeyPress>", reset_inactivity_timer)

def hide_all_widgets():
    for widget in root.winfo_children():
        if widget != Quote_write:
            widget.place_forget()

def check_inactivity():
    global last_activity_time
    if time.time() - last_activity_time > inactivity_timeout:
        hide_all_widgets()
        Quote_write.configure(text=str(quote))
        root.after(turn_off_timeout * 1000, root.quit)
    root.after(1000, check_inactivity)

check_inactivity()


# Idle screen
def Idle_screen():
    hide_all_widgets()  # Hide all widgets at startup
    Quote_write.configure(text=str(quote))
    root.after(5000, show_smile)  # Show smile animation after 5 seconds

#symbol for cloudyness
def place_sym():
    weather_sym = ctk.CTkImage(dark_image= Image.open(weather_symbol), size= (size["weather_symbol_size"], size["weather_symbol_size"]))
    Wsym_label = ctk.CTkLabel(root, image=weather_sym, text="")
    Wsym_label.place(x=size["weather_symbol_x"], y=size["weather_symbol_y"])

# Function to show "SMILE" first
def show_smile():
    Quote_write.configure(text="")  # Removes quote from screen (need to improve technique for this)
    smile_animation = SmileAnimation(root, "smile.gif", width=size["screen_width"], height=size["screen_height"], frame_delay=200, x=0, y=0)
    
    def remove_smile_animation():
        smile_animation.label.destroy()
    
    root.after(3000, remove_smile_animation)  # Remove smile animation after 3 seconds
    root.after(3000, start_clock)  # After 10 seconds, show date and time

# Function to start showing date and time
def start_clock():
    global updating
    updating = True  # Enable updating
    update_time()
    root.after(3000, move_clock_up, size["clock_start_y"])  # Move clock up after 3 seconds

# Function to update time (only if updating is enabled)
def update_time():
    if updating:
        current_time = time.strftime("%I:%M %p")
        current_date = time.strftime("%B %d")
        clock.configure(text=f"{current_time}\n{current_date}")
        clock.after(1000, update_time)  # Keep updating every second

widgets_shown = False

# Function to move the clock up smoothly from y=350 to y=200
def move_clock_up(y):
    global updating, widgets_shown
    updating = False  # Stop updating during movement to prevent flickering
    if y > size["clock_end_y"]:
        clock.place(y=y-1)
        root.after(5, move_clock_up, y-1)
    else:
        updating = True  # Resume updates after movement
        update_time()
        if widgets_shown == False:
            show_widgets()
            place_sym()
            widgets_shown = True

# Function to handle "Ask Mirror" button click
def ask_mirror():
    ask_mirror_button.configure(text="Listening...")  # Change button text
    ask_mirror_button.update_idletasks()  # Update the button text immediately
    ask_mirror_button.configure(text="Ask Mirror")  # Restore button text
    print("Ask Mirror Clicked!")

def create_smart_home_widget():
    smarthome = SmartHome(root)  # Create an instance of the SmartHome class
    # selection_box_commands(smarthome.frame, 0, 1)

def close_widget(frame):
    frame.place_forget()

# Creates a new music player that runs in the background
newPlayer = musicTest.MusicPlayer()

def handle_music_widget_action(cmd, songLabel):
    current_song = newPlayer.main(cmd)
    songLabel.configure(text=current_song)

music_widget_frame = None

def music_widget():
    global music_widget_frame
    if music_widget_frame is not None:
        return
    
    music_widget_frame = ctk.CTkFrame(master=root, width = 500, height=500, fg_color="black", border_width=3, border_color="white")
    music_widget_frame.place(relx=.5, rely=.5, anchor="center", bordermode = 'outside')

    for i in range(2):
        music_widget_frame.rowconfigure(i, weight=1)
    for i in range(3):
        music_widget_frame.columnconfigure(i, weight=1)

    songLabel = ctk.CTkLabel(music_widget_frame, text=newPlayer.currentFile, font=("Arial", 24), text_color="white", fg_color="black")
    closeWindow = ctk.CTkButton(music_widget_frame, text="X", font=("Arial", 24), text_color="white", fg_color="black", width=20, command=lambda: close_music_widget)
    shuffleButton = ctk.CTkButton(music_widget_frame, text="Shuffle", font=("Arial", 20), text_color="white", fg_color="black", width=20, command=lambda: handle_music_widget_action("shuffle", songLabel))
    skipButton = ctk.CTkButton(music_widget_frame, text="Skip", font=("Arial", 20), text_color="white", fg_color="black", width=20, command=lambda: handle_music_widget_action("skip", songLabel))
    pauseButton = ctk.CTkButton(music_widget_frame, text="Pause", font=("Arial", 20), text_color="white", fg_color="black", width=20, command=lambda: handle_music_widget_action("pause", songLabel))

    songLabel.grid(column = 0, row = 0, columnspan = 3, pady = 3, padx = 13)
    closeWindow.grid(column = 3, row = 0, pady = 3, padx = 3)
    shuffleButton.grid(column = 0, row = 1, pady = 3, padx = 3)
    skipButton.grid(column = 1, row = 1, pady = 3, padx = 3)
    pauseButton.grid(column = 2, row = 1, pady = 3, padx = 3) 

    # selection_box_commands(frame, 0, 1)  

def move_selection_box(frame, currentCol, currentRow, nextCol, nextRow):    
    nextWidget = frame.grid_slaves(row=nextRow, column=nextCol)    # locates the widget using corresponding row and column, returns a list
    nextWidget[0].configure(border_width=3, border_color='white')   # Accesses first widget in the list and turns the border white

    currentWidget = frame.grid_slaves(row=currentRow, column=currentCol) # Locates the current selected widget
    currentWidget[0].configure(border_width=3, border_color='black')  # Changes the border to black

    return currentCol, currentRow, nextCol, nextRow, nextWidget  #returns updated variables

# Function to ask the user to enter a command for the selection box
def selection_box_commands(frame, col, row):

    currentCol = col
    currentRow = row
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
                nextRow = currentRow
                currentCol, currentRow, nextCol, nextRow, currentSelectedWidget = move_selection_box(frame, currentCol, currentRow, nextCol, nextRow)
                currentCol = nextCol
            except:
                if (nextCol < 0): 
                    print(f"Out of grid range")

        elif(command == 'right' or command == 'r'):
            print(f"Command entered: right")
            try:
                nextCol = currentCol +1  # moves selection to right column
                nextRow = currentRow
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
            close_widget(frame)
            break

        else:
            print(f"not a command")   

# Function to show/hide the To-Do list mini-screen
def toggle_todo_list():
    if todo_frame.winfo_ismapped():  # If mini-screen is visible, hide it
        todo_frame.place_forget()
    else:
        todo_frame.place(x=size["todo_frame_x"], y=size["todo_frame_y"])  # Display the mini-screen to the right of the "To-Do List" widget
        todo_frame.lift()  # Bring the mini-screen to the front

# Function to hide the To-Do mini-screen when clicking on the main window
def hide_todo_list(event):
    if todo_frame.winfo_ismapped():  # Only hide if it is currently visible
        todo_frame.place_forget()

for i in range(3):
    root.grid_columnconfigure(i, weight=1)
for i in range(3):
    root.grid_rowconfigure(i, weight=1)
    
def exit_news():
    news_frame.grid_forget()
    news_frame.place_forget()
    global shown
    shown = False  # Reset the shown flag
    clock.place(x=250, y=200, anchor="center")  # Restore the clock
    show_widgets()  # Restore widgets

def weather_exit():
    weather_frame.grid_forget()
    weather_frame.place_forget()
    global shown
    shown = False  # Reset the shown flag
    clock.place(x=250, y=200, anchor="center")  # Restore the clock
    show_widgets()  # Restore widgets

def news_screen():
    hide_all_widgets()  # Hide all widgets
    news_frame.place(relx=0.5, y=0, anchor="n")  # Top right
    news_frame.grid_columnconfigure(0, weight=1)
    news_frame.grid_rowconfigure(0, weight=1)
    news_frame.grid_rowconfigure(1, weight=1)
    new_display.grid(column=0, row=1, padx=20, pady=20, sticky='nw')
    news_close.grid(column=0, row=0)

def weather_screen():
    hide_all_widgets()  # Hide all widgets
    weather_frame.place(relx=0.5, y=0, anchor="n")  # Top center
    for i in range(2):
        weather_frame.grid_columnconfigure(i, weight=1)
    for i in range(8):  # Adjusted to fit sunrise and sunset rows
        weather_frame.grid_rowconfigure(i, weight=1)
    Wsym_label.grid(column = 0, row = 1, padx = 3, pady = 3)
    tempLabel.grid(column = 1, row = 1, padx = 3, pady = 3)
    cloudLabel.grid(column = 0, row = 3, padx = 20, pady = 20, sticky = 'w', columnspan = 2)
    windLabel.grid(column = 0, row = 4, padx = 20, pady = 20, sticky = 'w', columnspan = 2)
    humidLabel.grid(column = 0, row = 5, padx = 20, pady = 20, sticky = 'w', columnspan = 2)
    Low_HighLabel.grid(column = 1, row = 2, padx = 10, pady = 10, sticky = 'n', columnspan = 2)
    #LowLabel.grid(column = 0, row = 2, padx = 20, pady = 20, sticky = 'ne')
    weather_close.grid(column = 0, row = 0, padx = 20, pady = 20, sticky = 'ne')
    riseLabel.grid(column = 0, row = 6, padx = 20, pady = 20, sticky = 'w', columnspan =2)
    setLabel.grid(column = 0, row = 7, padx = 20, pady = 20, sticky = 'w', columnspan =2)

news_frame = ctk.CTkScrollableFrame(master=root, width=500, height= 700, fg_color= 'black')
weather_frame = ctk.CTkFrame(master=root, width=500, height= 700, fg_color= 'black')
sample_text = ctk.CTkLabel(root,text = "this is the main screen",font = ("Aptos (Body)", 20), text_color = "white", wraplength= 425)
news_pic = ctk.CTkImage(dark_image= Image.open(news_pic), size= (80,80))
news_open = ctk.CTkButton(root, image = news_pic, text="", command=news_screen, fg_color= "transparent", width= 80, height= 80)
news_close = ctk.CTkButton(news_frame, text="Close News", command=exit_news)
weather_icon = ctk.CTkImage(dark_image= Image.open(weather_symbol), size= (80,80))
weather_open = ctk.CTkButton(root, image = weather_icon, text = "", command=weather_screen, width= 80, height= 80, fg_color= "transparent")
weather_close = ctk.CTkButton(weather_frame, text="Exit", command=weather_exit)

new_display = ctk.CTkLabel(news_frame,text = news,font = ("Aptos (Body)", 20), text_color = "white", wraplength= 450, anchor= 'w')
weather_sym = ctk.CTkImage(dark_image= Image.open(weather_symbol), size= (210,210))
Wsym_label = ctk.CTkLabel(weather_frame, image=weather_sym, text="")
tempLabel = ctk.CTkLabel(weather_frame, text = curr_temp, font = ("Times New Roman", 30), text_color = "white", fg_color= "black")
cloudLabel = ctk.CTkLabel(weather_frame, text = cloudy, font = ("Times New Roman", 25), text_color = "white", fg_color= "black")
windLabel = ctk.CTkLabel(weather_frame, text = wind_speed, font = ("Times New Roman", 25), text_color = "white", fg_color= "black")
humidLabel = ctk.CTkLabel(weather_frame, text = humidity, font = ("Times New Roman", 25), text_color = "white", fg_color= "black")
Low_HighLabel = ctk.CTkLabel(weather_frame, text = High + Low, font = ("Times New Roman", 25), text_color = "white", fg_color= "black")
#LowLabel = ctk.CTkLabel(weather_frame, text = Low, font = ("Times New Roman", 25), text_color = "white", fg_color= "black")
riseLabel = ctk.CTkLabel(weather_frame, text = sunrisetime, font = ("Times New Roman", 25), text_color = "white", fg_color= "black")
setLabel = ctk.CTkLabel(weather_frame, text = sunsettime, font = ("Times New Roman", 25), text_color = "white", fg_color= "black")

# Load animated GIFs with resized dimensions
calendar_gif = AnimatedGIF("images/calendar.gif", size=(80, 80))
todo_gif = AnimatedGIF("images/todolist2.gif", size=(80, 80))
settings_gif = AnimatedGIF("images/settings.gif", size=(80, 80))
smart_home_gif = AnimatedGIF("images/Smarthome.gif", size=(80, 80))

# Load static PNG with resized dimensions
music_icon = ctk.CTkImage(dark_image=Image.open("images/icons96.png"), size=(80, 80))

def update_gif(label, gif):
    frame = gif.get_next_frame()
    label.configure(image=frame)
    label.image = frame
    root.after(100, update_gif, label, gif)  # Adjust the delay (100ms) based on the GIF's frame rate

# List of widgets to display. This makes it easy to initialize the labels all at once
widgets = [
    {"text": "Calendar", "x": size["calendar_x"], "y": size["calendar_y"]},
    {"text": "Weather", "x": size["weather_x"], "y": size["weather_y"]},
    {"text": "To-Do List", "x": size["todo_x"], "y": size["todo_y"]},
    {"text": "Music", "x": size["music_x"], "y": size["music_y"]},
    {"text": "Settings", "x": size["settings_x"], "y": size["settings_y"]},
]

precreated_widgets = {}
for widget in widgets:
    precreated_widgets[widget["text"]] = ctk.CTkLabel(
        root, text=widget["text"], font=("Arial", size["label_font_size"]), text_color="white"
    )

# Create widgets once
calendar_widget = ctk.CTkLabel(root, text=calendar.month_name[time.localtime().tm_mon], font=("Arial", size["label_font_size"]))
update_gif(calendar_widget, calendar_gif)
weather_widget = ctk.CTkLabel(root, text=f"{temp} Degrees Celsius\n{clouds}% Cloudy", font=("Arial", size["label_font_size"]), fg_color=weather_color, text_color="Black")
todo_widget = ctk.CTkLabel(root, text="", font=("Arial", size["label_font_size"]), text_color="white")
update_gif(todo_widget, todo_gif)
music_widget_button = ctk.CTkButton(root, text="", image=music_icon, font=("Arial", size["label_font_size"]), command=lambda: music_widget())
smart_home_button = ctk.CTkButton(root, text="", image=smart_home_gif.frames[0], font=("Arial", size["label_font_size"]), command=lambda: create_smart_home_widget())
update_gif(smart_home_button, smart_home_gif)  # Animate the GIF
settings_widget = ctk.CTkLabel(root, text="", font=("Arial", size["label_font_size"]))
update_gif(settings_widget, settings_gif)
ask_mirror_button = ctk.CTkButton(root, text="Say 'Hey Vivi!'", font=("Arial", size["label_font_size"]), command=ask_mirror)

weather_open.place(x=420, y=50)
news_open.place(x=420, y=150)

# Function to show widgets using CustomTkinter
def show_widgets():
    # updated code so widgets arent re-initialized over and over again. The reason
    # everything was taking so long before is that every time show_widgets() was
    # called, it was re-initializing the widgets. Now, the widgets are only initialized
    # once and then updated as needed.
        
    global shown
    shown = False
    if not shown:  # Only place widgets if they haven't been shown yet
        for widget in widgets:
            label = precreated_widgets[widget["text"]]
            label.place(x=widget["x"], y=widget["y"])  # Place pre-created widgets

        # Place other widgets
        calendar_widget.place(x=size["calendar_x"], y=size["calendar_content_y"])
        weather_widget.place(x=size["weather_x"], y=size["weather_content_y"])
        todo_widget.place(x=size["todo_x"], y=size["todo_content_y"])
        music_widget_button.place(x=size["music_x"], y=size["music_content_y"])
        smart_home_button.place(x=size["smart_home_x"], y=size["smart_home_y"])
        settings_widget.place(x=size["settings_x"], y=size["settings_content_y"])
        ask_mirror_button.place(x=size["ask_mirror_x"], y=size["ask_mirror_y"])
        vivi_animation = ViviAnimation(root, "ViviAnimation.gif", width=75, height=75, frame_delay=50, x=size["vivi_x"], y=size["vivi_y"])

        shown = True

# Mini-screen for the To-Do List (Initially hidden)
todo_frame = ctk.CTkFrame(root, width=432, height=823, fg_color="black")  # Adjust width to suit the content
todo_canvas = ctk.CTkCanvas(todo_frame, width=180, height=768, bg='black')  # A canvas for scrolling
todo_scrollbar = ctk.CTkScrollbar(todo_frame, orientation="vertical", command=todo_canvas.yview)
todo_scrollbar.pack(side="right", fill="y")
todo_canvas.pack(side="left", fill="both", expand=True)
todo_canvas.configure(yscrollcommand=todo_scrollbar.set)

# Scrollable content inside the mini-screen
todo_inner_frame = ctk.CTkFrame(todo_canvas)
todo_inner_frame_id = todo_canvas.create_window((0, 0), window=todo_inner_frame, anchor="nw")

# Insert tasks into the scrollable frame as labels
for task in tasks:
    task_label = ctk.CTkLabel(todo_inner_frame, text=task, font=("Arial",28))
    task_label.pack(pady=5, padx=10, anchor="w")  # Anchor to the left side for alignment

# Update scroll region to support scrolling
def update_scroll_region(event):
    todo_canvas.configure(scrollregion=todo_canvas.bbox("all"))

todo_inner_frame.bind("<Configure>", update_scroll_region)

# Initially hide the mini-screen
todo_frame.place_forget()

# Bind a click event on the main window to hide the To-Do mini-screen
root.bind("<Button-1>", hide_todo_list)

# Changed from 'Start by showing "SMILE"' to start by showing QUOTE
Idle_screen()

root.mainloop()
