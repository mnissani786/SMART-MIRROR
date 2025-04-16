import asyncio
from dotenv import load_dotenv
import shutil
import subprocess
import requests
import time
import os

from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from langchain.memory import ConversationBufferMemory
from langchain.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.chains import LLMChain

from deepgram import (
    DeepgramClient,
    DeepgramClientOptions,
    LiveTranscriptionEvents,
    LiveOptions,
    Microphone,
)

from smarthome import SmartHome
from event_manager import event_manager
from goveeTest import changeLight, colorConversion

load_dotenv()

On_SmartHome = True

class LanguageModelProcessor:
    def __init__(self):
        self.llm = ChatGroq(temperature=0, model_name="meta-llama/llama-4-scout-17b-16e-instruct", groq_api_key=os.getenv("GROQ_API_KEY"))

        self.memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

        # Load the system prompt from a file
        with open('system_prompt.txt', 'r') as file:
            system_prompt = file.read().strip()
        
        self.prompt = ChatPromptTemplate.from_messages([
            SystemMessagePromptTemplate.from_template(system_prompt),
            MessagesPlaceholder(variable_name="chat_history"),
            HumanMessagePromptTemplate.from_template("{text}")
        ])

        self.conversation = LLMChain(
            llm=self.llm,
            prompt=self.prompt,
            memory=self.memory
        )

    def process(self, text):
        self.memory.chat_memory.add_user_message(text)  # Add user message to memory

        start_time = time.time()

        # Go get the response from the LLM
        response = self.conversation.invoke({"text": text})
        end_time = time.time()

        self.memory.chat_memory.add_ai_message(response['text'])  # Add AI response to memory

        elapsed_time = int((end_time - start_time) * 1000)
        print(f"LLM ({elapsed_time}ms): {response['text']}")
        return response['text']

