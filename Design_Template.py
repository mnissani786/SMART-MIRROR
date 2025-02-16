import tkinter as tk
import time
from tkinter import *

class App(tk.Tk):
    def __init__(root):
        super().__init__()

        #this is making the display size and title of the app        
        root.title("Reflective Assistant")
        root.geometry("500x700")
        root.config(bg="black")

        #creating the clock display and its position
        clock = tk.Label(root, font=("Aptos (Body)", 40), bg="black", fg="white")
        #clock.pack(pady=20)
        clock.place(relx=.5, rely=.5, anchor="center")

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
            #content = Frame(root, padx=3, pady=3)
            #frame = Frame(root, bg="blue")
            #frame = Frame(root, width=400, height=400, bg="blue")
            #frame.place(relx=.5, rely=.5, relwidth=0.95, relheight=0.95, anchor="center")
            #frame.grid(row=0, column=0, sticky=(N, S, E, W))
            #content.grid(column=0, row=0, sticky=(N, S, E, W))
            #frame.grid(column=0, row=0, columnspan=3, rowspan=2, sticky=(N, S, E, W))            

            #centers the root in the 0,0 grid position with a weight = 1 so it resizes 1:1 to the window
            #root.columnconfigure(0, weight=1)
            #root.rowconfigure(0, weight=1)

            #These configure the rows and columns inside the root so they rezise relative to the window
            for i in range(7): #creates 7 rows that can resize with window
                root.rowconfigure(i, weight=1)
            for i in range(3): #creates 3 columns that can resize with window
                root.columnconfigure(i, weight=1) 

            # Create and place all the widgets
            calendar_label = tk.Label(root, text="Calendar", font=("Arial", 20), bg="black", fg="white")
            #calendar_label.place(x=0, y=0)
            calendar_label.grid(column=0, row=0, sticky=(N,W), padx=25)
            #calendar_label.columnconfigure(0, weight=1)

            weather_label = tk.Label(root, text="Weather", font=("Arial", 20), bg="black", fg="white")
            #weather_label.place(x=300, y=0)
            weather_label.grid(column=1, row=0, sticky=(N, E, S, W), padx=25)

            todo_label = tk.Label(root, text="To-Do List", font=("Arial", 20), bg="black", fg="white")
            #todo_label.place(x=0, y=100)
            todo_label.grid(column=0,row=1, sticky=(N,W), padx=25)

            music_label = tk.Label(root, text="Music", font=("Arial", 20), bg="black", fg="white")
            #music_label.place(x=0, y=200)
            music_label.grid(column=0,row=3, sticky=(W), padx=25)

            clock.grid(row=1,column=1,sticky=(N,S,E,W))

            settings_label = tk.Label(root, text="Settings", font=("Arial", 20), bg="black", fg="white")
            #settings_label.place(x=0, y=300)
            settings_label.grid(column=0,row=7, sticky=(N,W), padx=25, pady=25)

            ask_mirror_button = tk.Button(root, text="Ask Mirror", font=("Arial", 20), bg="black", fg="white") #add    command=ask_mirror  After fg="white"
            #ask_mirror_button.place(x=500, y=500)
            ask_mirror_button.grid(column=1,row=7,sticky=(S),pady=25)
            
            calendar_widget = tk.Label(root, text="Februray", font=("Arial", 15), bg="black", fg="white") #change to     text=calendar.month_name[time.localtime().tm_mon]    when we have calander widget
            #calendar_widget.place(x=0, y=50)
            
            weather_widget = tk.Label(root, text="Sunny, 25°C", font=("Arial", 15), bg="black", fg="white")
            #weather_widget.place(x=300, y=50)
            
            todo_widget = tk.Label(root, text="1. Study\n2. Work on Project\n3. Exercise", font=("Arial", 15), bg="black", fg="white")
            #todo_widget.place(x=0, y=150)
            
            music_widget = tk.Label(root, text="Playing: Song XYZ", font=("Arial", 15), bg="black", fg="white")
            #music_widget.place(x=0, y=250)
            
            settings_widget = tk.Label(root, text="Volume: 50%\nBrightness: 80%", font=("Arial", 15), bg="black", fg="white")
            #settings_widget.place(x=0, y=350)

        update_time()

        root.after(5000, fade_clock)

#need to work on trying to mimic the ppt widget and ask mirror function

if __name__ == "__main__":
    
    App().mainloop()
