import customtkinter as ctk
from datetime import datetime
import pytz

class SmartMirrorApp:
    def __init__(self, root):
        self.root = root
        self.root.geometry("500x700")
        self.root.title("Smart Mirror")
        self.root.configure(bg="black")
        
        # Set appearance
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Create main container frame
        self.main_frame = ctk.CTkFrame(root, fg_color="black")
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Configure grid layout (5 rows, 1 column)
        self.main_frame.grid_rowconfigure(0, weight=1)  # Top spacing
        self.main_frame.grid_rowconfigure(1, weight=2)  # Greeting/Date
        self.main_frame.grid_rowconfigure(2, weight=3)  # Weather
        self.main_frame.grid_rowconfigure(3, weight=4)  # Todo
        self.main_frame.grid_rowconfigure(4, weight=2)  # Quote
        self.main_frame.grid_rowconfigure(5, weight=1)  # Bottom spacing
        self.main_frame.grid_columnconfigure(0, weight=1)
        
        # Create widgets
        self.create_greeting_widget()
        self.create_weather_widget()
        self.create_todo_widget()
        self.create_quote_widget()
        
        # Update time and date continuously
        self.update_datetime()
    
    def create_greeting_widget(self):
        """Create greeting and date/time section"""
        frame = ctk.CTkFrame(self.main_frame, fg_color="black", corner_radius=0)
        frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)
        
        # Greeting label
        self.greeting_label = ctk.CTkLabel(
            frame, 
            text="Good Morning, User", 
            font=("Helvetica", 24, "bold"),
            text_color="white"
        )
        self.greeting_label.pack(pady=(0, 10))
        
        # Date and time labels
        self.date_label = ctk.CTkLabel(
            frame, 
            text="Monday, January 1", 
            font=("Helvetica", 18),
            text_color="white"
        )
        self.date_label.pack()
        
        self.time_label = ctk.CTkLabel(
            frame, 
            text="12:00 PM", 
            font=("Helvetica", 36, "bold"),
            text_color="white"
        )
        self.time_label.pack()
    
    def create_weather_widget(self):
        """Create weather information section"""
        frame = ctk.CTkFrame(self.main_frame, fg_color="black", corner_radius=10)
        frame.grid(row=2, column=0, sticky="nsew", padx=10, pady=5)
        
        # Weather icon and temp
        weather_frame = ctk.CTkFrame(frame, fg_color="black")
        weather_frame.pack(pady=10)
        
        # Weather icon (using text as placeholder)
        self.weather_icon = ctk.CTkLabel(
            weather_frame, 
            text="☀️", 
            font=("Helvetica", 48),
            text_color="white"
        )
        self.weather_icon.pack(side="left", padx=10)
        
        # Temperature and description
        weather_info_frame = ctk.CTkFrame(weather_frame, fg_color="black")
        weather_info_frame.pack(side="left", padx=10)
        
        self.temp_label = ctk.CTkLabel(
            weather_info_frame, 
            text="72°F", 
            font=("Helvetica", 36, "bold"),
            text_color="white"
        )
        self.temp_label.pack(anchor="w")
        
        self.weather_desc = ctk.CTkLabel(
            weather_info_frame, 
            text="Sunny", 
            font=("Helvetica", 18),
            text_color="white"
        )
        self.weather_desc.pack(anchor="w")
        
        # Additional weather info
        extra_info_frame = ctk.CTkFrame(frame, fg_color="black")
        extra_info_frame.pack(pady=(0, 10))
        
        self.humidity_label = ctk.CTkLabel(
            extra_info_frame, 
            text="💧 Humidity: 45%", 
            font=("Helvetica", 14),
            text_color="white"
        )
        self.humidity_label.pack(side="left", padx=20)
        
        self.wind_label = ctk.CTkLabel(
            extra_info_frame, 
            text="🌬️ Wind: 5 mph", 
            font=("Helvetica", 14),
            text_color="white"
        )
        self.wind_label.pack(side="left", padx=20)
    
    def create_todo_widget(self):
        """Create todo list section"""
        frame = ctk.CTkFrame(self.main_frame, fg_color="#111111", corner_radius=10)
        frame.grid(row=3, column=0, sticky="nsew", padx=10, pady=5)
        
        # Title
        title = ctk.CTkLabel(
            frame, 
            text="Today's Tasks", 
            font=("Helvetica", 20, "bold"),
            text_color="white"
        )
        title.pack(pady=(10, 5))
        
        # Todo list
        self.todo_list = ctk.CTkFrame(frame, fg_color="#111111")
        self.todo_list.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Sample tasks
        tasks = [
            "☐ Check emails",
            "☐ Morning workout",
            "☑ Buy groceries",
            "☐ Read 30 pages",
            "☐ Call mom"
        ]
        
        for task in tasks:
            task_label = ctk.CTkLabel(
                self.todo_list, 
                text=task, 
                font=("Helvetica", 16),
                text_color="white",
                anchor="w"
            )
            task_label.pack(fill="x", pady=2)
        
        # Add task entry
        add_frame = ctk.CTkFrame(frame, fg_color="#111111")
        add_frame.pack(fill="x", padx=10, pady=(5, 10))
        
        self.new_task_entry = ctk.CTkEntry(
            add_frame, 
            placeholder_text="Add new task...",
            fg_color="#222222",
            border_width=1,
            text_color="white"
        )
        self.new_task_entry.pack(side="left", fill="x", expand=True, padx=(0, 5))
        
        add_button = ctk.CTkButton(
            add_frame, 
            text="+", 
            width=30,
            fg_color="#333333",
            hover_color="#444444",
            command=self.add_task
        )
        add_button.pack(side="right")
    
    def create_quote_widget(self):
        """Create inspirational quote section"""
        frame = ctk.CTkFrame(self.main_frame, fg_color="black", corner_radius=10)
        frame.grid(row=4, column=0, sticky="nsew", padx=10, pady=5)
        
        # Quote text
        self.quote_text = ctk.CTkLabel(
            frame, 
            text="The only way to do great work is to love what you do. \n- Steve Jobs", 
            font=("Helvetica", 14, "italic"),
            text_color="white",
            wraplength=450,
            justify="center"
        )
        self.quote_text.pack(pady=20)
    
    def update_datetime(self):
        """Update the date and time display"""
        now = datetime.now(pytz.timezone('America/New_York'))
        
        # Update time
        current_time = now.strftime("%I:%M %p").lstrip("0")
        self.time_label.configure(text=current_time)
        
        # Update date
        current_date = now.strftime("%A, %B %d")
        self.date_label.configure(text=current_date)
        
        # Update greeting based on time of day
        hour = now.hour
        if 5 <= hour < 12:
            greeting = "Good Morning"
        elif 12 <= hour < 18:
            greeting = "Good Afternoon"
        else:
            greeting = "Good Evening"
        
        self.greeting_label.configure(text=f"{greeting}, User")
        
        # Schedule next update
        self.root.after(1000, self.update_datetime)
    
    def add_task(self):
        """Add a new task to the todo list"""
        task_text = self.new_task_entry.get()
        if task_text:
            task_label = ctk.CTkLabel(
                self.todo_list, 
                text=f"☐ {task_text}", 
                font=("Helvetica", 16),
                text_color="white",
                anchor="w"
            )
            task_label.pack(fill="x", pady=2)
            self.new_task_entry.delete(0, 'end')

if __name__ == "__main__":
    root = ctk.CTk()
    app = SmartMirrorApp(root)
    root.mainloop()