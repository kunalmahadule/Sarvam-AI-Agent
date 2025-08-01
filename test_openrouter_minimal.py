import os
import requests
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("OPENROUTER_API_KEY")
if not api_key:
    raise ValueError("❌ OPENROUTER_API_KEY not found in .env")

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json",
    "HTTP-Referer": "http://localhost:8501",  # required by OpenRouter
    "X-Title": "Minimal Test"                 # optional, helps organize usage
}

body = {
    "model": "meta-llama/llama-3-70b-instruct",   # ✅ Correct model ID
    "messages": [
        {
            "role": "user",
            "content": "Hello, how are you?"
        }
    ]
}

response = requests.post(
    "https://openrouter.ai/api/v1/chat/completions",
    headers=headers,
    json=body
)

print("✅ Status Code:", response.status_code)
print("✅ Response:\n", response.json())
