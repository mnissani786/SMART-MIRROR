import customtkinter as ctk
import time
import calendar
from API_Data import temp
from API_Data import weather_color
from API_Data import clouds
from API_Data import quote
from API_Data import weather_symbol
from PIL import Image, ImageTk
from speech import *
import imageio  # For video playback
from goveeTest import *


# Initialize the main window
ctk.set_appearance_mode("dark")  # Optional: Dark mode
ctk.set_default_color_theme("blue")  # Optional: Default theme

root = ctk.CTk()
root.title("Reflective Assistant")
root.geometry("500x700")

# Sample list of tasks for the To-Do widget
tasks = [
    "1. Study",
    "2. Work on Project",
    "3. Exercise",
    "4. Read a book",
    "5. Attend meeting"
]

# Create the clock label
clock = ctk.CTkLabel(root, font=("Aptos (Body)", 30), text_color="white")
clock.place(x=250, y=350, anchor="center")  # Exactly in the center of the screen

updating = False  # Flag to control time updates

# Place quote on screen
Quote_write = ctk.CTkLabel(root, text="", font=("Aptos (Body)", 30), text_color="white", wraplength=450)
Quote_write.place(x=250, y=350, anchor="center")

# New Idle screen
def Idle_screen():
    Quote_write.configure(text=str(quote))
    root.after(5000, show_smile)  # After 10 seconds, show SMILE

#symbol for cloudyness
def place_sym():
    weather_sym = ctk.CTkImage(dark_image= Image.open(weather_symbol), size= (80,80))
    Wsym_label = ctk.CTkLabel(root, image=weather_sym, text="")
    Wsym_label.place(x=380, y=95)

# Function to show "SMILE" first
def show_smile():
    Quote_write.configure(text="")  # Removes quote from screen (need to improve technique for this)
    play_video()
    root.after(16000, start_clock)  # After 10 seconds, show date and time

# Function to play video before showing widgets
def play_video():
    video_label = ctk.CTkLabel(root, text="")  # Create a label to hold video frames
    video_label.place(x=0, y=0, relwidth=1, relheight=1)  # Make video cover full screen

    # Load the video file (use a path to your video file)
    video_path = "Neon Smile.mp4"  # Replace this with the path to your video file
    video = imageio.get_reader(video_path)

    def stream_video():
        for frame in video:
            frame_image = Image.fromarray(frame)  # Convert frame to image
            frame_image = frame_image.resize((500, 700), Image.Resampling.LANCZOS)  # Resize to fit screen
            frame_photo = ImageTk.PhotoImage(frame_image)
            video_label.configure(image=frame_photo)
            video_label.image = frame_photo
            root.update()  # Update the root window
            time.sleep(0.03)  # Control playback speed (~30 fps)

        video_label.destroy()  # Remove video label after playback

    root.after(0, stream_video)

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

widgets_shown = False

# Function to move the clock up smoothly from y=350 to y=200
def move_clock_up(y):
    global updating, widgets_shown
    updating = False  # Stop updating during movement to prevent flickering
    if y > 200:
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

# Function to show/hide the To-Do list mini-screen
def toggle_todo_list():
    if todo_frame.winfo_ismapped():  # If mini-screen is visible, hide it
        todo_frame.place_forget()
    else:
        todo_frame.place(x=150, y=230)  # Display the mini-screen to the right of the "To-Do List" widget
        todo_frame.lift()  # Bring the mini-screen to the front

# Function to hide the To-Do mini-screen when clicking on the main window
def hide_todo_list(event):
    if todo_frame.winfo_ismapped():  # Only hide if it is currently visible
        todo_frame.place_forget()

# List of widgets to display. This makes it easy to initialize the labels all at once
widgets = [
    {"text": "Calendar", "x": 50, "y": 50},
    {"text": "Weather", "x": 250, "y": 50},
    {"text": "To-Do List", "x": 50, "y": 200},
    {"text": "Music", "x": 50, "y": 400},
    {"text": "Settings", "x": 50, "y": 600},
]

precreated_widgets = {}
for widget in widgets:
    precreated_widgets[widget["text"]] = ctk.CTkLabel(
        root, text=widget["text"], font=("Arial", 20), text_color="white"
    )

# Create widgets once
calendar_widget = ctk.CTkLabel(root, text=calendar.month_name[time.localtime().tm_mon], font=("Arial", 15))
weather_widget = ctk.CTkLabel(root, text=f"{temp} Degrees Celsius\n{clouds}% Cloudy", font=("Arial", 15), fg_color=weather_color, text_color="Black")
todo_widget = ctk.CTkLabel(root, text="1. Study\n2. Work on Project\n3. Exercise", font=("Arial", 15), text_color="white")
# todo_widget.pack(pady=10, padx=20, anchor="w")  # Left-align with padding
todo_widget.bind("<Button-1>", lambda e: toggle_todo_list())  # Make the To-Do list clickable
music_widget = ctk.CTkLabel(root, text="Playing: Song XYZ", font=("Arial", 15))
smart_home_button = ctk.CTkButton(root, text="Smart Home", font=("Arial", 15), command=lambda: smart_home_widget())
settings_widget = ctk.CTkLabel(root, text="Volume: 50%\nBrightness: 80%", font=("Arial", 15))
ask_mirror_button = ctk.CTkButton(root, text="Ask Mirror", font=("Arial", 20), command=ask_mirror)

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
        calendar_widget.place(x=50, y=80)
        weather_widget.place(x=250, y=120)
        todo_widget.place(x=50, y=230)
        music_widget.place(x=50, y=430)
        smart_home_button.place(x=50, y=530)
        settings_widget.place(x=50, y=630)
        ask_mirror_button.place(x=250, y=630)

        shown = True

# Mini-screen for the To-Do List (Initially hidden)
todo_frame = ctk.CTkFrame(root, width=200, height=300, fg_color="black")  # Adjust width to suit the content
todo_canvas = ctk.CTkCanvas(todo_frame, width=180, height=280, bg='black')  # A canvas for scrolling
todo_scrollbar = ctk.CTkScrollbar(todo_frame, orientation="vertical", command=todo_canvas.yview)
todo_scrollbar.pack(side="right", fill="y")
todo_canvas.pack(side="left", fill="both", expand=True)
todo_canvas.configure(yscrollcommand=todo_scrollbar.set)

# Scrollable content inside the mini-screen
todo_inner_frame = ctk.CTkFrame(todo_canvas)
todo_inner_frame_id = todo_canvas.create_window((0, 0), window=todo_inner_frame, anchor="nw")

# Insert tasks into the scrollable frame as labels
for task in tasks:
    task_label = ctk.CTkLabel(todo_inner_frame, text=task, font=("Arial", 14))
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
