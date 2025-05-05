
import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia
import webbrowser
import os
import time
import random
import subprocess
from ecapture import ecapture as ec
import wolframalpha
import pyautogui
import requests


print('Loading your personal assistant')

engine=pyttsx3.init('sapi5')
voices=engine.getProperty('voices')
engine.setProperty('voice','voices[1].id')


def speak(text):
    engine.say(text)
    engine.runAndWait()

def wishMe():
    hour=datetime.datetime.now().hour
    if hour>=0 and hour<12:
        speak("Hello,Good Morning")
        print("Hello,Good Morning")
    elif hour>=12 and hour<18:
        speak("Hello,Good Afternoon")
        print("Hello,Good Afternoon")
    else:
        speak("Hello,Good Evening")
        print("Hello,Good Evening")

def takeCommand():
    r = sr.Recognizer()
    r.dynamic_energy_threshold = True
    r.energy_threshold = 300
    r.pause_threshold = 0.8

    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=0.5)
        print("Listening...")
        audio = r.listen(source, phrase_time_limit=5)

    try:
        statement = r.recognize_google(audio, language='en-in')
        print(f"user said: {statement}")
        speak(f"user said: {statement}")
        return statement
    except sr.UnknownValueError:
        print("Could not understand audio")
        speak("Could not understand audio")
        return ""
    except sr.RequestError as e:
        print(f"Could not request results; {e}")
        speak("Could not understand audio")
        return ""
    
def game_play():
    speak("Let's play Rock Paper Scissors! Best of five rounds.")
    choices = ["rock", "paper", "scissors"]
    user_score = 0
    comp_score = 0

    for i in range(5):
        speak(f"Round {i+1}. Please say rock, paper, or scissors.")
        user_choice = takeCommand().lower()
        comp_choice = random.choice(choices)

        if user_choice not in choices:
            speak("Invalid choice, round forfeited.")
        else:
            speak(f"You chose {user_choice}, computer chose {comp_choice}.")
            if user_choice == comp_choice:
                speak("It's a tie.")
            elif (user_choice=="rock" and comp_choice=="scissors") or \
                 (user_choice=="paper" and comp_choice=="rock") or \
                 (user_choice=="scissors" and comp_choice=="paper"):
                speak("You win this round.")
                user_score += 1
            else:
                speak("Computer wins this round.")
                comp_score += 1

    speak(f"Final score: You {user_score}, Computer {comp_score}.")
    if user_score > comp_score:
        speak("Congratulations, you won the game!")
    elif comp_score > user_score:
        speak("Computer won the game. Better luck next time.")
    else:
        speak("The game is a tie.")

def search_youtube(query):
    query = query.strip()
    webbrowser.open_new_tab(f"https://www.youtube.com/results?search_query={query}")
    speak(f"Searching YouTube for {query}")
    time.sleep(5)

def search_google(query):
    query = query.strip()
    webbrowser.open_new_tab(f"https://www.google.com/search?q={query}")
    speak(f"Searching Google for {query}")
    time.sleep(5)

def close_current_window():
    speak("Closing the current window")
    pyautogui.hotkey('alt', 'f4')

speak("Loading your personal assistant")
wishMe()


if __name__=='__main__':


    while True:
        speak("Tell me how can I help you now?")
        statement = takeCommand().lower()
        if statement==0:
            continue

        if "good bye" in statement or "ok bye" in statement or "stop" in statement:
            speak('your personal assistant shutting down,Good bye')
            print('your personal assistant is shutting down,Good bye')
            break

        elif 'play game' in statement or 'rock paper scissors' in statement:
            game_play()    

        if 'wikipedia' in statement:
            speak('Searching Wikipedia...')
            statement =statement.replace("wikipedia", "")
            results = wikipedia.summary(statement, sentences=3)
            speak("According to Wikipedia")
            print(results)
            speak(results)

        elif 'open youtube' in statement:
            webbrowser.open_new_tab("https://www.youtube.com")
            speak("youtube is open now")
            time.sleep(5)

        elif 'open google' in statement:
            webbrowser.open_new_tab("https://www.google.com")
            speak("Google chrome is open now")
            time.sleep(5)

        elif 'open gmail' in statement:
            webbrowser.open_new_tab("gmail.com")
            speak("Google Mail open now")
            time.sleep(5)


        elif 'time' in statement:
            strTime=datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"the time is {strTime}")

        elif 'who are you' in statement or 'what can you do' in statement:
            speak("I am a personal assistant created by Waqas Anwar. I can help you with searching, calculations, playing games, taking screenshots, and more.")
            print("I am a personal assistant created by Waqas Anwar. I can help you with searching, calculations, playing games, taking screenshots, and more.")

        elif "who made you" in statement or "who created you" in statement or "who discovered you" in statement:
            speak("I was built by Waqas Anwar")
            print("I was built by Waqas Anwar")

        elif 'search youtube' in statement:
            query = statement.replace("search youtube", "").strip()
            search_youtube(query)

        elif 'search google' in statement:
            query = statement.replace("search google", "").strip()
            search_google(query)

        
        elif "camera" in statement or "take a photo" in statement:
            ec.capture(0,"robo camera","img.jpg")

        elif 'search'  in statement:
            statement = statement.replace("search", "")
            webbrowser.open_new_tab(statement)
            time.sleep(5)

        elif 'ask' in statement:
            speak('I can answer to computational and geographical questions and what question do you want to ask now')
            question=takeCommand()
            app_id="R2K75H-7ELALHR35X"
            client = wolframalpha.Client('R2K75H-7ELALHR35X')
            res = client.query(question)
            answer = next(res.results).text
            speak(answer)
            print(answer)


        elif "log off" in statement or "sign out" in statement:
            speak("Ok , your pc will log off in 10 sec make sure you exit from all applications")
            subprocess.call(["shutdown", "/l"])

        elif "close" in statement or "back" in statement:
            close_current_window()


time.sleep(3)