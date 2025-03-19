import speech_recognition as sr
import pyttsx3

# Initialize recognizer
r = sr.Recognizer()

# Initialize the pyttsx3 engine
engine = pyttsx3.init()

# Set properties (optional)
engine.setProperty('rate', 150)    # Speed of speech (words per minute)
engine.setProperty('volume', 1.0)  # Volume (0.0 to 1.0)

# Choose a voice (optional)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[14].id)  # Use the first voice in the list


# Use microphone as source
def get_audio():
    with sr.Microphone() as source:
        print("Say something!")
        audio = r.listen(source)
    try:
        # Recognize speech using Google Web Speech API
        text = r.recognize_google(audio)
        print("You said: {}".format(text))
        audio = "You said: {}".format(text)
        engine.say(audio)
        engine.runAndWait()

    except sr.UnknownValueError:
        text = "Could not understand audio"
        # Say the text
        engine.say(text)
        # Wait for the speech to finish
        engine.runAndWait()
        
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
    


