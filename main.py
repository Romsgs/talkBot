import uuid
import speech_recognition as sr
from gtts import gTTS
# from playsound import playsound
import openai
import os
import pygame.mixer
import subprocess
pygame.mixer.init()
# OpenAI API key
openai_api_key = 
# Suppress ALSA warnings globally
subprocess.run(['/home/c0y073/miniconda3/bin/python', '/home/c0y073/dev/talkBot/getResponse.py'], stderr=subprocess.DEVNULL)

# Initialize the OpenAI API client
openai.api_key = openai_api_key

# Function to generate response from ChatGPT
def get_response(speech):
    # Define a system message for ChatGPT
    system_message = "voce ẽ um assistente virtual em portugues brasileiro"
    
    # Use ChatGPT to generate a greeting message
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": f"responda a este texto: {speech}, use respostas mais curtas para economizar os tokens."},
        ],
    )
    return response['choices'][0]['message']['content'].strip('"')

# Function to convert speech to text
def listen_to_voice():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("ouvindo...")
        audio = recognizer.listen(source)

    try:
        text_heard = recognizer.recognize_google(audio, language="pt-BR")
        return text_heard
    except sr.UnknownValueError:
        return "nada"
    except sr.RequestError as e:
        return "nada"

# Function to convert text to speech and play it
def speak(text):
    tts = gTTS(text=text, lang='pt-BR')
    filename = f'voice_{uuid.uuid4().hex}.mp3'
    tts.save(filename)
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()
    # playsound(filename)
    

# Function to play a greeting message
def play_greet():
    filename = 'greet.mp3'
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()
    # playsound(filename)

# Function to handle user interaction
def main():
    while True:
        text_heard = listen_to_voice()
        print(f"User: {text_heard}")

        if text_heard.lower() == "nada":
            continue

        elif text_heard == 'Oi bote':
            play_greet()
            text_heard = listen_to_voice()
            response = get_response(text_heard)
            print(f"Response: {response}")
            speak(response)

if __name__ == "__main__":
    main()