class TextToSpeech:
    # Set your Deepgram API Key and desired voice model
    DG_API_KEY = os.getenv("DEEPGRAM_API_KEY")
    MODEL_NAME = "aura-asteria-en"  # Example model name, change as needed

    @staticmethod
    def is_installed(lib_name: str) -> bool:
        lib = shutil.which(lib_name)
        return lib is not None

    def speak(self, text):
        if not self.is_installed("ffplay"):
            raise ValueError("ffplay not found, necessary to stream audio.")

        DEEPGRAM_URL = f"https://api.deepgram.com/v1/speak?model={self.MODEL_NAME}"
        headers = {
            "Authorization": f"Token {self.DG_API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "text": text
        }

        player_command = ["ffplay", "-autoexit", "-", "-nodisp"]
        player_process = subprocess.Popen(
            player_command,
            stdin=subprocess.PIPE,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

        start_time = time.time()  # Record the time before sending the request
        first_byte_time = None  # Initialize a variable to store the time when the first byte is received

        with requests.post(DEEPGRAM_URL, stream=True, headers=headers, json=payload) as r:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:
                    if first_byte_time is None:  # Check if this is the first chunk received
                        first_byte_time = time.time()  # Record the time when the first byte is received
                        ttfb = int((first_byte_time - start_time)*1000)  # Calculate the time to first byte
                        print(f"TTS Time to First Byte (TTFB): {ttfb}ms\n")
                    player_process.stdin.write(chunk)
                    player_process.stdin.flush()

        if player_process.stdin:
            player_process.stdin.close()
        player_process.wait()

class TranscriptCollector:
    def __init__(self):
        self.reset()

    def reset(self):
        self.transcript_parts = []

    def add_part(self, part):
        self.transcript_parts.append(part)

    def get_full_transcript(self):
        return ' '.join(self.transcript_parts)

transcript_collector = TranscriptCollector()

async def get_transcript(callback):
    transcription_complete = asyncio.Event()  # Event to signal transcription completion

    try:
        # example of setting up a client config. logging values: WARNING, VERBOSE, DEBUG, SPAM
        config = DeepgramClientOptions(options={"keepalive": "true"})
        deepgram: DeepgramClient = DeepgramClient("", config)

        dg_connection = deepgram.listen.asynclive.v("1")
        print ("Listening...")

        async def on_message(self, result, **kwargs):
            sentence = result.channel.alternatives[0].transcript
            
            if not result.speech_final:
                transcript_collector.add_part(sentence)
            else:
                # This is the final part of the current sentence
                transcript_collector.add_part(sentence)
                full_sentence = transcript_collector.get_full_transcript()
                # Check if the full_sentence is not empty before printing
                if len(full_sentence.strip()) > 0:
                    full_sentence = full_sentence.strip()
                    print(f"Human: {full_sentence}")
                    callback(full_sentence)  # Call the callback with the full_sentence
                    transcript_collector.reset()
                    transcription_complete.set()  # Signal to stop transcription and exit

        dg_connection.on(LiveTranscriptionEvents.Transcript, on_message)

        options = LiveOptions(
            model="nova-2",
            punctuate=True,
            language="en-US",
            encoding="linear16",
            channels=1,
            sample_rate=16000,
            endpointing=300,
            smart_format=True,
        )

        await dg_connection.start(options)

        # Open a microphone stream on the default input device
        microphone = Microphone(dg_connection.send)
        microphone.start()

        await transcription_complete.wait()  # Wait for the transcription to complete instead of looping indefinitely

        # Wait for the microphone to close
        microphone.finish()

        # Indicate that we've finished
        await dg_connection.finish()

    except Exception as e:
        print(f"Could not open socket: {e}")
        return

class ConversationManager:
    def __init__(self):
        self.transcription_response = ""
        self.llm = LanguageModelProcessor()

    async def main(self):
        global On_SmartHome
        def handle_full_sentence(full_sentence):
            self.transcription_response = full_sentence

        # Loop indefinitely until "goodbye" is detected
        while True:
            tts = TextToSpeech()
            while True:
                await get_transcript(handle_full_sentence)

                if On_SmartHome:
                    if "red" in self.transcription_response.lower():
                        print("Turning the light red...")
                        tts.speak("Govee Light Red.")
                        changeLight("devices.capabilities.color_setting", "colorRgb", int(colorConversion(255, 0, 0)))
                    if "orange" in self.transcription_response.lower():
                        print("Turning the light orange...")
                        tts.speak("Govee Light Orange.")
                        changeLight("devices.capabilities.color_setting", "colorRgb", int(colorConversion(255, 127, 0)))
                    if "yellow" in self.transcription_response.lower():
                        print("Turning the light yellow...")
                        tts.speak("Govee Light Yellow.")
                        changeLight("devices.capabilities.color_setting", "colorRgb", int(colorConversion(255, 255, 0)))    
                    if "green" in self.transcription_response.lower():
                        print("Turning the light green...")
                        tts.speak("Govee Light Green.")
                        changeLight("devices.capabilities.color_setting", "colorRgb", int(colorConversion(0, 255, 0)))
                    if "blue" in self.transcription_response.lower():
                        print("Turning the light blue...")
                        tts.speak("Govee Light Blue.")
                        changeLight("devices.capabilities.color_setting", "colorRgb", int(colorConversion(0, 0, 255)))
                    if "purple" in self.transcription_response.lower():
                        print("Turning the light purple...")
                        tts.speak("Govee Light Purplse.")
                        changeLight("devices.capabilities.color_setting", "colorRgb", int(colorConversion(160, 0, 255)))
                    if "close" in self.transcription_response.lower():
                        print("Closing the smart home widget...")
                        tts.speak("Closing smart home.")
                        event_manager.trigger_event("smart_home_deactivate")  # Trigger the event
                        On_SmartHome = False

                # Check for the keyword "vivi" to start the conversation
                if "hey, vivi" in self.transcription_response.lower():
                    print("Voice activation detected. Starting conversation...")
                    tts.speak("Hey! How can I help you?")
                    break
                if "smart home" in self.transcription_response.lower():
                    print("Smart home activation detected. Starting smart home conversation...")
                    tts.speak("Smart home activated.")
                    event_manager.trigger_event("smart_home_activate")  # Trigger the event
                    On_SmartHome = True

                # Reset transcription_response for the next loop iteration
                self.transcription_response = ""

            while True:
                await get_transcript(handle_full_sentence)
                  
                # Check for "goodbye", "exit", "quit" or "bye" to exit the loop
                if any(word in self.transcription_response.lower() for word in ["goodbye", "exit", "quit", "bye"]):
                    tts.speak("Goodbye!")
                    print("Exiting conversation...")
                    break
                
                llm_response = self.llm.process(self.transcription_response)

                tts.speak(llm_response)
                print(f"llm response: {llm_response}")

                # Reset transcription_response for the next loop iteration
                self.transcription_response = ""

if __name__ == "__main__":
    manager = ConversationManager()
    asyncio.run(manager.main())
