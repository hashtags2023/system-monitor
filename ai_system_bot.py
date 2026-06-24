import os
import random
from dotenv import load_dotenv
import pandas as pd
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
import openai
import requests

# --------------------------
# Load environment variables
# --------------------------
load_dotenv()

# --------------------------
# System prompt
# --------------------------
SYSTEM_PROMPT = "You are a helpful and friendly assistant. Only answer naturally and politely."

# --------------------------
# OpenAI API key setup
# --------------------------
api_keys = [
    os.getenv("OPENAI_KEY_1"),
    os.getenv("OPENAI_KEY_2"),
    os.getenv("OPENAI_KEY_3"),
]
api_keys = [key for key in api_keys if key]
use_openai = bool(api_keys)
api_index = 0

def rotate_key():
    global api_index
    api_index = (api_index + 1) % len(api_keys)
    openai.api_key = api_keys[api_index]

if use_openai:
    openai.api_key = api_keys[api_index]

# --------------------------
# Load DialoGPT model
# --------------------------
model_name = "microsoft/DialoGPT-small"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

# --------------------------
# Log file and conversation history
# --------------------------
LOG_FILE = "system_logs.csv"
conversation_history = []

# --------------------------
# Get latest system stats
# --------------------------
def get_latest_stats():
    try:
        df = pd.read_csv(LOG_FILE)
        return df.iloc[-1]
    except FileNotFoundError:
        return None

# --------------------------
# Local DialoGPT AI response
# --------------------------
def ai_response_local(user_input):
    conversation_history.append(f"User: {user_input}")
    prompt = SYSTEM_PROMPT + "\n" + "\n".join(conversation_history) + "\nBot:"
    
    inputs = tokenizer(prompt, return_tensors="pt")
    outputs = model.generate(
        input_ids=inputs["input_ids"],
        attention_mask=inputs["attention_mask"],
        max_new_tokens=60,
        do_sample=True,
        top_p=0.95,
        pad_token_id=tokenizer.eos_token_id
    )
    
    text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    bot_text = text.split("Bot:")[-1].strip()
    conversation_history.append(f"Bot: {bot_text}")
    
    if len(conversation_history) > 6:
        conversation_history.pop(0)
    
    return bot_text

# --------------------------
# OpenAI GPT response with key rotation
# --------------------------
def ai_response_openai(user_input, retries=3):
    if not api_keys:
        return ai_response_local(user_input)

    attempt = 0
    while attempt < retries:
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_input}
                ],
                max_tokens=150
            )
            return response.choices[0].message["content"].strip()
        except openai.error.RateLimitError:
            print(f"[Quota hit with key {api_index + 1}, rotating key...]")
            rotate_key()
            attempt += 1
        except openai.error.OpenAIError as e:
            print(f"[OpenAI API failed, using local fallback]: {e}")
            return ai_response_local(user_input)
    return "[All OpenAI keys exhausted, using local AI fallback.]"

# --------------------------
# Command fuzzy matching
# --------------------------
def closest_command(user_input):
    commands = ["cpu", "memory", "disk", "network", "joke", "hello", "hi", "how are you", "weather"]
    match = difflib.get_close_matches(user_input.lower(), commands, n=1, cutoff=0.6)
    return match[0] if match else None

# --------------------------
# Weather API setup
# --------------------------
OPENWEATHER_KEY = os.getenv("OPENWEATHER_KEY")
WEATHER_API_URL = "https://api.openweathermap.org/data/2.5/weather"

from difflib import get_close_matches

# --------------------------
# Fuzzy city/state mapping
# --------------------------
CITY_MAP = {
    "sacramento": "Sacramento,US",
    "los angeles": "Los Angeles,US",
    "san francisco": "San Francisco,US",
    "new york": "New York,US",
    "chicago": "Chicago,US",
    "ca": "California,US",
    "ny": "New York,US",
    "tx": "Texas,US",
    "fl": "Florida,US",
}

def get_city_fuzzy(user_input):
    """Fuzzy match city/state from user input."""
    user_input = user_input.lower().strip()
    matches = get_close_matches(user_input, CITY_MAP.keys(), n=1, cutoff=0.6)
    if matches:
        return CITY_MAP[matches[0]]
    return "New York,US"  # fallback default

# --------------------------
# Updated weather fetch
# --------------------------
def get_weather(user_input="New York"):
    """Fetch weather for city/state using OpenWeatherMap."""
    if not OPENWEATHER_KEY:
        return "Weather API key not set."

    # Strip 'weather' from input, e.g. "Sacramento weather" -> "Sacramento"
    city_query = user_input.lower().replace("weather", "").strip()
    city = get_city_fuzzy(city_query)

    try:
        params = {"q": city, "appid": OPENWEATHER_KEY, "units": "metric"}
        response = requests.get(WEATHER_API_URL, params=params)
        data = response.json()
        if response.status_code != 200:
            return f"Could not fetch weather: {data.get('message', 'Unknown error')}"
        temp = data["main"]["temp"]
        description = data["weather"][0]["description"]
        return f"The weather in {city} is {description} with a temperature of {temp}°C."
    except Exception as e:
        return f"Error fetching weather: {e}"



# --------------------------
# Multiple jokes
# --------------------------
jokes = [
    "Why did the computer go to the doctor? Because it caught a virus!",
    "Why do programmers prefer dark mode? Because light attracts bugs!",
    "Why was the cell phone wearing glasses? Because it lost its contacts!",
    "Why did the computer show up at work late? It had a hard drive!",
]

def get_joke():
    return random.choice(jokes)

# --------------------------
# Main bot response logic
# --------------------------
def bot_response(user_input):
    stats = get_latest_stats()
    cmd = closest_command(user_input)

    if stats is None and cmd in ["cpu", "memory", "disk", "network"]:
        return "No system data available yet."
    
    if cmd == "cpu":
        return f"CPU usage is {stats['cpu']}%, threshold is 80%."
    elif cmd == "memory":
        return f"Memory usage is {stats['memory']}%, threshold is 80%."
    elif cmd == "disk":
        return f"Disk usage is {stats['disk']}%, threshold is 90%."
    elif cmd == "network":
        total_mb = round(stats['network_bytes'] / (1024 * 1024), 2)
        sent_mb = stats.get('network_sent_mb', 'N/A')
        recv_mb = stats.get('network_recv_mb', 'N/A')
        return (f"🌐 Network Usage — Total: {total_mb} MB | "
                f"Sent: {sent_mb} MB | Received: {recv_mb} MB")
    elif cmd == "joke":
        return get_joke()
    elif cmd in ["hello", "hi"]:
        return "Hello! How can I help you today? 😄"
    elif cmd == "how are you":
        return "I'm a bot, but I'm running smoothly! How about you?"
    elif "weather" in user_input.lower():
        city = user_input.lower().replace("weather", "").strip() or "New York"
        return get_weather(city)
    elif use_openai:
        return ai_response_openai(user_input)
    else:
        return ai_response_local(user_input)

# --------------------------
# Chat loop
# --------------------------
def chat_bot():
    print("🤖 AI System Bot v3: Type 'quit' to exit.")
    while True:
        try:
            msg = input("You: ")
            if msg.lower() == "quit":
                break
            print("Bot:", bot_response(msg))
        except KeyboardInterrupt:
            print("\nExiting bot...")
            break

# --------------------------
# Main execution
# --------------------------
if __name__ == "__main__":
    chat_bot()
