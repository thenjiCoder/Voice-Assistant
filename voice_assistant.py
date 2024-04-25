import speech_recognition as sr
from gtts import gTTS
import tempfile
import os
from playsound import playsound
import datetime
import requests

# Initialize the recognizer
recognizer = sr.Recognizer()

def speak(text):
    # Create a temporary file to save the synthesized speech audio
    with tempfile.NamedTemporaryFile(delete=False) as f:
        temp_audio_file = f.name
    
    # Use gTTS to synthesize speech from the text
    tts = gTTS(text=text, lang='en')
    tts.save(temp_audio_file)

     # Play the synthesized speech audio using playsound
    playsound(temp_audio_file)
    
    # Play the synthesized speech audio
    #os.system("mpg123 " + temp_audio_file)  # Use a suitable audio player command
    
    # Clean up the temporary audio file
    os.remove(temp_audio_file)

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
    
def web_search(query):
    api_key = 'AIzaSyALuInPbOCbhZhHwDYQysTfwd8z9G3XZ8w'  # Replace with your Google API key
    cse_id = '83e1f9fd494844e42'  # Replace with your Custom Search Engine ID
    url = f'https://www.googleapis.com/customsearch/v1?q={query}&key=AIzaSyALuInPbOCbhZhHwDYQysTfwd8z9G3XZ8w&cx=83e1f9fd494844e42'

    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            search_results = data.get('items', [])
            return search_results
        else:
            print("Error: Unable to fetch search results.")
    except Exception as e:
        print(f"Error: {e}")   

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
        elif "search" in query:
            # Extract the search query from the user's query
            search_query = query.replace("search", "").strip()
            # Perform web search and get results
            results = web_search(search_query)
            if results:
                speak("Here are the search results:")
                for result in results:
                    speak(result['title'])
            else:
                speak("Sorry, no search results found.")    
        else:
            speak("Sorry, I didn't catch that.")

if __name__ == "__main__":
    assistant()
