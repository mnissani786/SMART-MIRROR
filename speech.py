import speech_recognition as sr
import pyttsx3

# intializing recognizer and engine
r = sr.Recognizer()
engine = pyttsx3.init()

# properties
engine.setProperty('rate', 150) 
engine.setProperty('volume', 1.0)  

voices = engine.getProperty('voices')
engine.setProperty('voice', voices[14].id)  # Use the first voice in the list

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
        engine.say(text)
        engine.runAndWait()
        
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
    


