import customtkinter as ctk
import tkinter as tk
from datetime import datetime
import random
import requests
from PIL import Image, ImageTk
import io
import threading
import time

# Set appearance mode and default color theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class SmartMirror(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Configure window
        self.title("Smart Mirror")
        self.geometry("500x700")
        self.configure(fg_color="black")
        
        # Configure grid layout (4 rows x 1 column)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure((0, 1, 2, 3), weight=1)
        
        # Initialize variables
        self.weather_temp = tk.StringVar(value="-- °C")
        self.weather_condition = tk.StringVar(value="Loading...")
        self.time_string = tk.StringVar(value="00:00")
        self.date_string = tk.StringVar(value="Loading...")
        self.quote_string = tk.StringVar(value="Loading inspiration...")
        
        # Sample todo items
        self.todo_items = [
            {"text": "Morning workout", "completed": False},
            {"text": "Team meeting at 10 AM", "completed": False},
            {"text": "Pick up groceries", "completed": False},
            {"text": "Call mom", "completed": True}
        ]
        
        # Sample quotes
        self.quotes = [
            "The best way to predict the future is to create it.",
            "Success is not final, failure is not fatal: It is the courage to continue that counts.",
            "The only way to do great work is to love what you do.",
            "Believe you can and you're halfway there.",
            "It does not matter how slowly you go as long as you do not stop."
        ]
        
        # Create frames
        self.create_header_frame()
        self.create_weather_frame()
        self.create_todo_frame()
        self.create_quote_frame()
        
        # Start update threads
        self.start_update_threads()
    
    def create_header_frame(self):
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=(20, 10))
        
        header_frame.grid_rowconfigure((0, 1, 2), weight=1)
        header_frame.grid_columnconfigure(0, weight=1)
        
        # Greeting label
        greeting_label = ctk.CTkLabel(
            header_frame,
            text="Hello, Beautiful!",
            font=ctk.CTkFont(family="Helvetica", size=32, weight="bold"),
            text_color="white"
        )
        greeting_label.grid(row=0, column=0, sticky="nw")
        
        # Time label
        time_label = ctk.CTkLabel(
            header_frame,
            textvariable=self.time_string,
            font=ctk.CTkFont(family="Helvetica", size=48, weight="bold"),
            text_color="white"
        )
        time_label.grid(row=1, column=0, sticky="nw")
        
        # Date label
        date_label = ctk.CTkLabel(
            header_frame,
            textvariable=self.date_string,
            font=ctk.CTkFont(family="Helvetica", size=18),
            text_color="white"
        )
        date_label.grid(row=2, column=0, sticky="nw")
    
    def create_weather_frame(self):
        weather_frame = ctk.CTkFrame(self, fg_color="transparent")
        weather_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)
        
        weather_frame.grid_rowconfigure((0, 1), weight=1)
        weather_frame.grid_columnconfigure((0, 1), weight=1)
        
        # Weather header
        weather_header = ctk.CTkLabel(
            weather_frame,
            text="Current Weather",
            font=ctk.CTkFont(family="Helvetica", size=18, weight="bold"),
            text_color="white"
        )
        weather_header.grid(row=0, column=0, sticky="w")
        
        # Weather info
        weather_info_frame = ctk.CTkFrame(weather_frame, fg_color="transparent")
        weather_info_frame.grid(row=1, column=0, sticky="w")
        
        # Temperature label
        temp_label = ctk.CTkLabel(
            weather_info_frame,
            textvariable=self.weather_temp,
            font=ctk.CTkFont(family="Helvetica", size=36, weight="bold"),
            text_color="white"
        )
        temp_label.pack(side="left", padx=(0, 20))
        
        # Condition label
        condition_label = ctk.CTkLabel(
            weather_info_frame,
            textvariable=self.weather_condition,
            font=ctk.CTkFont(family="Helvetica", size=18),
            text_color="white"
        )
        condition_label.pack(side="left")
    
    def create_todo_frame(self):
        todo_frame = ctk.CTkFrame(self, fg_color="transparent")
        todo_frame.grid(row=2, column=0, sticky="nsew", padx=20, pady=10)
        
        todo_frame.grid_rowconfigure(0, weight=0)  # Header
        todo_frame.grid_rowconfigure(1, weight=1)  # Content
        todo_frame.grid_columnconfigure(0, weight=1)
        
        # Todo header
        todo_header = ctk.CTkLabel(
            todo_frame,
            text="Today's Tasks",
            font=ctk.CTkFont(family="Helvetica", size=18, weight="bold"),
            text_color="white"
        )
        todo_header.grid(row=0, column=0, sticky="w", pady=(0, 10))
        
        # Todo list
        todo_list_frame = ctk.CTkFrame(todo_frame, fg_color="#111111")
        todo_list_frame.grid(row=1, column=0, sticky="nsew")
        
        # Add todo items
        for i, item in enumerate(self.todo_items):
            todo_item_frame = ctk.CTkFrame(todo_list_frame, fg_color="transparent")
            todo_item_frame.pack(fill="x", padx=10, pady=5)
            
            # Checkbox
            checkbox = ctk.CTkCheckBox(
                todo_item_frame,
                text="",
                checkbox_width=20,
                checkbox_height=20,
                fg_color="#555555",
                text_color="white"
            )
            checkbox.pack(side="left", padx=(0, 10))
            
            if item["completed"]:
                checkbox.select()
            
            # Task text
            text_color = "#888888" if item["completed"] else "white"
            task_label = ctk.CTkLabel(
                todo_item_frame,
                text=item["text"],
                font=ctk.CTkFont(family="Helvetica", size=16),
                text_color=text_color
            )
            task_label.pack(side="left", fill="x")
    
    def create_quote_frame(self):
        quote_frame = ctk.CTkFrame(self, fg_color="transparent")
        quote_frame.grid(row=3, column=0, sticky="nsew", padx=20, pady=(10, 20))
        
        quote_frame.grid_rowconfigure((0, 1), weight=1)
        quote_frame.grid_columnconfigure(0, weight=1)
        
        # Quote header
        quote_header = ctk.CTkLabel(
            quote_frame,
            text="Inspiration",
            font=ctk.CTkFont(family="Helvetica", size=18, weight="bold"),
            text_color="white"
        )
        quote_header.grid(row=0, column=0, sticky="sw")
        
        # Quote text
        quote_label = ctk.CTkLabel(
            quote_frame,
            textvariable=self.quote_string,
            font=ctk.CTkFont(family="Helvetica", size=16, slant="italic"),
            text_color="white",
            wraplength=460
        )
        quote_label.grid(row=1, column=0, sticky="nw")
    
    def update_clock(self):
        while True:
            now = datetime.now()
            self.time_string.set(now.strftime("%H:%M"))
            self.date_string.set(now.strftime("%A, %B %d, %Y"))
            time.sleep(1)
    
    def update_weather(self):
        # Simulating weather API call
        weather_data = {"temp": "22", "condition": "Partly Cloudy"}
        self.weather_temp.set(f"{weather_data['temp']}°C")
        self.weather_condition.set(weather_data['condition'])
    
    def update_quote(self):
        self.quote_string.set(random.choice(self.quotes))
    
    def start_update_threads(self):
        # Update clock
        clock_thread = threading.Thread(target=self.update_clock, daemon=True)
        clock_thread.start()
        
        # Initial updates
        self.update_weather()
        self.update_quote()

if __name__ == "__main__":
    app = SmartMirror()
    app.mainloop()