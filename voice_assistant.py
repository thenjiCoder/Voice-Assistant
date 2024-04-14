import speech_recognition as sr
import pyttsx3
import datetime

# Initialize the recognizer
recognizer = sr.Recognizer()

# Initialize the text-to-speech engine
engine = pyttsx3.init()

# Adjust parameters to make the voice sound more human and clean
#engine.setProperty('rate', 140)  # Adjust the speech rate (words per minute)
#engine.setProperty('volume', 0.5)  # Adjust the volume (0.0 to 1.0)
#engine.setProperty('voice', 'english')  # Select a specific voice (if available)


# Function to speak the given text
def speak(text):
    engine.say(text)
    engine.runAndWait()

def listen():
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        print("Recognizing...")
        query = recognizer.recognize_google(audio)
        print("User said:", query)
        return query.lower()
    except sr.UnknownValueError:
        print("Sorry, I didn't catch that.")
        return ""
    except sr.RequestError:
        print("Sorry, couldn't request results at the moment.")
        return ""

def assistant():
    speak("Hello! How can I help you today?")
    while True:
        query = listen()
        if "hello" in query:
            speak("Hi there!")
        elif "bye" in query:
            speak("Goodbye!")
            break
        elif "time" in query:
            current_time = datetime.datetime.now().strftime("%I:%M %p")
            speak(f"The current time is {current_time}")
        elif "date" in query:
            current_date = datetime.datetime.now().strftime("%A, %B %d, %Y")
            speak(f"Today's date is {current_date}")
        else:
            speak("Sorry, I didn't understand that command.")

if __name__ == "__main__":
    assistant()