import speech_recognition as sr
import webbrowser
import pyttsx3
import musiclib
import requests
from gtts import gTTS
import time
import pygame
import os

recognizer = sr.Recognizer()
engine = pyttsx3.init()
newsapi = "38694d0c75924caba97c295ba935012d"


def speak_old(text):
    engine.say(text)
    engine.runAndWait()

def speak(text):
    tts = gTTS(text)
    tts.save("temp.mp3")
   

    # Initialize pygame mixer
    pygame.mixer.init()

    # Load your mp3 file (use full path if not in same directory)
    pygame.mixer.music.load("temp.mp3")

    # Play the file
    pygame.mixer.music.play()

    # Keep the program running until the music finishes
    while pygame.mixer.music.get_busy():
        time.sleep(1)

    pygame.mixer.music.unload()
    os.remove("temp.mp3")

def processCommand(c):
    if "open google" in c.lower():
        speak("opening google")
        webbrowser.open("https://google.com")
    elif "open facebook" in c.lower():
        speak("opening facebook")
        webbrowser.open("https://facebook.com")
    elif "open youtube" in c.lower():
        speak("opening youtube")
        webbrowser.open("https://youtube.com")

    elif c.lower().startswith("play"):
        song = c.lower().split(" ")[1]
        link = musiclib.music[song]
        webbrowser.open(link)

    elif "news" in c.lower():
        r = requests.get(f"https://newsapi.org/v2/everything?q=apple&from=2025-08-02&to=2025-08-02&sortBy=popularity&apiKey={newsapi}")

        if r.status_code == 200:
            data = r.json()
            
            if data.get("status") == "ok":
                articles = data.get("articles", [])

                if articles:
                    speak("Here are the top news headlines.")
                    print("\nTop Headlines:\n")
                    for i, article in enumerate(articles[:5], start=1):  # Limit to top 5G
                        title = article.get('title', 'No title available.')
                        speak(f"Headline {i}: {title}")
                        time.sleep(1)  # Small pause between headlines
                else:
                    speak("Sorry, no news articles were found.")
            else:
                speak("There was an error with the news API.")
                print("News API error:", data.get("message", "Unknown error"))
        else:
            speak("Sorry, I couldn't fetch the news.")
            print(f"HTTP Error {r.status_code}: Could not fetch news.")

    else:
       # let openAI handle the request
       pass

    

if __name__ == "__main__":
    speak("Initializing Jerry....")
   
    while True:
        #listen for wake word "jerry"
        #obtain audio from microphone
        r = sr.Recognizer()

        
        

        print("Recognizing....")
        try:
            with sr.Microphone() as source:
              print("Listening...")
              audio = r.listen(source, timeout=2, phrase_time_limit=3)
            word = r.recognize_google(audio)
            if (word.lower() == "jerry"):
                print("Jerry is speaking....")
                speak("Yes")
                #listen for command
                with sr.Microphone() as source:
                  print("Jerry Active...")
                  audio = r.listen(source)
                  command = r.recognize_google(audio)

                  processCommand(command)

        except Exception as e:
            print("Error; {0}".format(e))