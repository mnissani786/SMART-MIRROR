import customtkinter as ctk

# Create main window
root = ctk.CTk()
root.geometry("500x400")

# Create a label to display weather
weather_label = ctk.CTkLabel(root, text="☀️  Sunny 25°C", font=("Arial", 20))
weather_label.place(x=50, y=50)  # Initial position

# Animation function
def move_widget():
    global x_pos
    x_pos += 5  # Move right by 5 pixels
    if x_pos > 400:  # Reset when it reaches the end
        x_pos = 50
    weather_label.place(x=x_pos, y=100)  # Update position
    root.after(100, move_widget)  # Repeat after 100ms

# Initialize position
x_pos = 50

# Start animation
move_widget()

root.mainloop()
