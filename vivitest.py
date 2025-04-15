import customtkinter as ctk
from Vivi import ViviAnimation

# Initialize the main window
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

root = ctk.CTk()
root.geometry("500x400")
root.title("Main Interface")

# Create an instance of the ViviAnimation
vivi_animation = ViviAnimation(root, "ViviStill.gif", width=150, height=150, frame_delay=50, x=100, y=150)

# Run the main loop
root.mainloop()