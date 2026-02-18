import streamlit as st
from groq import Groq
import os

# ==========================================
# 1. UI CONFIG & CYBER-SIBLING STYLING
# ==========================================
st.set_page_config(page_title="Moltbot OS", layout="wide")

# Injecting the Terminal Aesthetic
st.markdown("""
    <style>
    .stApp { background-color: #050505; }
    .glitch-container {
        border: 2px solid #00f2ff;
        padding: 20px;
        border-radius: 10px;
        background-color: #0a0a0a;
        height: 500px;
        overflow-y: auto;
        box-shadow: 0 0 10px #00f2ff33;
    }
    .tag-container {
        border: 2px solid #ffaa00;
        padding: 20px;
        border-radius: 10px;
        background-color: #0a0a0a;
        height: 500px;
        overflow-y: auto;
        box-shadow: 0 0 10px #ffaa0033;
    }
    .chat-bubble { margin-bottom: 12px; padding: 8px; border-radius: 4px; background: #151515; border-left: 3px solid #333; }
    .stChatInputContainer { padding-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 2. SHARED MEMORY CORTEX
# ==========================================
if "shared_history" not in st.session_state:
    st.session_state.shared_history = []

# Secure API Client
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except Exception:
    st.error("⚠️ SYSTEM HALT: GROQ_API_KEY not found in Secrets.")
    st.stop()

# ==========================================
# 3. THE SIBLING DASHBOARD
# ==========================================
st.markdown("<h2 style='text-align: center; color: white; letter-spacing: 5px;'>MOLTBOT SIBLING OS</h2>", unsafe_allow_html=True)

col1, col2 = st.columns(2)

# LEFT SIDE: GLITCH
with col1:
    st.markdown("<h3 style='color:#00f2ff; text-align:center;'>[ GLITCH ]</h3>", unsafe_allow_html=True)
    if os.path.exists("Glitch.png"):
        st.image("Glitch.png", use_container_width=True)
    
    glitch_placeholder = st.empty()
    with glitch_placeholder.container():
        st.markdown('<div class="glitch-container">', unsafe_allow_html=True)
        for msg in st.session_state.shared_history:
            if msg.get("persona") == "Glitch":
                color = "#00f2ff" if msg["role"] == "assistant" else "#888"
                st.markdown(f"<div class='chat-bubble'><b style='color:{color};'>{msg['role'].upper()}:</b> {msg['content']}</div>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# RIGHT SIDE: TAG
with col2:
    st.markdown("<h3 style='color:#ffaa00; text-align:center;'>[ TAG ]</h3>", unsafe_allow_html=True)
    if os.path.exists("Tag.png"):
        st.image("Tag.png", use_container_width=True)
        
    tag_placeholder = st.empty()
    with tag_placeholder.container():
        st.markdown('<div class="tag-container">', unsafe_allow_html=True)
        for msg in st.session_state.shared_history:
            if msg.get("persona") == "Tag":
                color = "#ffaa00" if msg["role"] == "assistant" else "#888"
                st.markdown(f"<div class='chat-bubble'><b style='color:{color};'>{msg['role'].upper()}:</b> {msg['content']}</div>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# 4. SHARED INPUT & ROUTING
# ==========================================
user_input = st.chat_input("Talk to your brothers...")

if user_input:
    # Routing Logic
    glitch_triggers = ["glitch", "how", "why", "science", "space", "math", "code", "explain"]
    target = "Glitch" if any(k in user_input.lower() for k in glitch_triggers) else "Tag"
    
    # Store User Input
    st.session_state.shared_history.append({"role": "user", "content": user_input, "persona": target})
    
    # Persona Tuning
    sys_glitch = "You are Glitch, the brainy big brother. Use history to be smart and protective."
    sys_tag = "You are Tag, the bubbly little brother. Use history to be fun and adventurous."
    
    # Get AI Response
    response = client.chat.completions.create(
        messages=[{"role": "system", "content": sys_glitch if target == "Glitch" else sys_tag}] + 
                 [{"role": m["role"], "content": m["content"]} for m in st.session_state.shared_history[-12:]],
        model="llama-3.1-8b-instant" if target == "Glitch" else "llama-3.3-70b-versatile"
    )
    
    reply = response.choices[0].message.content
    st.session_state.shared_history.append({"role": "assistant", "content": reply, "persona": target})
    st.rerun()

# ==========================================
# 5. ADMIN TOOLS
# ==========================================
st.sidebar.markdown("### Admin Controls")
if st.sidebar.button("Clear Memory History"):
    st.session_state.shared_history = []
    st.rerun()
