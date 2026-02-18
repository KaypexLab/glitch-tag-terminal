import streamlit as st
from groq import Groq
import os
import base64
import random

# ==========================================
# 1. UI CONFIG & ADVANCED SIBLING STYLE
# ==========================================
st.set_page_config(page_title="Glitch & Tag", layout="wide")

# Function to convert local image to Base64 (Kills the white box/path error)
def get_base64_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return None

# Injecting the Terminal Theme
st.markdown("""
    <style>
    .stApp { background-color: #050505; }
    
    .avatar-container {
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 10px;
    }

    .avatar-img {
        width: 300px; /* Big avatars for the boys */
        height: auto;
        object-fit: contain;
        filter: drop-shadow(0 0 15px rgba(255,255,255,0.1));
    }

    .terminal-window {
        border-radius: 10px;
        padding: 20px;
        background-color: #0a0a0a;
        height: 480px;
        overflow-y: auto;
        margin-top: 5px;
        font-family: 'Courier New', monospace;
    }
    
    .glitch-border { border: 2px solid #00f2ff; box-shadow: 0 0 15px #00f2ff33; }
    .tag-border { border: 2px solid #ffaa00; box-shadow: 0 0 15px #ffaa0033; }
    
    .chat-bubble { 
        margin-bottom: 12px; 
        padding: 12px; 
        border-radius: 8px; 
        background: #121212; 
        border-left: 4px solid #333;
        color: #e0e0e0;
    }
    
    h1, h3 { text-align: center; font-family: 'Courier New', monospace; color: white; }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 2. SHARED CORTEX
# ==========================================
if "shared_history" not in st.session_state:
    st.session_state.shared_history = []

try:
    # Safe key retrieval from Streamlit Secrets
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except:
    st.error("Missing GROQ_API_KEY in Streamlit Secrets!")
    st.stop()

# ==========================================
# 3. GLITCH & TAG INTERFACE
# ==========================================
st.markdown("<h1 style='letter-spacing: 10px; margin-bottom: 0px;'>GLITCH & TAG</h1>", unsafe_allow_html=True)

col1, col2 = st.columns(2)

# Prepare Base64 Images
glitch_b64 = get_base64_image("Glitch.png")
tag_b64 = get_base64_image("Tag.png")

# GLITCH (Big Brother)
with col1:
    st.markdown("<h3 style='color:#00f2ff; margin-bottom: 5px;'>[ GLITCH ]</h3>", unsafe_allow_html=True)
    if glitch_b64:
        st.markdown(f'<div class="avatar-container"><img src="data:image/png;base64,{glitch_b64}" class="avatar-img"></div>', unsafe_allow_html=True)
    else:
        st.warning("Glitch.png not found")
    
    glitch_html = '<div class="terminal-window glitch-border">'
    for msg in st.session_state.shared_history:
        if msg.get("persona") == "Glitch":
            role_color = "#00f2ff" if msg["role"] == "assistant" else "#888"
            glitch_html += f"<div class='chat-bubble'><b style='color:{role_color};'>{msg['role'].upper()}:</b> {msg['content']}</div>"
    glitch_html += '</div>'
    st.markdown(glitch_html, unsafe_allow_html=True)

# TAG (Little Brother)
with col2:
    st.markdown("<h3 style='color:#ffaa00; margin-bottom: 5px;'>[ TAG ]</h3>", unsafe_allow_html=True)
    if tag_b64:
        st.markdown(f'<div class="avatar-container"><img src="data:image/png;base64,{tag_b64}" class="avatar-img"></div>', unsafe_allow_html=True)
    else:
        st.warning("Tag.png not found")
        
    tag_html = '<div class="terminal-window tag-border">'
    for msg in st.session_state.shared_history:
        if msg.get("persona") == "Tag":
            role_color = "#ffaa00" if msg["role"] == "assistant" else "#888"
            tag_html += f"<div class='chat-bubble'><b style='color:{role_color};'>{msg['role'].upper()}:</b> {msg['content']}</div>"
    tag_html += '</div>'
    st.markdown(tag_html, unsafe_allow_html=True)

# ==========================================
# 4. SHARED INPUT & SIBLING CHIME-IN
# ==========================================
user_input = st.chat_input("Message the brothers...")

if user_input:
    # Routing Logic
    glitch_keywords = ["glitch", "how", "why", "science", "space", "math", "physics", "code"]
    target = "Glitch" if any(k in user_input.lower() for k in glitch_keywords) else "Tag"
    other_brother = "Tag" if target == "Glitch" else "Glitch"
    
    st.session_state.shared_history.append({"role": "user", "content": user_input, "persona": target})
    
    # System Instructions
    sys_glitch = "You are Glitch, the brainy BIG BROTHER. Tag is your LITTLE BROTHER. Be protective, logical, and smart."
    sys_tag = "You are Tag, the creative LITTLE BROTHER. Glitch is your BIG BROTHER. Be fun, adventurous, and bubbly."
    
    # Get Primary Response
    response = client.chat.completions.create(
        messages=[{"role": "system", "content": sys_glitch if target == "Glitch" else sys_tag}] + 
                 [{"role": m["role"], "content": m["content"]} for m in st.session_state.shared_history[-10:]],
        model="llama-3.1-8b-instant" if target == "Glitch" else "llama-3.3-70b-versatile"
    )
    
    reply = response.choices[0].message.content
    st.session_state.shared_history.append({"role": "assistant", "content": reply, "persona": target})

    # 30% Chance for Sibling Commentary
    if random.random() < 0.30:
        chime_sys = f"You are {other_brother}. Your brother {target} just said: '{reply}'. Give a 1-sentence reaction as his brother."
        chime_res = client.chat.completions.create(
            messages=[{"role": "system", "content": chime_sys}],
            model="llama-3.1-8b-instant"
        )
        st.session_state.shared_history.append({"role": "assistant", "content": chime_res.choices[0].message.content, "persona": other_brother})
    
    st.rerun()

# Sidebar Reset
st.sidebar.markdown("### Admin Controls")
if st.sidebar.button("Clear Memory"):
    st.session_state.shared_history = []
    st.rerun()
