# 🎙️ Python Multi-Domain Assistant

### **Speak a command. Let Python handle the rest.**

A voice-controlled desktop assistant built with Python that combines **speech recognition, text-to-speech, web search, external APIs, Wikipedia, system utilities, and persistent task management** into one command-driven experience.

Instead of interacting with every service separately, the assistant creates a single conversational interface:

```text
                    🎙️ YOU SPEAK
                         │
                         ▼
                 Speech Recognition
                         │
                         ▼
                  Command Processing
                         │
        ┌────────────────┼────────────────┐
        ▼                ▼                ▼
     Knowledge         Live Data        Tasks
        │                │                │
        ▼                ▼                ▼
    Wikipedia       Weather / News    To-Do List
        │                │                │
        └────────────────┼────────────────┘
                         ▼
                    🗣️ Response
                         │
                         ▼
                   Text-to-Speech
```

---

# 🌐 One Assistant, Multiple Domains

The idea behind the project is simple:

> **You shouldn't need a separate interaction model for every small task.**

The assistant understands a collection of voice commands and routes them to the appropriate functionality.

```text
                 ┌──────────────────────────┐
                 │       USER COMMAND       │
                 └────────────┬─────────────┘
                              │
                              ▼
                    ┌──────────────────┐
                    │ Command Router   │
                    └────────┬─────────┘
                             │
       ┌──────────┬──────────┼───────────┬───────────┐
       ▼          ▼          ▼           ▼           ▼
    Search     Weather      News       Tasks       System
       │          │          │           │           │
       ▼          ▼          ▼           ▼           ▼
   Wikipedia   OpenWeather  NewsAPI   todo_list    Time
       │
       ▼
    Google
```

This makes the project less about a single feature and more about **connecting multiple Python capabilities into one workflow**.

---

# 🎧 The Interaction Loop

The assistant operates through a continuous listen → understand → act → respond cycle.

```text
          ┌───────────────────────┐
          │       Start App       │
          └───────────┬───────────┘
                      ▼
               👋 Wish the User
                      │
                      ▼
                🎤 Listen
                      │
                      ▼
             Speech → Text
                      │
                      ▼
              Process Command
                      │
             ┌────────┴────────┐
             │                 │
        Recognized?          No
             │                 │
             ▼                 ▼
          Execute          Try Again
          Command
             │
             ▼
          Respond
             │
             ▼
       Text → Speech
             │
             ▼
       Continue Listening
```

The main loop continues until an exit command is received.

---

# 🗣️ Speech In → Speech Out

The project uses two sides of the voice interaction.

### 🎤 Speech Recognition

The `SpeechRecognition` library captures microphone input and uses the **Google Web Speech API** to convert speech into text.

```text
🎙️ Microphone
      │
      ▼
Audio Input
      │
      ▼
SpeechRecognition
      │
      ▼
Google Speech Recognition
      │
      ▼
Text Command
```

The recognizer also adjusts for ambient noise before listening and uses time limits so the assistant doesn't wait indefinitely.

---

### 🔊 Text-to-Speech

Once the assistant decides what to say, `pyttsx3` converts the response into spoken output.

```text
Python Response
      │
      ▼
   pyttsx3
      │
      ▼
🔊 Spoken Response
```

The assistant also prints its response to the terminal, making the application usable even when audio output needs troubleshooting.

---

# 🧭 Command Routing

The heart of the assistant is:

```python
process_command(query)
```

This function acts as the **central command router**.

A simplified view:

```text
                        query
                          │
                          ▼
                  process_command()
                          │
       ┌──────────────────┼──────────────────┐
       │                  │                  │
       ▼                  ▼                  ▼
    "weather"          "latest news"      "add task"
       │                  │                  │
       ▼                  ▼                  ▼
 Weather Handler      News Handler       Task Manager
```

Other commands are routed toward:

* Wikipedia
* Google Search
* Time
* YouTube
* Google
* Visual Studio Code
* Follow-up searches
* Exit handling

---

# 🧠 A Little Bit of Context

One particularly useful feature is the assistant's ability to remember the **last successful Wikipedia search topic** during the current session.

For example:

```text
You:
"Who is Alan Turing?"

        ↓

Assistant:
Wikipedia search → Alan Turing
        ↓
LAST_SEARCH_TOPIC = "alan turing"

        ↓

You:
"Tell me more"

        ↓

Assistant:
Searches the previous topic again
```

