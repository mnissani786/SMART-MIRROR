import customtkinter as ctk
import os

if os.environ.get('DISPLAY', '') == '':
	print('no display found. Using:0.0')
	os.environ.__setitem__('DISPLAY', ':0.0')

# Create main window
root = ctk.CTk()
root.geometry("500x400")

# Create a label to display weather
sample_label = ctk.CTkLabel(root, text="You've lost the game", font=("Arial", 20))
sample_label.place(x=50, y=50)  # Initial position


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
    sample_label.configure(font=("Arial", font_size))
    
    # Repeat animation
    root.after(100, animate_size)

# Start animation
animate_size()

root.mainloop()
