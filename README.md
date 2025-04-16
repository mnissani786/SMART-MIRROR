# Welcome to Reflective Assistant!

By Kaeden Bryer, Christina Carvalho, Maria Echeverri Solis and Malik Issani

This is our group's sophomore project at Oakland University. Reflective Assistant is the software for a smart mirror
which curates essential information for the user's morning.


## How to Run! (Read this before running)

I've added the sample code I used to get the voice agent working. To use these, you will need to 1. install all the requirements in requirements.txt and 2. make sure you have the .env file. I've purpose committed the .env file so it should work out of the box for you guys, but know that that is bad practice. Use of API keys accumulates charges, so if the world got them I'd be bankrupt lol.

run "pip install -r requirements.txt"
make sure dotenv and load_dotenv() are working properly if anything fails.

You might have to restart vscode or your computer if you're getting an error saying API key invalid.

Let me know if there are any issues!

As of submitting, this requirements.txt should be up to date with pip freeze > requirements.txt


## Vivi Voice Commands:
#### Voice Assistance
"Hey, Vivi" -- moves Vivi Voice Assistant from listening mode to active mode.

["Goodbye", "Exit", "Close", "Bye"] -- moves Vivi Voice Assistant from active mode to listening mode

#### Smart Home Widget
"Open Smart Home" -- Opens Smart Home Widget

["Red", "Orange", "Yellow", "Green", "Blue", "Purple] -- changes LED light strip colors and Govee Smart Lamp color

"Exit Smart Home" -- Exits Smart Home Widget

#### Music Widget
"Open Music" -- Opens Music Widget

"Play Music" -- Starts song

"Skip Music" -- Skips song

"Pause Song" -- Pauses song

"Shuffle Music" -- Shuffles Playlist

"Exit Music" -- Exits Music Widget


#### Weather Widget
"Open Weather" -- Opens Weather Widget

"Exit Weather" -- Exits Weather Widget


#### News Widget
"Open News" -- Opens News Widget

"Exit News" -- Exits News Widget


## Goals:
#### 1. Make Functioning widgets that gather data and respond to user inputs ✅


#### 2. Have functional user input ✅


#### 3. Ensure the Hardware is Properly Functioning and Clean 🌗


#### 4. Integrate a Real Time Voice Assistant 🌗
