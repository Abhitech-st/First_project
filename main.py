import speech_recognition as sr
import pyttsx3
import os
import subprocess
import wikipedia
import requests
import webbrowser
import schedule
import time
import threading

#Initialize speech to text system
engine = pyttsx3.init()
engine.setProperty("rate", 170)  # Speech speed
engine.setProperty("volume", 1.0)

def speak(text):
    print("JARVIS:", text)
    engine.say(text)
    engine.runAndWait()

def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎙️ Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    
    try:
        command = recognizer.recognize_google(audio)
        print("You said:", command)
        return command.lower()
    except sr.UnknownValueError:
        speak("Sorry, I didn’t catch that")
        return ""
    except sr.RequestError:
        speak("Network error. Please check your internet.")
        return ""
    
def remember(key, value):
    with open("memory.json", "r+") as file:
        data = json.load(file)
        data[key] = value
        file.seek(0)
        json.dump(data, file, indent=4)

def recall(key):
    with open("memory.json", "r") as file:
        data = json.load(file)
        return data.get(key)
def speak_reminder(task):
    speak(f"Reminder: {task}")

def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)

def start_reminder_thread():
    thread = threading.Thread(target=run_scheduler, daemon=True)
    thread.start()

# Main loop
speak("Hello! I am your JARVIS assistant.")
start_reminder_thread()
while True:
    query = listen()
    
    if "exit" in query or "stop" in query:
        speak("Goodbye!")
        break
    elif "your name" in query:
        speak("I am JARVIS, your voice assistant.")
    elif "open notepad" in query:
        speak("Opening Notepad")
        os.system("notepad")

    elif "open calculator" in query:
        speak("Opening Calculator")
        subprocess.Popen("calc.exe")

    elif "open command prompt" in query or "open terminal" in query:
        speak("Opening command prompt")
        os.system("start cmd")

    elif "play music" in query:
        try:
            music_path = "C:/Users/NCL/Music"  # replace with actual file path
            speak("Playing your music")
            os.startfile(music_path)
        except OSError:
            speak("There is no music yet")

    elif "wikipedia" in query:
        try:
            topic = query.replace("search wikipedia for", "").replace("wikipedia", "")
            speak("Searching Wikipedia for " + topic)
            result = wikipedia.summary(topic, sentences=2)
            speak(result)
        except Exception:
            speak("Sorry, I couldn't find anything on Wikipedia.")

    elif "tell me a joke" in query:
        try:
            response = requests.get("https://icanhazdadjoke.com/", headers={"Accept": "application/json"})
            joke = response.json()["joke"]
            speak(joke)
        except:
            speak("Sorry, I couldn't fetch a joke right now.")

    elif "weather in" in query:
        city = query.split("in")[-1].strip()
        api_key = "37d44c36a578e232c80dc252b3272fbf"  # I'll help you get this
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        response = requests.get(url).json()
        if response["cod"] == 200:
            temp = response["main"]["temp"]
            desc = response["weather"][0]["description"]
            speak(f"The temperature in {city} is {temp}°C with {desc}")
        else:
            speak("City not found.")

    elif "google" in query:
        search_term = query.replace("google", "").strip()
        webbrowser.open(f"https://www.google.com/search?q={search_term}")
        speak(f"Searching Google for {search_term}")

    elif "youtube" in query:
        topic = query.replace("search youtube for", "").strip()
        webbrowser.open(f"https://www.youtube.com/results?search_query={topic}")
        speak(f"Searching YouTube for {topic}")

    elif "shutdown" in query:
        speak("Shutting down the system")
        os.system("shutdown /s /t 1")

    elif "restart" in query:
        speak("Restarting the system")
        os.system("shutdown /r /t 1")

    elif "how are you" in query:
        speak("I'm functioning within normal parameters. Thank you.")
    elif "time" in query:
        from datetime import datetime
        speak("The current time is " + datetime.now().strftime("%I:%M %p"))
    elif "my name is" in query:
        name = query.replace("my name is", "").strip()
        remember("name", name)
        speak(f"Okay, I will remember your name is {name}")

    elif "what's my name" in query or "what is my name" in query:
        name = recall("name")
        if name:
            speak(f"Your name is {name}")
        else:
            speak("I don’t know your name yet.")
    elif "tell me the news" in query or "news" in query:
        api_key = "2cb0500ba6434b55b4c93f793ffdeb3e"  # Replace with your actual key
        url = f"https://newsapi.org/v2/top-headlines?country=in&apiKey={api_key}"
    
        try:
            news = requests.get(url).json()
            articles = news["articles"][:5]  # Get top 5 headlines
            
            for i, article in enumerate(articles):
                title = article["title"]
                speak(f"News {i+1}: {title}")
        except Exception as e:
            print("News error:", e)
            speak("Sorry, I couldn't fetch the news.")
    elif "meaning of" in query or "define" in query or "what does" in query:
        try:
            # Extract the word to define
            if "meaning of" in query:
                word = query.split("meaning of")[-1].strip()
            elif "define" in query:
                word = query.split("define")[-1].strip()
            elif "what does" in query:
                word = query.replace("what does", "").replace("mean", "").strip()
            else:
                word = ""

            url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
            response = requests.get(url)
            data = response.json()

            if isinstance(data, list):
                definition = data[0]['meanings'][0]['definitions'][0]['definition']
                example = data[0]['meanings'][0]['definitions'][0].get('example')
                speak(f"The meaning of {word} is: {definition}")
                if example:
                    speak(f"For example: {example}")
            else:
                speak(f"Sorry, I couldn't find the meaning of {word}.")
        except Exception as e:
            print("Dictionary error:", e)
            speak("Something went wrong while fetching the meaning.")
    elif "remind me" in query:
        try:
            if "in" in query and "to" in query:
                time_part = query.split("in")[1].split("to")[0].strip()
                task = query.split("to")[-1].strip()

                if "minute" in time_part or "minutes" in time_part:
                    minutes = int(''.join(filter(str.isdigit, time_part)))
                    schedule.every(minutes).minutes.do(speak_reminder, task).tag(task)
                    speak(f"Okay, I will remind you to {task} in {minutes} minute{'s' if minutes > 1 else ''}")
                
                elif "second" in time_part or "seconds" in time_part:
                    seconds = int(''.join(filter(str.isdigit, time_part)))
                    schedule.every(seconds).seconds.do(speak_reminder, task).tag(task)
                    speak(f"Okay, I will remind you to {task} in {seconds} second{'s' if seconds > 1 else ''}")
                
                else:
                    speak("Sorry, I can only set reminders in seconds or minutes for now.")
        except:
            speak("I couldn’t understand that. Please try again.")
    elif query:
        speak("You said: " + query)