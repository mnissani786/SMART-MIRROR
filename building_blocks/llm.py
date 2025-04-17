from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os
from pygame import mixer
import time

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

with open('system_prompt.txt', 'r') as file:
    system_prompt = file.read().strip()

def batch():
    chat = ChatGroq(temperature=0, model_name="meta-llama/llama-4-scout-17b-16e-instruct", groq_api_key=os.getenv("GROQ_API_KEY"))

    system = system_prompt
    human = "{text}"
    prompt = ChatPromptTemplate.from_messages([("system", system), ("human", human)])

    chain = prompt | chat
    text = (chain.invoke({"text": "Explain the importance of low latency LLMs."}))
    print(text.content)

# Streaming
def streaming():
    chat = ChatGroq(temperature=0, model_name="meta-llama/llama-4-scout-17b-16e-instruct",groq_api_key=os.getenv("GROQ_API_KEY"))
    prompt = ChatPromptTemplate.from_messages([("human", "Write a very long poem about {topic}")])
    chain = prompt | chat
    for chunk in chain.stream({"topic": "The Moon"}):
        print(chunk.content, end="", flush=True)

batch()
# streaming()
