import speech_recognition as sr
import pyttsx3
import wikipedia
import datetime
import requests
import json
import os  # Import the standard os library
from dotenv import load_dotenv # Import the dotenv function

# 1. Load the variables from the .env file
load_dotenv()

# 2. Access the variables from the environment
# Use os.getenv() to retrieve the secrets
OPENWEATHERMAP_API_KEY = os.getenv("OPENWEATHERMAP_API_KEY")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")
WEATHER_CITY = os.getenv("WEATHER_CITY")
NEWS_COUNTRY_CODE = os.getenv("NEWS_COUNTRY_CODE")


# --- GLOBAL CONTEXT ---
LAST_SEARCH_TOPIC = None
TODO_FILE_PATH = "todo_list.txt" # File to store the persistent To-Do list

# --- CORE UTILITIES: TTS (Text-to-Speech) ---
try:
    engine = pyttsx3.init()
    engine.setProperty('rate', 170) 
except Exception as e:
    print(f"Error initializing TTS engine: {e}")
    class DummyEngine:
        def say(self, text):
            print(f"[TTS-ERROR] Assistant: {text}")
        def runAndWait(self):
            pass
    engine = DummyEngine()

def speak(audio):
    """Converts the given text (audio) to speech and plays it."""
    print(f"Assistant: {audio}")
    try:
        engine.say(audio)
        engine.runAndWait()
    except Exception as e:
        print(f"TTS Error: Could not speak audio. {e}")

# --- CORE UTILITIES: STT (Speech-to-Text) ---
def take_command():
    """Listens for the user's voice command and converts it to text."""
    r = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source, duration=0.5)
            print("Listening...")
            r.pause_threshold = 1
            # Added timeout/limit for robustness
            audio = r.listen(source, timeout=5, phrase_time_limit=10) 

        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in') 
        print(f"User said: {query}\n")
        return query.lower() 
    
    except sr.WaitTimeoutError:
        print("No speech detected within the time limit.")
        return "none"
    except sr.UnknownValueError:
        print("Sorry, I could not understand the audio.")
        return "none"
    except sr.RequestError as e:
        speak(f"I'm facing a request error. Please check your internet connection or Google Speech API limits. Error: {e}")
        return "none"
    except Exception as e:
        print(f"An unexpected STT error occurred: {e}")
        return "none"

# --- TO-DO LIST MANAGEMENT CLASS ---

class TaskLoader:
    """Handles the persistence of the to-do list using a simple text file."""
    def __init__(self, file_path):
        self.file_path = file_path
        self.tasks = self._load_tasks()

    def _load_tasks(self):
        """Loads tasks from the file upon initialization."""
        if not os.path.exists(self.file_path):
            return []
        try:
            with open(self.file_path, 'r') as f:
                # Read each line, strip whitespace, and filter out empty lines
                return [line.strip() for line in f if line.strip()]
        except Exception as e:
            print(f"Error loading tasks: {e}")
            return []

    def _save_tasks(self):
        """Saves the current list of tasks back to the file."""
        try:
            with open(self.file_path, 'w') as f:
                for task in self.tasks:
                    f.write(task + '\n')
        except Exception as e:
            print(f"Error saving tasks: {e}")
            speak("I had trouble saving your task list.")

    def add_task(self, task):
        """Adds a new task and saves the list."""
        self.tasks.append(task)
        self._save_tasks()
        speak(f"Task added: {task}")

    def get_tasks_summary(self):
        """Returns a spoken summary of the current tasks."""
        if not self.tasks:
            return "Your to-do list is currently empty. What task would you like to add?"
        
        task_summary = ["Here are your current to-do items:"]
        for i, task in enumerate(self.tasks, 1):
            task_summary.append(f"Number {i}: {task}.")
            
        return " ".join(task_summary)

    def clear_tasks(self):
        """Clears all tasks from memory and the file."""
        self.tasks = []
        self._save_tasks()
        speak("All tasks have been successfully cleared from your to-do list.")
        
