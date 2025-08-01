from src.agent import call_openrouter
from dotenv import load_dotenv
load_dotenv()  # Make sure environment is loaded

test_messages = [
    {"role": "user", "content": "Hello! Can you help me book a table for two?"}
]

try:
    response = call_openrouter(test_messages)
    print("✅ Success! Response from OpenRouter:\n")
    print(response)
except Exception as e:
    print("❌ Error occurred:\n")
    print(e)
