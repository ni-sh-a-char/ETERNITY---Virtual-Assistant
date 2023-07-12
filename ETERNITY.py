import random
import webbrowser
import pyttsx3
import speech_recognition as sr
from gtts import gTTS
import playsound
import openai
import pyaudio
import time
import pyautogui
import sys

# Initialize OpenAI API
openai.api_key = "Paste your OpenAI key"

# Initialize the text to speech engine
engine = pyttsx3.init()

interrupt_flag = False  # Flag to indicate if interrupt was triggered

def transcribe_audio_to_text(filename):
    recognizer = sr.Recognizer()
    with sr.AudioFile(filename) as source:
        audio = recognizer.record(source)
    try:
        return recognizer.recognize_google(audio)
    except:
        print("Skipping unknown error")

def generate_response(prompt):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=4000,
        n=1,
        stop=None,
        temperature=0.5,
    )
    return response["choices"][0]["text"]

def speak_text(text):
    engine.say(text)
    engine.runAndWait()

def record_audio(ask=""):
    global interrupt_flag

    with sr.Microphone() as source:
        if ask:
            speak_text(ask)
        recognizer = sr.Recognizer()
        audio = recognizer.listen(source, 5, 5)
        voice_data = ''

        if interrupt_flag:  # Check if interrupt flag is True
            interrupt_flag = False
            return ''

        try:
            voice_data = recognizer.recognize_google(audio)
        except sr.UnknownValueError:
            speak_text("Sorry, I didn't catch that.")
        except sr.RequestError:
            speak_text("Sorry, I can't process your request at the moment.")

        print(">>", voice_data.lower())
        return voice_data.lower()

