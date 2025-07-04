import schedule
import time
import threading
import pyttsx3

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def speak_reminder(task):
    print(f"[Reminder Triggered] {task}")
    speak(f"Reminder: {task}")

def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)

def start_reminder_thread():
    thread = threading.Thread(target=run_scheduler, daemon=True)
    thread.start()

# ✅ START scheduler thread
start_reminder_thread()

# ✅ ADD a test reminder (fires in 10 seconds)
schedule.every(10).seconds.do(speak_reminder, "Test reminder: take a break.")

speak("Reminder test started.")

# ✅ Keep main thread alive
while True:
    time.sleep(1)