The flow is:

```text
First Search
     │
     ▼
LAST_SEARCH_TOPIC
     │
     ▼
"Tell me more"
     │
     ▼
Reuse Previous Topic
```

This creates a small conversational layer without requiring a database or a large language model.

---

# 📚 Knowledge Mode

For general knowledge queries, the assistant uses Wikipedia.

Commands such as:

```text
"Who is Albert Einstein?"
"What is Python?"
"Search Wikipedia for NASA"
```

are routed through the Wikipedia handler.

The assistant requests a short summary:

```python
wikipedia.summary(query_term, sentences=3)
```

and reads the result aloud.

If Wikipedia returns an ambiguous result, the assistant falls back toward Google search behavior.

---

# 🔎 Search Mode

The assistant can also open Google searches directly.

```text
Voice Command
      │
      ▼
"Search Google for Python decorators"
      │
      ▼
Build Search URL
      │
      ▼
Open Default Browser
```

It can also launch common websites through commands such as:

```text
"Open YouTube"
"Open Google"
```

The browser is therefore treated as another tool available to the assistant.

---

# 🌦️ Live Weather

The weather module connects the assistant to **OpenWeatherMap**.

```text
                  Weather Command
                        │
                        ▼
                OpenWeatherMap API
                        │
                        ▼
              ┌──────────────────┐
              │ Weather Response  │
              └────────┬─────────┘
                       │
              ┌────────┼─────────┐
              ▼        ▼         ▼
          Condition  Temp.    Humidity
              │        │         │
              └────────┼─────────┘
                       ▼
                 Spoken Report
```

The city and API key are loaded from environment variables rather than being hard-coded into the application.

---

# 📰 News Mode

The assistant can fetch top headlines using **NewsAPI**.

It retrieves the latest available headlines for the configured country and reads the first three stories.

```text
"Read latest news"
        │
        ▼
     NewsAPI
        │
        ▼
 Top Headlines
        │
        ▼
 First 3 Stories
        │
        ▼
🔊 Read Aloud
```

This makes the assistant useful not only for commands and static knowledge, but also for selected real-time information.

---

# ✅ A To-Do List That Remembers

The project also contains a lightweight persistent task manager.

Instead of keeping tasks only in memory, the assistant stores them in:

```text
todo_list.txt
```

The architecture is:

```text
Voice Command
      │
      ▼
TaskManager
      │
 ┌────┼─────────────┐
 ▼    ▼             ▼
Add  Show          Clear
 │    │             │
 └────┼─────────────┘
      ▼
todo_list.txt
```

Supported operations include:

### ➕ Add

```text
"Add task complete Python project"
```

### 📋 Show

```text
"Show tasks"
```

### 🗑️ Clear

```text
"Clear tasks"
```

Tasks are loaded when the assistant starts and saved back to the text file when changes are made.

---

# 🧩 The Task Manager

The task functionality is encapsulated inside:

```python
class TaskLoader:
```

It handles:

```text
             TaskLoader
                 │
       ┌─────────┼─────────┐
       ▼         ▼         ▼
    Load       Add       Clear
    Tasks      Task      Tasks
       │         │         │
       └─────────┼─────────┘
                 ▼
           Save to File
```

This separation keeps task persistence independent from the main command-processing logic.

---

# ⏰ System Utilities

The assistant also provides simple system-oriented commands.

For example:

```text
"What is the time?"
```

returns the current system time.

The assistant also greets the user differently depending on the current hour:

```text
00:00 ── 11:59  → Good Morning
12:00 ── 17:59  → Good Afternoon
18:00 ── 23:59  → Good Evening
```

It's a small detail, but it gives the interaction a more natural starting point.

---

# 🛡️ Error Handling

Voice applications depend on external hardware and services, so failures are expected.

The assistant includes handling for situations such as:

### 🎤 No speech detected

A timeout prevents indefinite listening.

### ❓ Speech not understood

The assistant safely returns `"none"` and continues.

### 🌐 Speech API request failure

The assistant provides an internet/API-related error message.

### 📖 Wikipedia page not found

The assistant reports that no matching page was found.

### 🔀 Wikipedia ambiguity

The assistant can redirect the search toward Google.

### 🌦️ Weather API failure

Network/API failures are caught and converted into spoken feedback.

### 📰 News API failure

HTTP and network errors are handled separately.

### 🔊 TTS failure

A fallback dummy engine prevents the application from crashing solely because text-to-speech initialization fails.

