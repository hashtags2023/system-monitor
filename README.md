# system-monitor

# 🤖 AI System Monitor Bot

An interactive command-line chatbot that combines **system monitoring** with an **AI assistant**.  
The bot can answer general questions using OpenAI, fetch weather data, and monitor your system’s CPU, memory, and disk usage.

## 🚀 Features

- 💬 Chat with an AI assistant (OpenAI-powered)
- 🌦️ Fetch real-time weather data (OpenWeather API)
- 🖥️ Monitor system resources:
  - CPU usage
  - Memory usage
  - Disk space
- ⚡ Fallback to local responses if API calls fail
- 🔑 Secure API key handling with `.env`

---

## 📂 Project Structure

system-monitor/
│
├── ai_system_bot.py # Main chatbot with OpenAI & weather integration
├── ai_system_bot_v2.py # Improved version with enhanced response handling
├── monitor.py # System resource monitoring (CPU, memory, disk)
├── plot_logs.py # Visualizes system log data as charts
├── requirements.txt # Project dependencies
├── .gitignore # Excluded files (venv, .env, logs, large files)
└── README.md # Project documentation

---

## 🛠️ Setup & Installation

1. Clone the repository:

   ```bash
    git clone https://github.com/hashtags2023/system-monitor.git
    cd system-monitor
   ```

2. Create a virtual environment:

   ```bash
    python3 -m venv venv_ai
    source venv_ai/bin/activate
   ```

3. Install dependencies:

   ```bash
    pip install -r requirements.txt

   ```

4. Add your API keys to .env:

   ```ini
    OPENAI_API_KEY=your_openai_key_here
    WEATHER_API_KEY=your_openweather_key_here
   ```

5. Run the bot:

```bash
    python ai_system_bot.py
```

## Example Usage

```vbnet
🤖 AI System Bot v3: Type 'quit' to exit.
You: weather in Sacramento, CA
Bot: The current temperature in Sacramento is 85°F, with clear skies.
You: check system
Bot: CPU: 12% | Memory: 55% | Disk: 40%
You: tell me a joke
Bot: Why don’t programmers like nature? It has too many bugs.
```

## 🚀 Roadmap

- [x] Add system monitoring (CPU, memory, disk)
- [x] Integrate OpenAI API for chatbot responses
- [ ] Fix OpenWeather API key issue
- [ ] Add more monitoring features (network, processes)
- [ ] Build a web dashboard UI

## 🤝 Contributing

Pull requests are welcome! If you’d like to suggest improvements, feel free to open an issue.

## 📜 License

This project is licensed under the MIT License.

---

```yaml

```