# Initialize the Task Loader globally
TASK_MANAGER = TaskLoader(TODO_FILE_PATH)


# --- SMART ASSISTANT FUNCTIONS ---

def wish_me():
    """Wishes the user based on the time of day and introduces the assistant."""
    hour = int(datetime.datetime.now().hour)
    if 0 <= hour < 12:
        speak("Good Morning!")
    elif 12 <= hour < 18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")
    
    speak("I am your professional Python assistant. How may I help you today?")

def handle_wikipedia_search(query_term):
    """Encapsulates Wikipedia search logic."""
    global LAST_SEARCH_TOPIC
    
    if not query_term or query_term == 'search' or query_term == 'what is':
        speak("Please tell me what you would like to search for.")
        return

    try:
        speak(f"Searching Wikipedia for {query_term}...")
        results = wikipedia.summary(query_term, sentences=3) 
        speak(f"According to Wikipedia, about {query_term}.")
        speak(results)
        LAST_SEARCH_TOPIC = query_term # Update context on success
    except wikipedia.exceptions.PageError:
        speak(f"Sorry, I could not find anything about {query_term} on Wikipedia.")
        LAST_SEARCH_TOPIC = None 
    except wikipedia.exceptions.DisambiguationError:
        speak(f"The search for {query_term} is ambiguous. I will perform a Google search instead.")
        handle_google_search(query_term)
    except Exception as e:
        speak(f"An error occurred while searching Wikipedia. {e}")
        LAST_SEARCH_TOPIC = None

def handle_google_search(query_term):
    """Opens a Google search query in the default web browser."""
    if not query_term:
        speak("Please tell me what you would like to search for on Google.")
        return
        
    speak(f"Searching Google for {query_term}")
    search_url = f"https://www.google.com/search?q={query_term.replace(' ', '+')}"
    webbrowser.open(search_url)

def handle_weather_report():
    """Fetches and speaks the weather report."""
    if OPENWEATHERMAP_API_KEY == "YOUR_OPENWEATHERMAP_API_KEY":
        speak("To get the weather report, please update the script with your OpenWeatherMap API key and city name.")
        return
        
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={WEATHER_CITY}&appid={OPENWEATHERMAP_API_KEY}&units=metric"
        response = requests.get(url)
        data = response.json()
        
        if data["cod"] == 200:
            weather_desc = data["weather"][0]["description"]
            temp = data["main"]["temp"]
            humidity = data["main"]["humidity"]
            
            speak(f"The current weather in {WEATHER_CITY} is {weather_desc}, with a temperature of {temp} degrees Celsius, and humidity at {humidity} percent.")
        else:
            speak(f"Sorry, I could not retrieve the weather for {WEATHER_CITY}.")
    
    except requests.exceptions.RequestException:
        speak("I could not connect to the weather service. Please check your network connection.")
    except Exception as e:
        speak(f"An unexpected error occurred while fetching weather: {e}")

def handle_news_report():
    """Fetches and speaks the top news headlines."""
    if NEWS_API_KEY == "YOUR_NEWS_API_KEY_HERE":
        speak("To get the news, please update the script with your News API key.")
        return
        
    try:
        # NewsAPI endpoint for top headlines (country-specific)
        url = (
            f"https://newsapi.org/v2/top-headlines?country={NEWS_COUNTRY_CODE}&apiKey={NEWS_API_KEY}"
        )
        
        response = requests.get(url, timeout=10)
        response.raise_for_status() # Raise an HTTPError for bad responses (4xx or 5xx)
        data = response.json()
        
        articles = data.get("articles")
        
        if data["status"] == "ok" and articles:
            speak(f"Here are the top headlines for your region. News from various sources:")
            
            # Read out the first 3 headlines
            for i, article in enumerate(articles[:3]):
                title = article.get('title', 'A recent news story')
                source = article.get('source', {}).get('name', 'Unknown Source')
                
                # Clean up titles that end with the source name (common in news APIs)
                if f" - {source}" in title:
                    title = title.replace(f" - {source}", "").strip()

                speak(f"Headline number {i+1}: {title}.")
            
            speak("You can check a search engine for more details on these stories.")
            
        else:
            speak(f"Sorry, I could not retrieve any headlines right now. The API response was not successful.")
    
    except requests.exceptions.HTTPError as e:
        speak(f"Error accessing news service. Please check your API key or country code. Status: {e.response.status_code}")
    except requests.exceptions.RequestException:
        speak("I could not connect to the news service. Please check your network connection.")
    except Exception as e:
        speak(f"An unexpected error occurred while fetching news: {e}")
        
