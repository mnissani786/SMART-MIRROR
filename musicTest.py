import vlc
import time
import mutagen
from mutagen.mp4 import MP4
import os
import random
import threading

directory = ".\Sample Music"
files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
player = None

# Selects a random song from the song folder
def skip():
    if files:
        random_file = random.choice(files)
        print(f"Current Song: {random_file}")
        
        # Get the file path and create the VLC player
        file_path = os.path.join(directory, random_file)
        player = vlc.MediaPlayer(file_path)

        player.play()
        time.sleep(1)  # Small delay to give VLC time to start playing

        # Wait for the media to finish playing or an error to occur
        while player.get_state() not in [vlc.State.Ended, vlc.State.Stopped, vlc.State.Error]:
            time.sleep(1)  # Sleep to avoid overloading the CPU and causing buffer issues
    else:
        print("No files found in directory.")

# Debugging
while True:
    cmd = input("Enter command:")
    if cmd == "play":
        pass
    elif cmd == "pause":
        pass
    elif cmd == "skip":
        currentSong = threading.Thread(target=skip)
        currentSong.start()
    elif cmd == "exit":
        break
