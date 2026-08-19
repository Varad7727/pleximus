import os
import streamlit as st
from dotenv import load_dotenv
from google import genai
from tools import (
    calculator,
    weather,
    text_utility,
    wikipedia_summary,
    currency_converter,
)

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Nexus AI | Tool Calling Agent",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom UI styling
st.markdown(
    """
    <style>
        .main-title {
            font-size: 2.2rem;
            font-weight: 700;
            background: linear-gradient(90deg, #4F46E5, #06B6D4);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 0.2rem;
        }
        .subtitle {
            font-size: 1rem;
            color: #6B7280;
            margin-bottom: 1.5rem;
        }
        .tool-badge {
            display: inline-block;
            padding: 4px 10px;
            margin: 3px;
            border-radius: 12px;
            font-size: 0.8rem;
            background-color: #F3F4F6;
            color: #1F2937;
            border: 1px solid #E5E7EB;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# Validate API Key
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    st.error("⚠️ API Key not found! Please add `GEMINI_API_KEY` to your `.env` file.")
    st.stop()

# Initialize tools list
tools_list = [
    calculator,
    weather,
    text_utility,
    wikipedia_summary,
    currency_converter,
]

# Initialize Client and Chat Session
if "client" not in st.session_state:
    st.session_state.client = genai.Client(api_key=api_key)

if "chat" not in st.session_state:
    st.session_state.chat = st.session_state.client.chats.create(
        model="gemini-3.6-flash",
        config={
            "tools": tools_list,
            "system_instruction": (
                "You are an AI assistant equipped with specialized tools. When a user asks about weather, "
                "math, text formatting, Wikipedia topics, or currency conversion, invoke the relevant tool. "
                "For weather queries, infer the coordinates (e.g., Ratnagiri: lat 16.9902, lon 73.3120) and run the tool."
            ),
        },
    )

if "messages" not in st.session_state:
    st.session_state.messages = []

# Sidebar configuration
with st.sidebar:
    st.markdown("### 🛠️ Active Tools")
    st.markdown(
        """
        <span class="tool-badge">🔢 Calculator</span>
        <span class="tool-badge">🌦️ Weather (Open-Meteo)</span>
        <span class="tool-badge">🔤 Text Utility</span>
        <span class="tool-badge">📖 Wikipedia Summary</span>
        <span class="tool-badge">💱 Currency Converter</span>
        """,
        unsafe_allow_html=True,
    )
    
    st.markdown("---")
    st.markdown("### 💡 Quick Prompts")
    quick_prompts = [
        "What is 25 multiplied by 18?",
        "What is the weather in Ratnagiri right now?",
        "Convert 100 USD to INR",
        "Give me a summary of Python (programming language)",
        "Reverse the text 'Autonomous Agent'",
    ]
    for qp in quick_prompts:
        if st.button(qp, use_container_width=True):
            st.session_state.pending_prompt = qp

    st.markdown("---")
    if st.button("🗑️ Clear Conversation", use_container_width=True):
        st.session_state.messages = []
        st.session_state.chat = st.session_state.client.chats.create(
            model="gemini-3.6-flash",
            config={"tools": tools_list},
        )
        st.rerun()

# Main header
st.markdown('<div class="main-title">⚡ Nexus AI Tool Agent</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Autonomous reasoning and real-time tool execution powered by Gemini 3.6 Flash</div>', unsafe_allow_html=True)

# Render chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"], avatar="🧑‍💻" if msg["role"] == "user" else "🤖"):
        st.markdown(msg["content"])

# Prompt handler
prompt = st.chat_input("Ask a question, request math, weather, or wiki lookup...")
if "pending_prompt" in st.session_state and st.session_state.pending_prompt:
    prompt = st.session_state.pop("pending_prompt")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="🧑‍💻"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar="🤖"):
        with st.spinner("Invoking tools & generating response..."):
            try:
                response = st.session_state.chat.send_message(prompt)
                reply = response.text
                st.markdown(reply)
                st.session_state.messages.append({"role": "assistant", "content": reply})
            except Exception as e:
                error_msg = f"⚠️ **Execution Error:** {e}"
                st.error(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})