def process_command(query):
    """The central logic hub for handling user commands."""
    global LAST_SEARCH_TOPIC
    
    # --- TO-DO LIST COMMANDS (NEW) ---
    if 'add task' in query or 'to do' in query:
        # Extract the task after "add task" or "add to do"
        task = query.split('add task', 1)[-1].split('add to do', 1)[-1].strip()
        
        if task and task != 'list':
            TASK_MANAGER.add_task(task)
        else:
            speak("What task should I add to your list?")
            # Optionally, ask for the task again using take_command()

    elif 'show tasks' in query or 'what is on my list' in query:
        speak(TASK_MANAGER.get_tasks_summary())

    elif 'clear tasks' in query or 'delete all tasks' in query:
        TASK_MANAGER.clear_tasks()

    # --- Contextual Follow-up ---
    elif 'tell me more' in query or 'more about' in query:
        if LAST_SEARCH_TOPIC:
            speak(f"Searching for more information about {LAST_SEARCH_TOPIC}.")
            handle_wikipedia_search(LAST_SEARCH_TOPIC) 
        else:
            speak("I don't have a previous topic to follow up on. Please start a new search.")
            
    # --- Weather Command ---
    elif 'weather' in query:
        handle_weather_report()
            
     # --- NEWS COMMAND (NEW) ---
    elif 'read news' in query or 'latest news' in query or 'top headlines' in query:
        handle_news_report()
        
    # --- Wikipedia Search ---
    elif 'wikipedia' in query or 'who is' in query or 'what is' in query:
        query_term = query.replace("wikipedia", "").replace("search", "").replace("who is", "").replace("what is", "").strip()
        handle_wikipedia_search(query_term)
            
    # --- Google Search ---
    elif 'search google' in query or 'google for' in query:
        query_term = query.replace("search google", "").replace("google for", "").strip()
        handle_google_search(query_term)
    
    # --- System Time ---
    elif 'the time' in query:
        strTime = datetime.datetime.now().strftime("%I:%M %p")     
        speak(f"Sir, the current time is {strTime}")

    # --- Open Website/Application ---
    elif 'open youtube' in query:
        speak("Opening YouTube in your default browser.")
        webbrowser.open("youtube.com")
        
    elif 'open google' in query:
        speak("Opening Google in your default browser.")
        webbrowser.open("google.com")
        
    # Example: Open a specific application (Modify path for your system)
    elif 'open vs code' in query or 'open visual studio' in query:
        app_path = r"C:\Users\YourUser\AppData\Local\Programs\Microsoft VS Code\Code.exe" 
        
        if os.path.exists(app_path):
            os.startfile(app_path)
            speak("Opening Visual Studio Code.")
        else:
            speak("Sorry, I could not find the specified application path. Please update the path in the code.")
            
    # --- Final Exit Command ---
    elif 'exit' in query or 'quit' in query or 'stop listening' in query:
        speak("Goodbye! Shutting down the assistant.")
        return False # Signal to end the main loop
        
    # --- Fallback/Unknown Command ---
    elif query != "none":
        speak(f"I heard '{query}', but I am not programmed to handle that command yet.")
        
    return True # Signal to continue the main loop


# --- MAIN EXECUTION BLOCK ---
def main():
    """The entry point and main loop for the assistant application."""
    wish_me()
    running = True
    while running:
        query = take_command()
        
        if query != "none":
            running = process_command(query)

if __name__ == "__main__":
    main()