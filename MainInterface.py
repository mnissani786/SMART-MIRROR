import customtkinter as ctk
import time
import calendar
from API_Data import temp, weather_color, clouds, quote, weather_symbol
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

# New Idle screen
def Idle_screen():
    Quote_write.configure(text=str(quote))
    root.after(5000, show_smile)  # After 10 seconds, show SMILE

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
    get_audio()
    ask_mirror_button.configure(text="Ask Mirror")  # Restore button text
    print("Ask Mirror Clicked!")

def create_smart_home_widget():
    smarthome = SmartHome(root)  # Create an instance of the SmartHome class

def close_widget(frame):
    frame.place_forget()

# Creates a new music player that runs in the background
newPlayer = musicTest.MusicPlayer()

# Function to show music UI
def music_widget():
    frame = ctk.CTkFrame(master=root, width = 500, height=500, fg_color="black", border_width=3, border_color="white")
    frame.place(relx=.5, rely=.5, anchor="center", bordermode = 'outside')
    for i in range(2):
        frame.rowconfigure(i, weight=1)
    for i in range(3):
        frame.columnconfigure(i, weight=1)

    songLabel = ctk.CTkLabel(frame, text=newPlayer.currentFile, font=("Arial", 24), text_color="white", fg_color="black")
    closeWindow = ctk.CTkButton(frame, text="X", font=("Arial", 24), text_color="white", fg_color="black", width=20, command=lambda: close_widget(frame))
    shuffleButton = ctk.CTkButton(frame, text="Shuffle", font=("Arial", 20), text_color="white", fg_color="black", width=20, command=lambda: newPlayer.main("shuffle"))
    skipButton = ctk.CTkButton(frame, text="Skip", font=("Arial", 20), text_color="white", fg_color="black", width=20, command=lambda: newPlayer.main("skip"))
    pauseButton = ctk.CTkButton(frame, text="Pause", font=("Arial", 20), text_color="white", fg_color="black", width=20, command=lambda: newPlayer.main("pause"))

    songLabel.grid(column = 0, row = 0, columnspan = 3, pady = 3, padx = 13)
    closeWindow.grid(column = 3, row = 0, pady = 3, padx = 3)
    shuffleButton.grid(column = 0, row = 1, pady = 3, padx = 3)
    skipButton.grid(column = 1, row = 1, pady = 3, padx = 3)
    pauseButton.grid(column = 2, row = 1, pady = 3, padx = 3)   

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
weather_widget = ctk.CTkLabel(root, text=f"{temp} Degrees Celsius\n{clouds}% Cloudy", font=("Arial", size["label_font_size"]), fg_color=weather_color, text_color="Black")
todo_widget = ctk.CTkLabel(root, text="1. Study\n2. Work on Project\n3. Exercise", font=("Arial", size["label_font_size"]), text_color="white")
# todo_widget.pack(pady=10, padx=20, anchor="w")  # Left-align with padding
todo_widget.bind("<Button-1>", lambda e: toggle_todo_list())  # Make the To-Do list clickable
music_widget_button = ctk.CTkButton(root, text="Playing: Song XYZ", font=("Arial", size["label_font_size"]), command=lambda: music_widget())
smart_home_button = ctk.CTkButton(root, text="Smart Home", font=("Arial", size["label_font_size"]), command=lambda: create_smart_home_widget())
settings_widget = ctk.CTkLabel(root, text="Volume: 50%\nBrightness: 80%", font=("Arial", size["label_font_size"]))
ask_mirror_button = ctk.CTkButton(root, text="Say 'Hey Vivi!'", font=("Arial", size["label_font_size"]), command=ask_mirror)

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
        vivi_animation = ViviAnimation(root, "ViviAnimation.gif", width=75, height=75, frame_delay=50, x=200, y=200)

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
