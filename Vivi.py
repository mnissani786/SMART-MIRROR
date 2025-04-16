import customtkinter as ctk
from PIL import Image, ImageTk, ImageSequence

class GifAnimation:
    def __init__(self, parent, gif_path, width=100, height=100, frame_delay=50, x=0, y=0):
        self.parent = parent
        self.gif_path = gif_path
        self.width = width
        self.height = height
        self.frame_delay = frame_delay
        self.x = x
        self.y = y

        # Load the GIF and prepare frames
        gif = Image.open(self.gif_path)
        self.frames = [
            ctk.CTkImage(frame.copy().convert("RGBA"), size=(self.width, self.height))
            for frame in ImageSequence.Iterator(gif)
        ]
        self.frame_count = len(self.frames)

        # Create a label to display the animation
        self.label = ctk.CTkLabel(self.parent, text="", image=self.frames[0])
        self.label.place(x=self.x, y=self.y)

        # Start the animation
        self.current_frame = 0
        self.update_animation()

    def update_animation(self):
        frame = self.frames[self.current_frame]
        self.label.configure(image=frame)
        self.label.image = frame  # Keep a reference to avoid garbage collection
        self.current_frame = (self.current_frame + 1) % self.frame_count
        self.parent.after(self.frame_delay, self.update_animation)

# Only run the following code if this file is executed directly
if __name__ == "__main__":
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")

    root = ctk.CTk()
    root.geometry("500x400")
    root.title("Vivi Animation Test")

    # Create an instance of ViviAnimation for testing
    vivi_animation = ViviAnimation(root, "ViviAnimation.gif", width=150, height=150, frame_delay=50, x=100, y=100)

    # Run the main loop
    root.mainloop()