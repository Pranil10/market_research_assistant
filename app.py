import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
api_key=os.getenv("GITHUB_MODEL_API_KEY") or st.secrets.get("GITHUB_MODEL_API_KEY")

# GitHub model API 
client = OpenAI(
    api_key=api_key,  
    base_url="https://models.github.ai/inference" 
)

# Streamlit setup
st.set_page_config(page_title="Researcer", page_icon="📊")
st.title("Reasearcher")
st.caption("Ask for a company profile --")

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display message history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input
userinput = st.chat_input("Enter a company name (e.g., HDFC, Mahindra)... ")

if userinput:
    # Save user message
    st.session_state.messages.append({"role": "user", "content": userinput})
    with st.chat_message("user"):
        st.markdown(userinput)

    # Messages to send to model
    messages = [
        {
            "role": "system",
            "content": (
                "You are a Market Research Associate who creates detailed company profiles "
                "based only on the company's official website."
            ),
        },
        {
            "role": "user",
            "content": (
                f"Create a Company Profile that includes: \n"
                f"- Company Overview\n"
                f"- Growth Rate (if available)\n"
                f"- Market Share per segment (if listed)\n"
                f"Use only the official website of {userinput} as your source."
            ),
        },
    ]

    # Call the model
    with st.chat_message("assistant"):
        with st.spinner("🧠 Thinking like a research pro..."):
            try:
                response = client.chat.completions.create(
                    model="openai/gpt-4.1",  # put correct model ID if needed
                    messages=messages,
                    temperature=0.3,
                    top_p=1.0
                )
            except Exception as e:
                st.error(f'Response - {e}')
            try:
                reply = response.choices[0].message.content
            except Exception as e:
                st.error(f'Reply - {e}')    
            try:    
                st.markdown(reply)
                st.session_state.messages.append({"role": "assistant", "content": reply})
            except Exception as e:
                st.error(f"❌ Error: {e}")
