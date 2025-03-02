import customtkinter as ctk
import time
import calendar

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

# Function to show "SMILE" first
def show_smile():
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

    weather_widget = ctk.CTkLabel(root, text="Sunny, 25°C", font=("Arial", 15))
    weather_widget.place(x=250, y=120)  # Positioned higher to prevent overlap with the clock

    todo_widget = ctk.CTkLabel(root, text="1. Study\n2. Work on Project\n3. Exercise", font=("Arial", 15))
    todo_widget.place(x=50, y=230)

    music_widget = ctk.CTkLabel(root, text="Playing: Song XYZ", font=("Arial", 15))
    music_widget.place(x=50, y=430)

    settings_widget = ctk.CTkLabel(root, text="Volume: 50%\nBrightness: 80%", font=("Arial", 15))
    settings_widget.place(x=50, y=630)

    # Adjusted position for the "Ask Mirror" button to fit within the display
    ask_mirror_button = ctk.CTkButton(root, text="Ask Mirror", font=("Arial", 20), command=ask_mirror)
    ask_mirror_button.place(x=250, y=630)  # Positioned near the bottom but within the window

# Start by showing "SMILE"
show_smile()

root.mainloop()
