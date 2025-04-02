import customtkinter as ctk
from datetime import datetime
import random

# Set appearance mode and default color theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

class SmartMirrorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Smart Mirror")
        self.root.geometry("500x700")
        self.root.configure(bg="black")
        
        # Configure grid to make it expandable
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
        # Main frame
        self.main_frame = ctk.CTkFrame(self.root, fg_color="black")
        self.main_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        
        # Configure main frame grid
        for i in range(5):
            self.main_frame.grid_rowconfigure(i, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)
        
        # Create UI elements
        self.create_greeting()
        self.create_weather()
        self.create_day()
        self.create_todo()
        self.create_quote()
        
        # Update dynamic content
        self.update_time()

    def create_greeting(self):
        greeting_frame = ctk.CTkFrame(self.main_frame, fg_color="black")
        greeting_frame.grid(row=0, column=0, sticky="nsew", pady=(0, 10))
        
        self.time_label = ctk.CTkLabel(
            greeting_frame,
            text="12:00",
            font=("Helvetica", 40, "bold"),
            text_color="white"
        )
        self.time_label.pack()
        
        greeting_label = ctk.CTkLabel(
            greeting_frame,
            text="Hello, User!",
            font=("Helvetica", 24),
            text_color="white"
        )
        greeting_label.pack()

    def create_weather(self):
        weather_frame = ctk.CTkFrame(self.main_frame, fg_color="black")
        weather_frame.grid(row=1, column=0, sticky="nsew", pady=10)
        
        # Sample weather data (in real app, this would come from an API)
        weather_label = ctk.CTkLabel(
            weather_frame,
            text="Sunny • 72°F",
            font=("Helvetica", 20),
            text_color="white"
        )
        weather_label.pack()

    def create_day(self):
        day_frame = ctk.CTkFrame(self.main_frame, fg_color="black")
        day_frame.grid(row=2, column=0, sticky="nsew", pady=10)
        
        day = datetime.now().strftime("%A, %B %d")
        day_label = ctk.CTkLabel(
            day_frame,
            text=day,
            font=("Helvetica", 20),
            text_color="white"
        )
        day_label.pack()

    def create_todo(self):
        todo_frame = ctk.CTkFrame(self.main_frame, fg_color="black")
        todo_frame.grid(row=3, column=0, sticky="nsew", pady=10)
        
        todo_title = ctk.CTkLabel(
            todo_frame,
            text="To-Do",
            font=("Helvetica", 20, "bold"),
            text_color="white"
        )
        todo_title.pack(anchor="w")
        
        # Sample todo list
        tasks = ["Buy groceries", "Call mom", "Finish project"]
        for task in tasks:
            task_label = ctk.CTkLabel(
                todo_frame,
                text=f"• {task}",
                font=("Helvetica", 16),
                text_color="white"
            )
            task_label.pack(anchor="w", padx=10)

    def create_quote(self):
        quote_frame = ctk.CTkFrame(self.main_frame, fg_color="black")
        quote_frame.grid(row=4, column=0, sticky="nsew", pady=10)
        
        quotes = [
            "The best way to predict the future is to create it. - Peter Drucker",
            "You miss 100% of the shots you don’t take. - Wayne Gretzky",
            "Be the change you wish to see in the world. - Mahatma Gandhi"
        ]
        
        quote_label = ctk.CTkLabel(
            quote_frame,
            text=random.choice(quotes),
            font=("Helvetica", 16, "italic"),
            text_color="white",
            wraplength=450,
            justify="center"
        )
        quote_label.pack()

    def update_time(self):
        current_time = datetime.now().strftime("%H:%M")
        self.time_label.configure(text=current_time)
        self.root.after(1000, self.update_time)  # Update every second

if __name__ == "__main__":
    root = ctk.CTk()
    app = SmartMirrorApp(root)
    root.mainloop()