---

# 🔐 Keeping API Keys Out of the Code

The project uses environment variables for external service credentials.

```text
                  .env
                   │
        ┌──────────┴──────────┐
        ▼                     ▼
 Weather API Key          News API Key
        │                     │
        └──────────┬──────────┘
                   ▼
              Python App
```

The application reads them using:

```python
load_dotenv()

OPENWEATHERMAP_API_KEY = os.getenv("OPENWEATHERMAP_API_KEY")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")
```

This is a much safer approach than placing API keys directly inside the source code.

**Never commit your real `.env` file or API keys to GitHub.**

---

# 🏗️ Project Architecture

The project can be viewed as several small systems working together:

```text
                         🎙️ USER
                            │
                            ▼
                    Speech Recognition
                            │
                            ▼
                    Command Processing
                            │
        ┌───────────┬───────┼───────┬───────────┐
        ▼           ▼       ▼       ▼           ▼
    Wikipedia    Google   Weather  News       Tasks
        │           │       │       │           │
        ▼           ▼       ▼       ▼           ▼
     Knowledge    Browser  API     API      Local File
        │           │       │       │           │
        └───────────┴───────┼───────┴───────────┘
                            ▼
                     Response Generation
                            │
                            ▼
                      🖥️ Terminal
                            +
                         🔊 TTS
```

---

# 📂 Project Structure

```text
python-multi-domain-assistant/
│
├── 📄 assistant.py
├── 📄 requirements.txt
├── 📄 .gitignore
├── 📄 README.md
│
└── 📝 todo_list.txt
    └── Created/used when tasks are persisted
```

### `assistant.py`

The main application containing:

* speech recognition
* text-to-speech
* command routing
* Wikipedia search
* Google search
* weather
* news
* task management
* contextual follow-ups
* application/website launching

### `requirements.txt`

Contains the Python packages required by the current project setup.

### `.gitignore`

Used to prevent sensitive/local files from being committed.

### `todo_list.txt`

Local persistent storage for the assistant's tasks.

---

# 🛠️ Technology Palette

| Technology               | What It Does              |
| ------------------------ | ------------------------- |
| 🐍 **Python**            | Core application          |
| 🎤 **SpeechRecognition** | Converts speech into text |
| 🔊 **pyttsx3**           | Text-to-speech            |
| 📖 **Wikipedia**         | Knowledge retrieval       |
| 🌐 **Requests**          | HTTP/API communication    |
| 🌦️ **OpenWeatherMap**   | Weather information       |
| 📰 **NewsAPI**           | News headlines            |
| 🔐 **python-dotenv**     | Environment configuration |
| 💾 **Text File Storage** | Persistent task list      |

---

# ⚙️ Setup

## 1. Clone the repository

```bash
git clone https://github.com/taniiishaa/Python-Multi-Domain-Assistant.git
cd Python-Multi-Domain-Assistant
```

## 2. Create a virtual environment

```bash
python -m venv venv
```

### Windows

```bash
.\venv\Scripts\activate
```

### Linux / macOS

```bash
source venv/bin/activate
```

---

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

> **Note:** The current `requirements.txt` primarily contains the voice/Windows dependencies. The source code also imports `requests`, `wikipedia`, and `python-dotenv`, so make sure those packages are installed as well if they are not already available in your environment.

```bash
pip install requests wikipedia python-dotenv
```

---

# 🔑 Configure External APIs

Create a local file named:

```text
.env
```

in the project root.

Example:

```env
OPENWEATHERMAP_API_KEY="YOUR_OPENWEATHERMAP_API_KEY"
NEWS_API_KEY="YOUR_NEWS_API_KEY"
WEATHER_CITY="Your City"
NEWS_COUNTRY_CODE="in"
```

Keep this file private.

```text
.env
  ↓
LOCAL ONLY 🔒
  ↓
Never commit to GitHub
```

---

# ▶️ Launch the Assistant

Run:

```bash
python assistant.py
```

You should see the assistant greet you and begin listening for commands.

Example interaction:

```text
Assistant: Good Afternoon!
Assistant: I am your professional Python assistant.
Assistant: How may I help you today?

Listening...
Recognizing...

User said: what is artificial intelligence

Assistant: Searching Wikipedia for artificial intelligence...
Assistant: According to Wikipedia...
```

---

# 🎙️ Example Commands

The assistant understands several command patterns.

