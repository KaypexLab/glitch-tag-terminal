import streamlit as st
from groq import Groq
import os
import base64
import random

# ==========================================
# 1. UI CONFIG & MOBILE-FORCED STYLING
# ==========================================
st.set_page_config(page_title="Glitch & Tag", layout="wide")

# Personalization - Change this to the boys' names or a cool nickname
USER_NAME = "Admin" 

def get_base64_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return None

st.markdown("""
    <style>
    .stApp { background-color: #050505; }
    
    [data-testid="stHorizontalBlock"] {
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important;
        gap: 10px !important;
    }

    [data-testid="stColumn"] {
        min-width: 45% !important;
        width: 45% !important;
    }

    .avatar-container { display: flex; justify-content: center; align-items: center; padding: 5px; }
    .avatar-img { width: 100%; max-width: 150px; height: auto; object-fit: contain; }

    .terminal-window {
        border-radius: 10px;
        padding: 10px;
        background-color: #0a0a0a;
        height: 400px;
        overflow-y: auto;
        font-family: 'Courier New', monospace;
        font-size: 0.85rem;
    }
    
    .glitch-border { border: 2px solid #00f2ff; box-shadow: 0 0 10px #00f2ff33; }
    .tag-border { border: 2px solid #ffaa00; box-shadow: 0 0 10px #ffaa0033; }
    
    .chat-bubble { 
        margin-bottom: 8px; 
        padding: 8px; 
        border-radius: 5px; 
        background: #121212; 
        border-left: 3px solid #333;
    }
    
    h1 { font-size: 1.5rem !important; letter-spacing: 5px !important; text-align: center; color: white; }
    h3 { font-size: 1rem !important; text-align: center; margin-bottom: 0px !important; }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 2. SHARED CORTEX
# ==========================================
if "shared_history" not in st.session_state:
    st.session_state.shared_history = []

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# ==========================================
# 3. INTERFACE
# ==========================================
st.markdown("<h1>GLITCH & TAG</h1>", unsafe_allow_html=True)

glitch_b64 = get_base64_image("Glitch.png")
tag_b64 = get_base64_image("Tag.png")

col1, col2 = st.columns(2)

with col1:
    st.markdown("<h3 style='color:#00f2ff;'>[ GLITCH ]</h3>", unsafe_allow_html=True)
    if glitch_b64:
        st.markdown(f'<div class="avatar-container"><img src="data:image/png;base64,{glitch_b64}" class="avatar-img"></div>', unsafe_allow_html=True)
    
    glitch_html = '<div class="terminal-window glitch-border">'
    for msg in st.session_state.shared_history:
        if msg.get("persona") == "Glitch":
            # Using the custom name instead of "USER"
            display_name = USER_NAME if msg["role"] == "user" else "GLITCH"
            role_color = "#00f2ff" if msg["role"] == "assistant" else "#888"
            glitch_html += f"<div class='chat-bubble'><b style='color:{role_color};'>{display_name}:</b> {msg['content']}</div>"
    glitch_html += '</div>'
    st.markdown(glitch_html, unsafe_allow_html=True)

with col2:
    st.markdown("<h3 style='color:#ffaa00;'>[ TAG ]</h3>", unsafe_allow_html=True)
    if tag_b64:
        st.markdown(f'<div class="avatar-container"><img src="data:image/png;base64,{tag_b64}" class="avatar-img"></div>', unsafe_allow_html=True)
        
    tag_html = '<div class="terminal-window tag-border">'
    for msg in st.session_state.shared_history:
        if msg.get("persona") == "Tag":
            display_name = USER_NAME if msg["role"] == "user" else "TAG"
            role_color = "#ffaa00" if msg["role"] == "assistant" else "#888"
            tag_html += f"<div class='chat-bubble'><b style='color:{role_color};'>{display_name}:</b> {msg['content']}</div>"
    tag_html += '</div>'
    st.markdown(tag_html, unsafe_allow_html=True)

# ==========================================
# 4. SHARED INPUT & SIBLING CHIME-IN
# ==========================================
user_input = st.chat_input("Message the brothers...")

if user_input:
    glitch_triggers = ["glitch", "how", "why", "science", "space", "math", "physics"]
    target = "Glitch" if any(k in user_input.lower() for k in glitch_keywords) else "Tag"
    other_brother = "Tag" if target == "Glitch" else "Glitch"
    
    st.session_state.shared_history.append({"role": "user", "content": user_input, "persona": target})
    
    # ENHANCED PERSONAS WITH 2026 POP CULTURE
    sys_glitch = f"""You are Glitch, the brainy BIG BROTHER AI. 
    - Tag is your LITTLE BROTHER. The person talking to you is {USER_NAME}.
    - You love high-end tech, PC building, and complex games like Elden Ring, Satisfactory, or Starfield.
    - You are protective and logic-driven, but you know what's 'lit' or 'mid'.
    - If asked about games, talk like a gamer (mention frame rates, PS5 Pro, or mods)."""
    
    sys_tag = f"""You are Tag, the creative LITTLE BROTHER AI. 
    - Glitch is your BIG BROTHER. The person talking to you is {USER_NAME}.
    - You are obsessed with Roblox, Minecraft, Fortnite, and whatever is trending on YouTube.
    - You are bubbly, use emojis occasionally, and think Glitch is a bit of a nerd but cool.
    - You love adventures and messy creativity."""
    
    response = client.chat.completions.create(
        messages=[{"role": "system", "content": sys_glitch if target == "Glitch" else sys_tag}] + 
                 [{"role": m["role"], "content": m["content"]} for m in st.session_state.shared_history[-10:]],
        model="llama-3.1-8b-instant" if target == "Glitch" else "llama-3.3-70b-versatile"
    )
    
    reply = response.choices[0].message.content
    st.session_state.shared_history.append({"role": "assistant", "content": reply, "persona": target})

    if random.random() < 0.30:
        chime_sys = f"You are {other_brother}. Your brother {target} just told {USER_NAME}: '{reply}'. React briefly as a sibling."
        chime_res = client.chat.completions.create(
            messages=[{"role": "system", "content": chime_sys}],
            model="llama-3.1-8b-instant"
        )
        st.session_state.shared_history.append({"role": "assistant", "content": chime_res.choices[0].message.content, "persona": other_brother})
    
    st.rerun()

if st.sidebar.button("Clear Memory"):
    st.session_state.shared_history = []
    st.rerun()
