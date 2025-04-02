import customtkinter as ctk
from datetime import datetime
import random

# Sample data for quote and weather
QUOTES = [
    "Believe you can and you're halfway there.",
    "The only way to do great work is to love what you do.",
    "You are never too old to set another goal or to dream a new dream.",
]

WEATHER = "26°C, Clear Skies"

def update_quote():
    quote_label.configure(text=random.choice(QUOTES))

def add_todo():
    task = todo_entry.get()
    if task:
        todo_listbox.insert(ctk.END, task)
        todo_entry.delete(0, ctk.END)

def remove_todo():
    try:
        selected = todo_listbox.curselection()
        todo_listbox.delete(selected[0])
    except:
        pass

# Initialize main app
ctk.set_appearance_mode("dark")  # Dark mode for modern look
root = ctk.CTk()
root.geometry("500x700")
root.title("Smart Mirror")
root.configure(bg="black")

# Grid configuration
root.columnconfigure(0, weight=1)
root.rowconfigure([0, 1, 2, 3, 4], weight=1)

# Hello Message
hello_label = ctk.CTkLabel(root, text="Hello, User!", font=("Arial", 24), text_color="white")
hello_label.grid(row=0, column=0, pady=10, sticky="n")

# Weather
weather_label = ctk.CTkLabel(root, text=f"Weather: {WEATHER}", font=("Arial", 18), text_color="white")
weather_label.grid(row=1, column=0, pady=10)

# Day of the week
day_label = ctk.CTkLabel(root, text=datetime.today().strftime("%A"), font=("Arial", 20), text_color="white")
day_label.grid(row=2, column=0, pady=10)

# Quote Section
quote_label = ctk.CTkLabel(root, text=random.choice(QUOTES), wraplength=400, font=("Arial", 16), text_color="white")
quote_label.grid(row=3, column=0, pady=10)
quote_button = ctk.CTkButton(root, text="New Quote", command=update_quote)
quote_button.grid(row=3, column=0, pady=10, sticky="s")

# To-do List
todo_frame = ctk.CTkFrame(root)
todo_frame.grid(row=4, column=0, pady=20, padx=20, sticky="nsew")

todo_label = ctk.CTkLabel(todo_frame, text="To-Do List", font=("Arial", 18), text_color="white")
todo_label.pack()

todo_entry = ctk.CTkEntry(todo_frame, width=300)
todo_entry.pack(pady=5)

todo_add_button = ctk.CTkButton(todo_frame, text="Add", command=add_todo)
todo_add_button.pack()

todo_listbox = ctk.CTkTextbox(todo_frame, height=100, width=300)
todo_listbox.pack(pady=5)

todo_remove_button = ctk.CTkButton(todo_frame, text="Remove", command=remove_todo)
todo_remove_button.pack()

root.mainloop()