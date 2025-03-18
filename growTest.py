import customtkinter as ctk

# Create main window
root = ctk.CTk()
root.geometry("500x400")

# Create a weather label
weather_label = ctk.CTkLabel(root, text="☀️  Sunny 25°C", font=("Arial", 20))
weather_label.place(relx=0.5, rely=0.5, anchor="center")  # Center the widget

# Animation variables
font_size = 20
growing = True

# Function to animate the size change
def animate_size():
    global font_size, growing

    if growing:
        font_size += 2  # Increase size
        if font_size >= 40:  # Max size
            growing = False
    else:
        font_size -= 2  # Decrease size
        if font_size <= 20:  # Min size
            growing = True

    # Apply new font size
    weather_label.configure(font=("Arial", font_size))
    
    # Repeat animation
    root.after(100, animate_size)

# Start animation
animate_size()

root.mainloop()