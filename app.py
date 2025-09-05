import streamlit as st
from openai import OpenAI
import traceback

st.set_page_config(page_title="OpenAI Chatbot", page_icon="🤖")
st.title("🤖 My Chatbot (with pasted API key)")

# Step 1: Enter API key directly in the app
api_key = st.text_input("Enter your OpenAI API key:", type="password")

if not api_key:
    st.warning("Please paste your API key above to continue.")
    st.stop()

client = OpenAI(api_key=api_key)

# Step 2: Store chat history
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": "You are a helpful assistant."}]

# Step 3: Show chat history
for msg in st.session_state.messages:
    if msg["role"] != "system":
        st.chat_message(msg["role"]).write(msg["content"])

# Step 4: Handle new user input
if user_input := st.chat_input("Type your message..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.chat_message("user").write(user_input)

    try:
        resp = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=st.session_state.messages
        )
        reply = resp.choices[0].message.content
    except Exception as e:
        reply = f"⚠️ Error: {repr(e)}"
        st.error("API call failed.")
        st.text(traceback.format_exc())

    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.chat_message("assistant").write(reply)
