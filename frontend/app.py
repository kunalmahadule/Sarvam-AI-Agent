import streamlit as st

import sys
import os

# Add the root project directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.agent import run_agent



st.set_page_config(page_title="GoodFoods AI Agent", page_icon="🍽️", layout="centered")

st.title("🍽️ GoodFoods Restaurant Reservation Agent")
st.markdown("Welcome! I can help you find restaurants, make reservations, or cancel them. Just type below 👇")

# Session state to store chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input box
user_input = st.chat_input("Ask me something like: 'Book a table for 2 in Mumbai for Chinese'")

if user_input:
    # Store user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Call LLM agent logic
    tool_result, assistant_reply = run_agent(user_input, st.session_state.messages)

    # Store assistant message
    st.session_state.messages.append({"role": "assistant", "content": assistant_reply})
    with st.chat_message("assistant"):
        st.markdown(assistant_reply)
