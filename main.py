import speech_recognition as sr
import pyttsx3 as pts
import spacy
import wikipedia as wk
import pywhatkit as pk
import sys
import os
from cfonts import render, say
os.system('cls')

global_var=0
listener = sr.Recognizer()
player = pts.init()
voice=player.getProperty('voices')
player.setProperty('voice',voice[1].id)
nlp = spacy.load('en_core_web_sm')
dictionary = ["terminate", "end", "stop", "quit", "exit","Bye"]


def listen():
    global global_var
    with sr.Microphone() as input_device:
        listener.adjust_for_ambient_noise(input_device)
        # Set timeout to 60 seconds
        try:
            voice_content = listener.listen(input_device, timeout=60)
            text_command = listener.recognize_google(voice_content)
            print(name+"   :"+ text_command)
            global_var=0
        except sr.UnknownValueError:
            global_var=global_var+1
            print("ChittiROBI: Unable to recognize speech.")
            if global_var>=4:
                print("See you later, Good Bye!")
                sys.exit()
            return None
    return text_command

def nextstep():
    with sr.Microphone() as input_device:
        voice("Do you want anything else?")
        print("chittiROBI: Do you want anything else?")
    run_voice()

def voice(text):
    player.say(text)
    player.runAndWait()

def answer_question(question):
    doc = nlp(question)
    # Perform NLP operations = that uses Wikipedia to answer the question
    query = ' '.join([token.text for token in doc if not token.is_stop])
    try:
        info = wk.summary(query, 2)
        print("chittiROBI:", info)
        voice(info)
    except wk.exceptions.DisambiguationError as e:
        print("chittiROBI: Multiple results found. Please provide more specific input.")
        voice("Multiple results found. Please provide more specific input.")
    except wk.exceptions.PageError:
        print("chittiROBI: No results found for the given query.")
        voice("No results found for the given query.")

def run_voice():
    while True:
        command = listen()
        if command is None:
            continue
        if "what is" in command:
            command = command.replace("what is", "")
            answer_question(command)
            nextstep()
        elif "play" in command:
            command = command.replace("play", "")
            try:
                pk.playonyt(command)
                nextstep()
            except pk.core.exceptions.InternetException:
                print("chittiROBI: Error connecting to the Internet. Please check your internet connection and try again.")
                sys.exit()
        elif any(word in command for word in dictionary):
            print("chittiROBI: Goodbye! Have a nice Day")
            voice("Goodbye!")
            sys.exit()
        else:
            answer_question(command)
            nextstep()

def greet(name):
    with sr.Microphone() as input_device:
        listener.adjust_for_ambient_noise(input_device)
        tex="Hello", name + ", I am ChittiRobi. How can I help you today?"
        voice(tex)
        print("chittiROBI: Hello", name + ", I am chittiROBI. How can I help you today?")
    run_voice()

# Replace the render() function with this code
print(render('Welcome to my World!', align='center', colors=['cyan', 'yellow'], font='simple'))
voice("Please enter your name?")
name=input("Please Enter your name: ")

greet(name)
