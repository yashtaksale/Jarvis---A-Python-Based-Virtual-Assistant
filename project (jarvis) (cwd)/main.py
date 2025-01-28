import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
import requests
import openai
from gtts import gTTS
import pygame
import os


recognizer = sr.Recognizer()
engine = pyttsx3.init()
newsapi = "<enter your key>"

def speak_old(text):
    engine.say(text)
    engine.runAndWait()

def speak(text):
    tts = gTTS(text)
    tts.save('temp.mp3') 

    pygame.mixer.init()

    pygame.mixer.music.load('temp.mp3')

    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    
    pygame.mixer.music.unload()
    os.remove("temp.mp3") 

def aiProcess(command):
    try:
        client = openai(api_key="<enter your key")

        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a virtual assistant named Jarvis skilled in general tasks like Alexa and Google Cloud. Give short responses please"},
                {"role": "user", "content": command}
            ]
        )

        return completion.choices[0].message.content

    except Exception as e:
        speak("Sorry, I had trouble communicating with the AI service. Please try again.")
        print(f"AI Process Error: {str(e)}")
        return "Sorry, I had trouble communicating with the AI service."

def processCommand(c):
    try:
        if "open google" in c.lower():
            webbrowser.open("https://google.com")
            speak("Opening Google")
        elif "open facebook" in c.lower():
            webbrowser.open("https://facebook.com")
            speak("Opening Facebook")
        elif "open youtube" in c.lower():
            webbrowser.open("https://youtube.com")
            speak("Opening YouTube")
        elif "open linkedin" in c.lower():
            webbrowser.open("https://linkedin.com")
            speak("Opening LinkedIn")
        elif c.lower().startswith("play"):
            song = c.lower().split(" ")[1]
            if song in musicLibrary.music:
                webbrowser.open(musicLibrary.music[song])
                speak(f"Playing {song}")
            else:
                speak(f"Sorry, I couldn't find the song: {song}")
        elif "news" in c.lower():
            r = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey={newsapi}")
            if r.status_code == 200:
                data = r.json()
                
                articles = data.get('articles', [])
                
                if articles:
                    for article in articles[:5]:  
                        speak(article['title'])
                else:
                    speak("Sorry, I couldn't find any news.")
            else:
                speak("Sorry, I couldn't fetch the news at the moment.")
        else:
            output = aiProcess(c)
            speak(output)
    
    except Exception as e:
        speak("Sorry, I encountered an issue while processing the command.")
        print(f"Command Processing Error: {str(e)}")

if __name__ == "__main__":
    speak("Initializing Jarvis... I'm ready to assist you. Just say 'Jarvis' to begin.")
    
    while True:
        try:
            with sr.Microphone() as source:
                print("Listening for wake word...")
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=3)
            
            word = recognizer.recognize_google(audio)
            if word.lower() == "jarvis":
                speak("Yes, how can I assist you?")
                
                with sr.Microphone() as source:
                    print("Jarvis is active. Please give a command...")
                    audio = recognizer.listen(source)
                
                command = recognizer.recognize_google(audio)
                print(f"Command received: {command}")
                
                processCommand(command)
        
        except sr.UnknownValueError:
            print("Could not understand the audio.")
            speak("Sorry, I didn't catch that. Please repeat.")
        except sr.RequestError:
            print("Could not request results from Google Speech Recognition service.")
            speak("Sorry, I couldn't process your request. Please try again.")
        except Exception as e:
            print(f"Error: {str(e)}")
            speak(f"An error occurred: {e}")
