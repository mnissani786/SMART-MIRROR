import customtkinter as ctk
import time
import calendar
from API_Data import temp
from API_Data import weather_color
from API_Data import clouds
from API_Data import quote
from PIL import Image, ImageTk
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
clock.grid(row=3, column=1, padx=10, pady=10, sticky="nsew")

updating = False  # Flag to control time updates

# Place quote on screen
Quote_write = ctk.CTkLabel(root, text="", font=("Aptos (Body)", 30), text_color="white", wraplength=450)
Quote_write.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

# New Idle screen
def Idle_screen():
    Quote_write.configure(text=str(quote))
    root.after(5000, show_smile)  # After 10 seconds, show SMILE

#symbol for cloudyness
def place_sym():
    weather_sym = ctk.CTkImage(dark_image= Image.open(weather_sym), size=(80,80))
    Wsym_label = ctk.CTkLabel(root, image=weather_sym, text="")
    Wsym_label.grid(row=1, column=2, padx=10, pady=10, sticky="nsew")

# Function to show "SMILE" first
def show_smile():
    Quote_write.configure(text="")  # Removes quote from screen (need to improve technique for this)
    play_gif()
    root.after(5000, start_clock)  # After 10 seconds, show date and time

# Function to play GIF before showing widgets
def play_gif():
    gif_label = ctk.CTkLabel(root, text="")  # Create a label to hold the GIF frames
    gif_label.grid(row=0, column=0, rowspan=8, columnspan=3, padx=10, pady=10, sticky="nsew")

    # Load the GIF file
    gif_path = "neon 1092 tragif.gif"  # Replace this with the path to your GIF
    gif = Image.open(gif_path)
    
    # Get frames from the GIF
    frames = []
    try:
        while True:
            frames.append(ImageTk.PhotoImage(gif.copy().resize((500, 700), Image.Resampling.LANCZOS)))
            gif.seek(len(frames))  # Move to the next frame
    except EOFError:
        pass  # No more frames

    # Cycle through frames
    def update_gif(frame_index):
        gif_label.configure(image=frames[frame_index])  # Set the current frame
        gif_label.image = frames[frame_index]  # Prevent garbage collection
        root.after(100, update_gif, (frame_index + 1) % len(frames))  # Loop through frames

    update_gif(0)  # Start displaying the GIF

    # After the GIF finishes, remove it and show widgets
    root.after(5000, gif_label.destroy)  # Adjust time according to GIF duration

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
        place_sym()

# Function to handle "Ask Mirror" button click
def ask_mirror():
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

# Function to hide the To-Do mini-screen when clicking on the main window
def hide_todo_list(event):
    if todo_frame.winfo_ismapped():  # Only hide if it is currently visible
        todo_frame.place_forget()

for i in range(3):  # 3 columns
        root.columnconfigure(i, weight=1)
for j in range(8):  # 8 rows
        root.rowconfigure(j, weight=1)
# Function to show widgets using CustomTkinter
def show_widgets():
    widgets = [
        {"text": "Calendar", "row": 0, "col": 0},
        {"text": "Weather", "row": 0, "col": 1},
        {"text": "To-Do List", "row": 1, "col": 0},
        {"text": "Music", "row": 2, "col": 0},
        {"text": "Settings", "row": 3, "col": 0},
    ]

    for widget in widgets:
        label = ctk.CTkLabel(root, text=widget["text"], font=("Arial", 20), text_color="white")
        label.grid(row=widget["row"], column=widget["col"], padx=10, pady=10, sticky="nsew")

    # Creating functional widgets with adjusted coordinates
    calendar_widget = ctk.CTkLabel(root, text=calendar.month_name[time.localtime().tm_mon], font=("Arial", 15))
    calendar_widget.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

    #weather_widget = ctk.CTkLabel(root, text="Sunny, 25°C", font=("Arial", 15))
    #updated weather widget
    weather_widget = ctk.CTkLabel(root, text= str(temp) + " Degrees Celsius\n" + str(clouds) + "% Cloudy", font=("Arial", 15), fg_color= weather_color, text_color= ("Black"))
    weather_widget.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

    # To-Do List Widget with click-to-expand functionality
    todo_widget = ctk.CTkLabel(root, text="1. Study\n2. Work on Project\n3. Exercise", font=("Arial", 15), text_color="white")
    todo_widget.pack(pady=10, padx=20, anchor="w")  # Left-align with padding
    todo_widget.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
    todo_widget.bind("<Button-1>", lambda e: toggle_todo_list())  # Make the To-Do list clickable

    # Music widget
    music_widget = ctk.CTkLabel(root, text="Playing: Song XYZ", font=("Arial", 15))
    music_widget.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")

    smart_home_button = ctk.CTkButton(root, text="Smart Home", font=("Arial", 15), command=lambda: smart_home_widget())
    smart_home_button.grid(row=3, column=0, padx=10, pady=10, sticky="nsew")

    # Settings widget
    settings_widget = ctk.CTkLabel(root, text="Volume: 50%\nBrightness: 80%", font=("Arial", 15))
    settings_widget.grid(row=4, column=0, padx=10, pady=10, sticky="nsew")

    # "Ask Mirror" button
    ask_mirror_button = ctk.CTkButton(root, text="Ask Mirror", font=("Arial", 20), command=ask_mirror)
    ask_mirror_button.grid(row=7, column=1, padx=10, pady=10, sticky="nsew")

# Mini-screen for the To-Do List (Initially hidden)
todo_frame = ctk.CTkFrame(root, width=200, height=300)  # Adjust width to suit the content
todo_canvas = ctk.CTkCanvas(todo_frame, width=180, height=280)  # A canvas for scrolling
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
