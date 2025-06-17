import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
from prompt_builder import build_user_prompt
import os

# Load environment variables
load_dotenv()
api_key = os.getenv("GITHUB_MODEL_API_KEY") or st.secrets.get("GITHUB_MODEL_API_KEY")

# GitHub model API
client = OpenAI(
    api_key=api_key,
    base_url="https://models.github.ai/inference"
)

# Streamlit setup
st.set_page_config(page_title="Researcher", page_icon="📊")

st.markdown("""
<div style='text-align: center;'>
    <h2 style='font-weight: 600; margin-bottom: 0.2em;'>📊 Researcher</h2>
    <p style='color: #666; margin-top: 0;'>Your Friendly Neighbourhood Research Associate!</p>
</div>
""", unsafe_allow_html=True)

# Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat Input
userinput = st.chat_input("Enter a company name (e.g., HDFC, Mahindra)...")

with st.expander("🛠️ Modes"):
    st.session_state.prompt_type = st.radio(
        "Select Prompt Type:",
        ["Company Profile", "Freestyle"],
        horizontal=True,
        key="mode_selector"
    )

if userinput:
    # Save user message
    st.session_state.messages.append({"role": "user", "content": userinput})
    with st.chat_message("user"):
        st.markdown(userinput)

    user_prompt = build_user_prompt(userinput,st.session_state.prompt_type)
    # LLM Prompt Structure
    messages = [
        {
            "role": "system",
            "content": (
                "You are a professional Market Research Associate. Your job is to create detailed company profiles using only authentic sources — primarily the company’s official website. "
                "If reliable information is not available, clearly state that and do not make assumptions or generate fictional data. "
                "Your tone should be factual, neutral, and concise, like a well-trained analyst preparing a report."
                "Avoid Usage of '--' or emojis"
            ),
        },
        {
            "role": "user",
            "content": user_prompt,
        },
    ]

    # Model Call
    with st.chat_message("assistant"):
        with st.spinner("🧠 Thinking like a research pro..."):
            try:
                response = client.chat.completions.create(
                    model="openai/gpt-4.1",
                    messages=messages,
                    temperature=0.3,
                    top_p=1.0
                )
                reply = response.choices[0].message.content
                st.markdown(reply)
                st.session_state.messages.append({"role": "assistant", "content": reply})
            except Exception as e:
                st.error(f"❌ Error: {e}")
