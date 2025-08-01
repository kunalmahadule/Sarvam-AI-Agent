import os
import requests
import json
from src.tool_call_handler import find_restaurants, make_reservation, cancel_reservation
from dotenv import load_dotenv

load_dotenv()
# Set your OpenRouter API key here (you can also load from .env securely)
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")


# Tool schema definitions for LLM
tools = [
    {
        "type": "function",
        "function": {
            "name": "find_restaurants",
            "description": "Find restaurants in a given city based on cuisine and number of people",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {"type": "string"},
                    "cuisine": {"type": "string"},
                    "seats_required": {"type": "integer"}
                },
                "required": ["city"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "make_reservation",
            "description": "Reserve a table at a restaurant",
            "parameters": {
                "type": "object",
                "properties": {
                    "restaurant_name": {"type": "string"},
                    "user_name": {"type": "string"},
                    "time": {"type": "string"}
                },
                "required": ["restaurant_name", "user_name", "time"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "cancel_reservation",
            "description": "Cancel an existing reservation using reservation ID",
            "parameters": {
                "type": "object",
                "properties": {
                    "reservation_id": {"type": "string"}
                },
                "required": ["reservation_id"]
            }
        }
    }
]

# Model config (adjust as needed)
MODEL_NAME = "openrouter/meta-llama/llama-3-70b-instruct"



def call_openrouter(messages, tools=None, tool_choice="auto"):
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        raise ValueError("❌ OPENROUTER_API_KEY not found in .env")

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost:8501",  # Required by OpenRouter
        "X-Title": "Restaurant Reservation Agent",
    }

    body = {
        "model": "meta-llama/llama-3-70b-instruct",  # ✅ RIGHT
        "messages": messages,
    }

    if tools:
        body["tools"] = tools
        body["tool_choice"] = tool_choice  # "auto" or specific tool name

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers=headers,
        json=body
    )

    response.raise_for_status()  # Raise error for non-2xx codes
    return response.json()



def run_agent(user_input, history):
    # Step 1: Add user input
    messages = history + [{"role": "user", "content": user_input}]

    # Step 2: Initial call to LLM with tools
    response = call_openrouter(messages, tools)

    choice = response["choices"][0]

    if "tool_calls" in choice["message"]:
        tool_call = choice["message"]["tool_calls"][0]
        tool_name = tool_call["function"]["name"]
        tool_args = json.loads(tool_call["function"]["arguments"])

        # Step 3: Execute tool in Python
        if tool_name == "find_restaurants":
            result = find_restaurants(**tool_args)
        elif tool_name == "make_reservation":
            result = make_reservation(**tool_args)
        elif tool_name == "cancel_reservation":
            result = cancel_reservation(**tool_args)
        else:
            result = {"error": "Unknown tool called"}

        # Step 4: Send tool response back to LLM for final answer
        messages.append(choice["message"])  # tool call message
        messages.append({
            "role": "tool",
            "tool_call_id": tool_call["id"],
            "content": json.dumps(result)
        })

        # Step 5: Final LLM call with tool result
        final_response = call_openrouter(messages)
        final_message = final_response["choices"][0]["message"]["content"]
        return result, final_message

    else:
        # No tool used; direct response
        return None, choice["message"]["content"]
