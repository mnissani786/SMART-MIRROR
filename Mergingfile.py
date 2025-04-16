# Imports
import customtkinter as ctk
import time
import calendar
from API_Data import temp
from API_Data import weather_symbol
from API_Data import weather_color
from API_Data import clouds, wind_mph, humid, low_temp, high_temp, sunrisetime, sunsettime 
from API_Data import quote, news_pic, news_list
from PIL import Image, ImageTk
import imageio  # For video playback
from goveeTest import *
from itertools import count


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

# Initialize the main window
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

root = ctk.CTk()
root.title("Reflective Assistant")
root.geometry("500x700")

# Inactivity timer setup
news = str(news_list)
curr_temp = str(temp) + "° C"
cloudy = "Cloud Coverage: " + str(clouds) +"% "
wind_speed = "Wind Speed: " + str(wind_mph) + "mph"
humidity = "Humidity:" + str(humid) + "%"
High = "H: " + str(high_temp) + " || "
Low = "L: " + str(low_temp)
sunrisetime = "🌅 Sunrise: " + str(sunrisetime) + " EST"
sunsettime = "🌇 Sunset: " + str(sunsettime) + " EST"

# Create the clock label
clock = ctk.CTkLabel(root, font=("Aptos (Body)", 30), text_color="white")
clock.place(x=250, y=350, anchor="center")

updating = False
shown = False


# Place quote on screen
Quote_write = ctk.CTkLabel(root, text="", font=("Aptos (Body)", 30), text_color="white", wraplength=450)
Quote_write.place(x=250, y=350, anchor="center")

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
    root.after(5000, show_smile)


#symbol for cloudyness
def place_sym():
    weather_sym = ctk.CTkImage(dark_image= Image.open(weather_sym), size= (80,80))
    Wsym_label = ctk.CTkLabel(root, image=weather_sym, text="")
    Wsym_label.place(x=380, y=95)


# Show SMILE first
def show_smile():
    Quote_write.configure(text="")      # Clear the quote
    clock.place_forget()               # <- Hide the clock temporarily
    play_gif()
    root.after(5000, start_clock)      # After the GIF, resume logic



# Play GIF
def play_gif():
    gif_label = ctk.CTkLabel(root, text="")
    gif_label.place(x=0, y=0, relwidth=1, relheight=1)

    gif_path = "neon 1092 tragif.gif"
    animated_gif = AnimatedGIF(gif_path, (500, 700))

    def update_gif():
        gif_label.configure(image=animated_gif.get_next_frame())
        root.after(100, update_gif)

    update_gif()
    root.after(5000, gif_label.destroy)

# Start showing time
def start_clock():
    global updating
    clock.place(x=250, y=350, anchor="center")  # Place the clock at its initial position
    updating = True
    update_time()  # Start updating the time
    root.after(3000, move_clock_up, 350)  # Start moving the clock up after 3 seconds


# Update time
def update_time():
    if updating:
        current_time = time.strftime("%I:%M %p")
        current_date = time.strftime("%B %d")
        clock.configure(text=f"{current_time}\n{current_date}")
        clock.after(1000, update_time)

# Move clock up
def move_clock_up(y):
    global updating
    updating = False
    if y > 200:  # Target position for the clock
        clock.place(x=250, y=y - 1)  # Move the clock up
        root.after(5, move_clock_up, y - 1)  # Continue moving up
    else:
        updating = True
        update_time()
        show_widgets()  # Show widgets after the clock has moved
        place_sym()

# Ask Mirror button
def ask_mirror():
    print("Ask Mirror Clicked!")

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

# Show widgets
def show_widgets():
    global shown  # Track if widgets are already shown

    if not shown:
        # Left-side widgets (aligned vertically)
        # Calendar widget with animated GIF
        calendar_label = ctk.CTkLabel(root, text="")
        calendar_label.place(x=50, y=50)  # Left side, top
        update_gif(calendar_label, calendar_gif)

        # To-Do List widget with animated GIF
        todo_label = ctk.CTkLabel(root, text="")
        todo_label.place(x=50, y=150)  # Left side, below calendar
        update_gif(todo_label, todo_gif)

        # Music widget with static PNG
        music_widget = ctk.CTkButton(root, text="", image=music_icon, fg_color="transparent", width=80, height=80)
        music_widget.place(x=30, y=250)  # Left side, below to-do list

        # Settings widget with animated GIF
        settings_label = ctk.CTkLabel(root, text="")
        settings_label.place(x=50, y=450)  # Left side, below smart home
        update_gif(settings_label, settings_gif)

        # Smart Home Button with animated GIF
        smart_home_button = ctk.CTkButton(
            root,
            text="",
            image=smart_home_gif.frames[0],  # Use the first frame of the GIF
            fg_color="transparent",
            width=80,
            height=80,
            command=smart_home_widget  # Set the command to open the Smart Home widget
        )
        smart_home_button.place(x=35, y=350)  # Left side, below music
        update_gif(smart_home_button, smart_home_gif)  # Animate the GIF

        # Right-side widgets (aligned vertically)
        # Weather icon
        weather_open.place(x=420, y=50)  # Right side, top

        # News icon
        news_open.place(x=420, y=150)  # Right side, below weather

        # Other widgets
        ask_mirror_button = ctk.CTkButton(root, text="Ask Mirror", font=("Arial", 20), command=ask_mirror)
        ask_mirror_button.place(x=250, y=630)

        shown = True
    else:
        for widget in root.winfo_children():
            widget.place_forget()
        shown = False

Idle_screen()

root.mainloop()