### 📚 Knowledge

```text
"Who is Alan Turing?"
"What is artificial intelligence?"
"Search Wikipedia for Python"
```

### 🔎 Web

```text
"Search Google for Python projects"
"Google for machine learning tutorials"
```

### 🌦️ Weather

```text
"What's the weather?"
```

### 📰 News

```text
"Read latest news"
"Show top headlines"
```

### ⏰ Time

```text
"What is the time?"
```

### ✅ Tasks

```text
"Add task finish assignment"
"Show tasks"
"Clear tasks"
```

### 🌐 Websites

```text
"Open YouTube"
"Open Google"
```

### 🔁 Context

```text
"Tell me more"
"More about it"
```

### 🛑 Exit

```text
"Exit"
"Quit"
"Stop listening"
```

---

# 💡 Why This Project Matters

This project brings together several areas of Python development that are often explored separately:

```text
       Python Fundamentals
               │
       ┌───────┼────────┐
       ▼       ▼        ▼
    APIs     Files    Automation
       │       │        │
       └───────┼────────┘
               ▼
        Voice Interfaces
               │
       ┌───────┴───────┐
       ▼               ▼
 Speech → Text      Text → Speech
       │               │
       └───────┬───────┘
               ▼
        Personal Assistant
```

It demonstrates how Python can act as the **glue between multiple technologies and services**.

---

# 🧠 Key Learning Areas

Through this project, the implementation explores:

* 🎤 Speech recognition
* 🔊 Text-to-speech
* 🧭 Command routing
* 🌐 REST API integration
* 🔐 Environment-variable based configuration
* 📖 External knowledge retrieval
* 💾 File-based persistence
* 🧱 Object-oriented task management
* ⚠️ Exception handling
* 🖥️ Desktop/browser automation
* 🔁 Lightweight conversational context

---

# ⚠️ Current Limitations

This assistant is intentionally a rule-based Python assistant rather than a general-purpose conversational AI.

The command router relies on keyword matching such as:

```python
if 'weather' in query:
```

and:

```python
elif 'latest news' in query:
```

That means the assistant can only respond to commands that its current logic knows how to handle.

It does **not** currently provide:

* LLM-based conversation
* unrestricted natural-language reasoning
* long-term conversational memory
* a graphical desktop interface
* user accounts
* database-backed task management

The project is therefore best understood as a **Python voice automation assistant and integration project**.

---

# 🚀 Future Evolution

The architecture leaves plenty of room to grow.

```text
             CURRENT ASSISTANT
                    │
                    ▼
          Rule-Based Commands
                    │
          ┌─────────┼─────────┐
          ▼         ▼         ▼
        APIs      Tasks     Search
                    │
                    ▼
             ┌─────────────┐
             │ NEXT LEVEL  │
             └──────┬──────┘
                    │
       ┌────────────┼────────────┐
       ▼            ▼            ▼
      LLM        Memory       Plugins
       │            │            │
       ▼            ▼            ▼
 Natural Language  Context    More Tools
       │            │            │
       └────────────┼────────────┘
                    ▼
            🤖 Intelligent
             Assistant
```

Potential future improvements:

* 🤖 LLM-powered natural-language command understanding
* 🧠 persistent conversation memory
* 🗣️ more natural conversational responses
* 🖥️ graphical interface
* 📅 calendar integration
* 📧 email integration
* 🗂️ richer task management
* 🔌 modular tool/plugin architecture
* ⚡ asynchronous API operations
* 🔐 improved configuration and secret handling
* ☁️ deployment as a service

---

# 🌱 From Voice Commands to Intelligent Agents

The most interesting part of this project isn't the individual APIs.

It's the architecture.

Today:

```text
Voice
  ↓
Keyword Matching
  ↓
Specific Function
  ↓
Response
```

A future agent-oriented version could become:

```text
Voice
  ↓
Natural Language Understanding
  ↓
Intent + Context
  ↓
Choose Appropriate Tool
  ↓
Execute Tool
  ↓
Interpret Result
  ↓
Respond Naturally
```

That transition moves the project from a **command-based assistant** toward a more flexible **tool-using AI assistant**.

---

<p align="center">
  <b>🎙️ Python · 🔊 Voice AI · 🌐 APIs · 🤖 Automation · 🧠 NLP · ⚙️ Python Development</b>
</p>

<p align="center">
  <i>Listen. Understand. Execute. Respond.</i>
</p>