def respond(voice_data):
    global engine, interrupt_flag

    if "mute" in voice_data or "cancel" in voice_data or "stop" in voice_data:
        interrupt_flag = True
        engine.stop()
        return

    # 1: greeting

    if "hello" in voice_data or "hi" in voice_data or "hey" in voice_data:
        greetings = [
            "Yeah, how can I help you, " + person_obj.name + "?",
            "Hey, what's up, " + person_obj.name + "?",
            "I'm listening, " + person_obj.name + ".",
            "How can I assist you, " + person_obj.name + "?",
            "Hello, " + person_obj.name + ".",
        ]
        greet = random.choice(greetings)
        speak_text(greet)

    # 2: name
    if "what is your name" in voice_data or "what's your name" in voice_data or "tell me your name" in voice_data:
        if person_obj.name:
            speak_text("What's with my name?")
        else:
            speak_text("I don't know my name. What's your name?")

    if "my name is" in voice_data:
        person_name = voice_data.split("is")[-1].strip()
        speak_text("Ok, I will remember that " + person_name)
        person_obj.setName(person_name)

    if "your name should be" in voice_data:
        asis_name = voice_data.split("be")[-1].strip()
        speak_text("Ok, I will remember that's my name is " + asis_name)
        asis_obj.setName(asis_name)

    # 3: greeting
    if "how are you" in voice_data or "how are you doing" in voice_data:
        speak_text("I'm very well, thanks for asking " + person_obj.name)

    # 4: time
    if "what's the time" in voice_data or "tell me the time" in voice_data or "what time is it" in voice_data:
        current_time = time.ctime().split(" ")[3].split(":")[0:2]
        if current_time[0] == "00":
            hours = '12'
        else:
            hours = current_time[0]
        minutes = current_time[1]
        speak_text(hours + " hours and " + minutes + " minutes")

    # 5: search google
    if there_exists(["search for"], voice_data) and 'youtube' not in voice_data:
        search_term = voice_data.split("for")[-1]
        url = "https://google.com/search?q=" + search_term
        webbrowser.get().open(url)
        speak_text("Here is what I found for " + search_term + " on Google.")

    # 6: search youtube
    if "youtube" in voice_data:
        search_term = voice_data.split("for")[-1]
        url = "https://www.youtube.com/results?search_query=" + search_term
        webbrowser.get().open(url)
        speak_text("Here is what I found for " + search_term + " on YouTube.")

    # 7: get stock price
    if there_exists(["price of"], voice_data):
        search_term = voice_data.split("for")[-1]
        url = "https://google.com/search?q=" + search_term
        webbrowser.get().open(url)
        speak_text("Here is what I found for " + search_term + " on Google.")

    # 8: play music
    if there_exists(["play music"], voice_data):
        search_term = voice_data.split("for")[-1]
        url = "https://open.spotify.com/search/" + search_term
        webbrowser.get().open(url)
        speak_text("You are listening to " + search_term + ". Enjoy!")

    # 9: open a website
    if there_exists(["open a website"], voice_data):
        website = voice_data.split("website")[-1].strip()
        url = "https://" + website
        webbrowser.get().open(url)
        speak_text("Opening " + website)

    # 10: make a note
    if there_exists(["make a note"], voice_data):
        search_term = voice_data.split("for")[-1]
        url = "https://keep.google.com/#home"
        webbrowser.get().open(url)
        speak_text("Here you can make notes.")

    # 11: open Instagram
    if there_exists(["open Instagram"], voice_data):
        search_term = voice_data.split("for")[-1]
        url = "https://www.instagram.com/"
        webbrowser.get().open(url)
        speak_text("Opening Instagram.")

    # 12: open Twitter
    if there_exists(["open Twitter"], voice_data):
        search_term = voice_data.split("for")[-1]
        url = "https://twitter.com/"
        webbrowser.get().open(url)
        speak_text("Opening Twitter.")

    # 13: open Galiyaara
    if there_exists(["open Galiyaara"], voice_data):
        search_term = voice_data.split("for")[-1]
        url = "https://galiyaara-36629.web.app/"
        webbrowser.get().open(url)
        speak_text("Here's your Galiyaara.")

    # 14: show time table
    if there_exists(["show my time table"], voice_data):
        im = Image.open("image.jpeg")
        im.show()

    # 15: weather
    if there_exists(["weather", "tell me the weather report", "what's the condition outside"], voice_data):
        search_term = voice_data.split("for")[-1]
        url = "https://www.google.com/search?q=weather"
        webbrowser.get().open(url)
        speak_text("Here is what I found on weather.")

    # 16: open Gmail
    if there_exists(["open my mail", "Gmail", "check my email"], voice_data):
        search_term = voice_data.split("for")[-1]
        url = "https://mail.google.com/mail/u/0/#inbox"
        webbrowser.get().open(url)
        speak_text("Here you can check your Gmail.")

    # 17: game - rock paper scissor
    if there_exists(["game"], voice_data):
        voice_data = record_audio("Choose among rock, paper, or scissor.")
        moves = ["rock", "paper", "scissor"]
        cmove = random.choice(moves)
        pmove = voice_data
        speak_text("The computer chose " + cmove)
        speak_text("You chose " + pmove)
        if pmove == cmove:
            speak_text("The match is a draw.")
        elif pmove == "rock" and cmove == "scissor":
            speak_text("Player wins.")
        elif pmove == "rock" and cmove == "paper":
            speak_text("Computer wins.")
        elif pmove == "paper" and cmove == "rock":
            speak_text("Player wins.")
        elif pmove == "paper" and cmove == "scissor":
            speak_text("Computer wins.")
        elif pmove == "scissor" and cmove == "paper":
            speak_text("Player wins.")
        elif pmove == "scissor" and cmove == "rock":
            speak_text("Computer wins.")

    # 18: toss a coin
    if there_exists(["toss", "flip", "coin"], voice_data):
        moves = ["head", "tails"]
        cmove = random.choice(moves)
        speak_text("The computer chose " + cmove)

    # 19: calculator
    if there_exists(["plus", "minus", "multiply", "divide", "modulus", "power", "+", "-", "*", "/", "%", "**"], voice_data):
        opr = voice_data.split()[1]

        if opr == '+':
            speak_text(int(voice_data.split()[0]) + int(voice_data.split()[2]))
        elif opr == '-':
            speak_text(int(voice_data.split()[0]) - int(voice_data.split()[2]))
        elif opr == '*':
            speak_text(int(voice_data.split()[0]) * int(voice_data.split()[2]))
        elif opr == '/':
            speak_text(int(voice_data.split()[0]) / int(voice_data.split()[2]))
        elif opr == '%':
            speak_text(int(voice_data.split()[0]) % int(voice_data.split()[2]))
        elif opr == '**':
            speak_text(int(voice_data.split()[0]) ** int(voice_data.split()[2]))
        else:
            speak_text("Wrong Operator")

    # 20: take a screenshot
    if there_exists(["capture", "my screen", "screenshot"], voice_data):
        myScreenshot = pyautogui.screenshot()
        myScreenshot.save('screenshot.png')

person_obj = person()
asis_obj = asis()
asis_obj.name = 'ETERNITY'

def main():
    while True:
        voice_data = record_audio("Recording")  # Get the voice input
        respond(voice_data)

if __name__ == "__main__":
    main()
