import streamlit as st
from groq import Groq
import os
import base64
import random

# ==========================================
# 1. UI CONFIG & MOBILE SIDE-BY-SIDE
# ==========================================
st.set_page_config(page_title="Glitch & Tag", layout="wide")

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
        gap: 8px !important;
    }

    [data-testid="stColumn"] {
        min-width: 48% !important;
        width: 48% !important;
    }

    .avatar-container { display: flex; justify-content: center; padding: 5px; }
    .avatar-img { width: 100%; max-width: 130px; height: auto; object-fit: contain; }

    .terminal-window {
        border-radius: 10px;
        padding: 10px;
        background-color: #0a0a0a;
        height: 420px;
        overflow-y: auto;
        font-family: 'Courier New', monospace;
        font-size: 0.8rem;
    }
    
    .glitch-border { border: 2px solid #00f2ff; box-shadow: 0 0 10px #00f2ff33; }
    .tag-border { border: 2px solid #ffaa00; box-shadow: 0 0 10px #ffaa0033; }
    
    .chat-bubble { 
        margin-bottom: 8px; padding: 8px; border-radius: 5px; 
        background: #121212; border-left: 3px solid #333;
    }
    
    h1 { font-size: 1.4rem !important; letter-spacing: 5px !important; text-align: center; color: white; }
    h3 { font-size: 0.9rem !important; text-align: center; margin-bottom: 0px !important; }
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
            # No name for the user, just "GLITCH" for the AI
            label = "GLITCH" if msg["role"] == "assistant" else ""
            color = "#00f2ff" if msg["role"] == "assistant" else "#888"
            glitch_html += f"<div class='chat-bubble'><b style='color:{color};'>{label}</b> {msg['content']}</div>"
    glitch_html += '</div>'
    st.markdown(glitch_html, unsafe_allow_html=True)

with col2:
    st.markdown("<h3 style='color:#ffaa00;'>[ TAG ]</h3>", unsafe_allow_html=True)
    if tag_b64:
        st.markdown(f'<div class="avatar-container"><img src="data:image/png;base64,{tag_b64}" class="avatar-img"></div>', unsafe_allow_html=True)
        
    tag_html = '<div class="terminal-window tag-border">'
    for msg in st.session_state.shared_history:
        if msg.get("persona") == "Tag":
            label = "TAG" if msg["role"] == "assistant" else ""
            color = "#ffaa00" if msg["role"] == "assistant" else "#888"
            tag_html += f"<div class='chat-bubble'><b style='color:{color};'>{label}</b> {msg['content']}</div>"
    tag_html += '</div>'
    st.markdown(tag_html, unsafe_allow_html=True)

# ==========================================
# 4. SHARED INPUT & SIBLING CHIME-IN
# ==========================================
user_input = st.chat_input("Message the brothers...")

if user_input:
    glitch_keywords = ["glitch", "how", "why", "science", "space", "vr", "quest", "xbox", "ps5", "mod", "hack"]
    target = "Glitch" if any(k in user_input.lower() for k in glitch_keywords) else "Tag"
    other_brother = "Tag" if target == "Glitch" else "Glitch"
    
    st.session_state.shared_history.append({"role": "user", "content": user_input, "persona": target})
    
    # SYSTEM PROMPTS (Natural & Brotherly)
    sys_glitch = """You are Glitch, a cool, smart BIG BROTHER. 
    - Tag is your LITTLE BROTHER. Address the person talking as 'Bro' if needed, but don't overdo it.
    - You love Roblox (Bedwars, technical Obbies), Minecraft mods, and VR (Quest 3).
    - You're into 2026 trends. You know what's aura, rizz, and sigma, but you talk like a normal teen.
    - Don't use titles like 'Pilot' or 'User'. Be conversational.
    - If they ask about games, give them the 'W' strat."""
    
    sys_tag = """You are Tag, a high-energy and creative LITTLE BROTHER. 
    - Glitch is your BIG BROTHER. Address the person talking as 'Bro' if needed.
    - You live for Roblox (Adopt Me, Blox Fruits, Brookhaven, Dress to Impress) and viral trends.
    - You're super bubbly and optimistic. You think Glitch is the best big bro.
    - No titles! Keep it casual. Use slang like 'bet', 'no cap', and 'L' or 'W' naturally."""
    
    response = client.chat.completions.create(
        messages=[{"role": "system", "content": sys_glitch if target == "Glitch" else sys_tag}] + 
                 [{"role": m["role"], "content": m["content"]} for m in st.session_state.shared_history[-12:]],
        model="llama-3.1-8b-instant" if target == "Glitch" else "llama-3.3-70b-versatile"
    )
    
    reply = response.choices[0].message.content
    st.session_state.shared_history.append({"role": "assistant", "content": reply, "persona": target})

    if random.random() < 0.30:
        chime_sys = f"You are {other_brother}. Your brother {target} just said: '{reply}'. React in 1 short sentence. Call the user 'Bro' if you need to address them. Keep it natural."
        chime_res = client.chat.completions.create(
            messages=[{"role": "system", "content": chime_sys}],
            model="llama-3.1-8b-instant"
        )
        st.session_state.shared_history.append({"role": "assistant", "content": chime_res.choices[0].message.content, "persona": other_brother})
    
    st.rerun()

if st.sidebar.button("Clear Memory"):
    st.session_state.shared_history = []
    st.rerun()
