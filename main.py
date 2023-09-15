import speech_recognition as sr
from gtts import gTTS
import openai
import os
import simpleaudio as sa
from pydub import AudioSegment
from pydub.playback import play
# OpenAI API key
openai_api_key = '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'

# Initialize the OpenAI API client
openai.api_key = openai_api_key

# generate response function
def get_response(speech):
    # Define a system message for ChatGPT
    system_message = "You must act like a alexa assistent"
    
    # Use ChatGPT to generate a greeting message
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": f"answer this {speech}, no more than 500 characters."},
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

# Function to convert text to speech and play it using simpleaudio
def text_to_voice(text):
    tts = gTTS(text, lang="pt-BR")
    tts.save("response.mp3")
    audio = AudioSegment.from_mp3("response.mp3")
    play(audio)


if __name__ == "__main__":
    while True:
        text_heard = listen_to_voice()
        print(f"User: {text_heard}")
        if text_heard.lower() == "nada":
            continue
        else:
          response = get_response(text_heard)
          print(f"Response: {response}")
          text_to_voice(response)

        # Add an exit condition, for example, by saying "exit" to stop the loop
        
