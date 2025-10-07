# Multimodal Voice Assistant Project (Python)

A powerful, multi-domain desktop assistant built entirely in Python, demonstrating proficiency in natural language processing (NLP), external API integration, and modular software design. This project was developed as a core deliverable during the CodexIntern Internship.

## 🚀 Key Features Demonstrated

* **Speech Recognition (ASR):** Utilizes the `speech_recognition` library and Google Web Speech API to convert real-time microphone input into actionable text commands.
* **Text-to-Speech (TTS):** Provides natural language feedback using the `pyttsx3` engine for a complete voice-user experience.
* **Secure API Integration:** Implements secure retrieval of external data (Weather, News) using `requests` and follows best practices for secret management (`python-dotenv` and `.gitignore`).
* **Multi-Domain Intelligence:** Handles commands across various domains:
    * **Real-time Weather Forecasts** (OpenWeatherMap API)
    * **Top Global News Headlines** (NewsAPI)
    * **General Knowledge Queries** (Wikipedia API)
    * **System Time/Date Queries**
* **Robust Error Handling:** Includes modular functions and custom error messages for API failures and recognition issues.

## ⚙️ Project Setup and Dependencies

This project requires the following Python libraries:

1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/taniiishaa/Python-Multi-Domain-Assistant/
    cd Multimodal-Voice-Assistant-Project
    ```

2.  **Create and Activate a Virtual Environment (Best Practice):**
    ```bash
    python -m venv venv
    .\venv\Scripts\activate  # On Windows
    # source venv/bin/activate # On Linux/Mac
    ```

3.  **Install Required Packages:**
    ```bash
    pip install -r requirements.txt
    ```

## 🔑 Configuration (Secure API Keys)

For security, all API keys must be stored in a local **`.env`** file.

1.  Sign up for API keys from [OpenWeatherMap](https://openweathermap.org/api) and [NewsAPI](https://newsapi.org/).
2.  Create a file named **`.env`** in the project root and populate it:
    ```
    OPENWEATHERMAP_API_KEY="YOUR_API_KEY"
    NEWS_API_KEY="YOUR_API_KEY"
    WEATHER_CITY="Your City Name"
    NEWS_COUNTRY_CODE="in"
    ```

## ▶️ Running the Assistant

Execute the main script:
```bash
python assistant.py
