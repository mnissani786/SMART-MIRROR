import time
import mutagen
from mutagen.mp4 import MP4
import os
import random
import threading
from threading import current_thread
from threading import Event

import sys
import ctypes

# Get the absolute path to the VLC DLL directory you bundled
vlc_dir = os.path.join(os.path.dirname(__file__), 'vlc')

# Add the VLC directory to the DLL search path (Python 3.8+)
os.add_dll_directory(vlc_dir)

# You can also explicitly load the DLL to ensure it's initialized
ctypes.CDLL(os.path.join(vlc_dir, 'libvlc.dll'))

import vlc

class MusicPlayer:
    def __init__(self):
        self.directory = ".\Sample Music"  # Can change if necessary
        self.files = [f for f in os.listdir(self.directory) if os.path.isfile(os.path.join(self.directory, f))] # Finds the files
        self.currentFile = None
        self.player = None
        self.shuffle = True
        self.paused = False
        self.event = Event() # This helps to kill the active thread

    # The user can toggle suffle
    def toggleShuffle(self):
        return not self.shuffle

    # Selects song file based on shuffle status and current song playing
    def fileSelect(self):    
        if self.shuffle == True: #If shuffle is on, it selects a random file
            randomFile = random.choice(self.files)
            return randomFile    
        elif self.currentFile == None: # If shuffle is not on, and there *IS NOT* a current song playing or paused, it selects the first file
            firstfile = self.files[0]
            print(firstfile)
            return firstfile
        else: # If shuffle is not on, and there *IS* a current song playing or paused, it selects the next file in the list
            counter = 0
            for x in self.files:
                counter += 1
                #print("Counter: "+str(counter)+" x: "+x)
                if x == self.currentFile and self.files[counter] != None:                    
                    nextFile = self.files[counter]
                    return nextFile
                time.sleep(1)        
                

    def togglePause(self):
        self.player.pause() #toggles 

    def play(self):
        self.currentFile = self.fileSelect()
        print(f"Current Song: {self.currentFile}")
        
        # Get the file path and create the VLC player
        self.file_path = os.path.join(self.directory, self.currentFile)
        self.player = vlc.MediaPlayer(self.file_path)
        time.sleep(1)
        self.player.play()
        return self.player    

    def skip(self, event):
        if self.files:
            self.player = self.play()

            time.sleep(1)  # Small delay to give VLC time to start playing
            
            # Wait for the media to finish playing or an error to occur
            while self.player.get_state() not in [vlc.State.Ended, vlc.State.Stopped, vlc.State.Error]:
                # Checks if the user skipped the song
                if event.is_set():
                    self.player.stop()
                    break
                time.sleep(1)  # Sleep to avoid overloading the CPU and causing buffer issues
            
            # After the song reaches the end, it automaticly skips to the next song
            if event.is_set() == False:
                self.skip(event)

        else:
            print("No files found in directory.")

    # for debugging, will transfer to UI design
    def main(self, cmd):        
        if cmd == "pause":
            self.togglePause()
        elif cmd == "skip":
            self.event.set()  # Changes event to true, meaning that skip has been called
            time.sleep(1)  # Sleep to avoid overloading the CPU and causing buffer issues
            self.event.clear()  # Resets event to false
            self.currentSong = threading.Thread(target=self.skip, args=(self.event,))  # Creates the thread to play the music
            self.currentSong.start()
        elif cmd == "shuffle":
            self.shuffle = self.toggleShuffle()
            print("Shuffle set to: " +str(self.shuffle))
            

# if __name__ == "__main__":
#     newPlayer = MusicPlayer()
#     newPlayer.main()