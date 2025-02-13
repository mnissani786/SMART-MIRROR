
## Imported from ChatGPT as example
## https://chatgpt.com/c/67a8234e-1350-800f-ac5f-e11519580c57

## ***************DO NOT RUN FROM HERE**********************
## type:     python Test.py      in command prompt to run program

import tkinter as tk
import threading
import queue

class CommandApp(tk.Tk):
    def __init__(self, command_queue):
        super().__init__()

        self.command_queue = command_queue
        self.title("Button Selector")
        self.geometry("400x400")

        # Button setup
        self.buttons = []
        self.button_labels = ["Button 1", "Button 2", "Button 3", "Button 4"]

        # Canvas for visual box selection
        self.canvas = tk.Canvas(self, width=400, height=400, bg="black")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Create buttons aligned vertically on the right side
        self.button_positions = []
        button_width, button_height = 100, 40

        for i, label in enumerate(self.button_labels):
            y_position = 50 + i * 70
            x_start = 300
            button = tk.Button(self.canvas, text=label, width=10, height=2)
            button_window = self.canvas.create_window(x_start, y_position, window=button)
            self.button_positions.append((x_start, y_position))
            self.buttons.append(button)

        # Selection box
        self.selection_index = 0
        self.selection_box = self.canvas.create_rectangle(
            self.button_positions[0][0] - button_width // 2 - 5,
            self.button_positions[0][1] - button_height // 2 - 5,
            self.button_positions[0][0] + button_width // 2 + 5,
            self.button_positions[0][1] + button_height // 2 + 5,
            outline="white", width=3
        )

        # Start the command processing loop
        self.update_box()

    def move_selection(self, direction):
        if direction == "up" and self.selection_index > 0:
            self.selection_index -= 1
        elif direction == "down" and self.selection_index < len(self.buttons) - 1:
            self.selection_index += 1

        # Update the selection box position
        x, y = self.button_positions[self.selection_index]
        self.canvas.coords(
            self.selection_box,
            x - 50 - 5, y - 20 - 5,  # Left-top corner
            x + 50 + 5, y + 20 + 5   # Right-bottom corner
        )

    def press_selected_button(self):
        # Simulate button press by calling its command function (if any)
        selected_button = self.buttons[self.selection_index]
        print(f"Pressed: {selected_button['text']}")  # Feedback on the command prompt

    def update_box(self):
        # Poll the queue for new commands
        while not self.command_queue.empty():
            command = self.command_queue.get()
            if command in {"up", "down"}:
                self.move_selection(command)
            elif command == "enter":
                self.press_selected_button()

        # Schedule next update
        self.after(100, self.update_box)


def read_commands(command_queue):
    """Reads commands from the command prompt and places them in a queue."""
    while True:
        command = input("Enter a direction (up, down, enter): ").strip().lower()
        if command in {"up", "down", "enter"}:
            command_queue.put(command)
        else:
            print(f"Unknown command: '{command}'")


def main():
    # Create a thread-safe queue for commands
    command_queue = queue.Queue()

    # Create and start the Tkinter app
    app = CommandApp(command_queue)

    # Start the command-reading thread
    command_thread = threading.Thread(target=read_commands, args=(command_queue,), daemon=True)
    command_thread.start()

    # Run the Tkinter main loop
    app.mainloop()


if __name__ == "__main__":
    main()
