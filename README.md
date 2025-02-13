import tkinter as tk
import time
#this is making the display size and title of the app
root = tk.Tk()
root.title("Reflective Assistant")
root.geometry("1280x1024")
root.config(bg="black")

#creating the clock display and its position
clock = tk.Label(root, font=("Aptos (Body)", 40), bg="black", fg="white")
clock.pack(pady=20)
clock.place(x=640, y=512, anchor="center")

#this is using the time import to show the clock and date and keep it updated
def update_time():
    current_time = time.strftime("%I:%M:%S %p")
    current_date = time.strftime("%B %d, %Y")
    clock.config(text=f"{current_time}\n{current_date}")
    clock.after(1000, update_time) 

#this is creating the fading animation
def fade_clock(a=255):
    if a > 0:
        fade_color = f'#{a:02x}{a:02x}{a:02x}'
        clock.config(fg=fade_color)
        root.after(50, fade_clock, a - 10)  
    else:
        clock.config(text="SMILE", fg="white")
        root.after(5000, lambda: fade_in_clock(0))


#another fading animation to remove the message and bring clock back
def fade_in_clock(a=0):
    if a < 255:
        fade_color = f'#{a:02x}{a:02x}{a:02x}'
        clock.config(fg=fade_color, text=time.strftime("%I:%M:%S %p"))
        root.after(50, fade_in_clock, a + 10)  
    else:
        move_clock_up(512)



#making the clock widget move up the screen
def move_clock_up(y):
    if y > 200:
        clock.place(y=y-5)
        root.after(50, move_clock_up, y-5)
    
    else:
        show_widgets()

def show_widgets():
    # Create and place all the widgets
    calendar_label = tk.Label(root, text="Calendar", font=("Arial", 20), bg="black", fg="white")
    calendar_label.place(x=0, y=0)

    weather_label = tk.Label(root, text="Weather", font=("Arial", 20), bg="black", fg="white")
    weather_label.place(x=640, y=0)

    todo_label = tk.Label(root, text="To-Do List", font=("Arial", 20), bg="black", fg="white")
    todo_label.place(x=0, y=200)

    music_label = tk.Label(root, text="Music", font=("Arial", 20), bg="black", fg="white")
    music_label.place(x=0, y=400)

    settings_label = tk.Label(root, text="Settings", font=("Arial", 20), bg="black", fg="white")
    settings_label.place(x=0, y=600)

    ask_mirror_button = tk.Button(root, text="Ask Mirror", font=("Arial", 20), bg="black", fg="white", command=ask_mirror)
    ask_mirror_button.place(x=640, y=640)

    
    calendar_widget = tk.Label(root, text=calendar.month_name[time.localtime().tm_mon], font=("Arial", 15), bg="black", fg="white")
    calendar_widget.place(x=0, y=0)

    
    weather_widget = tk.Label(root, text="Sunny, 25°C", font=("Arial", 15), bg="black", fg="white")
    weather_widget.place(x=640, y=0)

    
    todo_widget = tk.Label(root, text="1. Study\n2. Work on Project\n3. Exercise", font=("Arial", 15), bg="black", fg="white")
    todo_widget.place(x=0, y=200)

    
    music_widget = tk.Label(root, text="Playing: Song XYZ", font=("Arial", 15), bg="black", fg="white")
    music_widget.place(x=0, y=400)

    
    settings_widget = tk.Label(root, text="Volume: 50%\nBrightness: 80%", font=("Arial", 15), bg="black", fg="white")
    settings_widget.place(x=0, y=600)

#need to work on trying to mimic the ppt widget and ask mirror function




update_time()

root.after(5000, fade_clock)



root.mainloop()
