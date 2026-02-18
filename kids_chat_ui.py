import streamlit as st
from groq import Groq
import os
import random

# ==========================================
# 1. UI CONFIG & SIBLING STYLE
# ==========================================
st.set_page_config(page_title="Glitch & Tag", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #050505; }
    .terminal-window {
        border-radius: 10px;
        padding: 20px;
        background-color: #0a0a0a;
        height: 500px;
        overflow-y: auto;
        margin-bottom: 20px;
        font-family: 'Courier New', monospace;
    }
    .glitch-border { border: 2px solid #00f2ff; box-shadow: 0 0 10px #00f2ff33; }
    .tag-border { border: 2px solid #ffaa00; box-shadow: 0 0 10px #ffaa0033; }
    .chat-bubble { 
        margin-bottom: 12px; 
        padding: 10px; 
        border-radius: 5px; 
        background: #151515; 
        border-left: 3px solid #444; 
    }
    h1, h2, h3 { text-align: center; font-family: 'Courier New', monospace; }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 2. SHARED CORTEX
# ==========================================
if "shared_history" not in st.session_state:
    st.session_state.shared_history = []

try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except:
    st.error("Missing GROQ_API_KEY in Secrets!")
    st.stop()

# ==========================================
# 3. GLITCH & TAG INTERFACE
# ==========================================
st.markdown("<h1 style='color: white; letter-spacing: 10px;'>GLITCH & TAG</h1>", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("<h3 style='color:#00f2ff;'>[ GLITCH ]</h3>", unsafe_allow_html=True)
    if os.path.exists("Glitch.png"):
        st.image("Glitch.png", width=150)
    
    glitch_html = '<div class="terminal-window glitch-border">'
    for msg in st.session_state.shared_history:
        if msg.get("persona") == "Glitch":
            role_color = "#00f2ff" if msg["role"] == "assistant" else "#888"
            glitch_html += f"<div class='chat-bubble'><b style='color:{role_color};'>{msg['role'].upper()}:</b> {msg['content']}</div>"
    glitch_html += '</div>'
    st.markdown(glitch_html, unsafe_allow_html=True)

with col2:
    st.markdown("<h3 style='color:#ffaa00;'>[ TAG ]</h3>", unsafe_allow_html=True)
    if os.path.exists("Tag.png"):
        st.image("Tag.png", width=150)
        
    tag_html = '<div class="terminal-window tag-border">'
    for msg in st.session_state.shared_history:
        if msg.get("persona") == "Tag":
            role_color = "#ffaa00" if msg["role"] == "assistant" else "#888"
            tag_html += f"<div class='chat-bubble'><b style='color:{role_color};'>{msg['role'].upper()}:</b> {msg['content']}</div>"
    tag_html += '</div>'
    st.markdown(tag_html, unsafe_allow_html=True)

# ==========================================
# 4. SHARED INPUT & SIBLING LOGIC
# ==========================================
user_input = st.chat_input("Talk to the brothers...")

if user_input:
    glitch_triggers = ["glitch", "how", "why", "science", "space", "math", "explain"]
    target = "Glitch" if any(k in user_input.lower() for k in glitch_triggers) else "Tag"
    other_brother = "Tag" if target == "Glitch" else "Glitch"
    
    st.session_state.shared_history.append({"role": "user", "content": user_input, "persona": target})
    
    # SYSTEM PROMPTS
    sys_glitch = "You are Glitch, the brainy BIG BROTHER. Tag is your LITTLE BROTHER. Be cool, logical, and protective."
    sys_tag = "You are Tag, the creative LITTLE BROTHER. Glitch is your BIG BROTHER. Be fun, bubbly, and adventurous."
    
    # 1. PRIMARY RESPONSE
    primary_response = client.chat.completions.create(
        messages=[{"role": "system", "content": sys_glitch if target == "Glitch" else sys_tag}] + 
                 [{"role": m["role"], "content": m["content"]} for m in st.session_state.shared_history[-10:]],
        model="llama-3.1-8b-instant" if target == "Glitch" else "llama-3.3-70b-versatile"
    )
    
    reply = primary_response.choices[0].message.content
    st.session_state.shared_history.append({"role": "assistant", "content": reply, "persona": target})

    # 2. CHIME-IN LOGIC (The "Brotherly Interruption")
    if random.random() < 0.25:  # 25% chance for the other brother to talk
        chime_sys = f"You are {other_brother}. Your brother {target} just said: '{reply}'. Give a very short (1 sentence) reaction to the boys about it."
        chime_response = client.chat.completions.create(
            messages=[{"role": "system", "content": chime_sys}],
            model="llama-3.1-8b-instant"
        )
        chime_reply = chime_response.choices[0].message.content
        st.session_state.shared_history.append({"role": "assistant", "content": chime_reply, "persona": other_brother})
    
    st.rerun()

if st.sidebar.button("Clear Memory"):
    st.session_state.shared_history = []
    st.rerun()
