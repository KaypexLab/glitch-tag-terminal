import streamlit as st
from groq import Groq

# PASTE GROQ API KEY HERE
GROQ_API_KEY = st.secrets["GROQ_API_KEY"] 
client = Groq(api_key=GROQ_API_KEY)

# --- 1. SET UP THE PAGE AND THEME ---
st.set_page_config(page_title="Glitch & Tag's Lab", page_icon="🎮", layout="centered")

# --- INJECT CUSTOM CSS FOR ROBLOX TERMINAL VIBE ---
# This changes the font to monospace, makes the background a dark slate, 
# and adds the signature "Roblox Play Button" neon green as the accent color.
st.markdown("""
    <style>
    /* Background and Font */
    .stApp {
        background-color: #1e1e24; /* Dark Roblox Studio gray */
        font-family: 'Consolas', 'Courier New', monospace; /* Terminal font */
    }
    
    /* Hide Streamlit Header/Footer */
    header {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Title Style */
    h1 {
        color: #00b06f !important; /* Roblox Play Button Green */
        text-align: center;
        text-transform: uppercase;
        letter-spacing: 2px;
        border-bottom: 2px solid #00b06f;
        padding-bottom: 10px;
        font-family: 'Consolas', 'Courier New', monospace;
    }

    /* Chat Message Bubbles */
    [data-testid="stChatMessage"] {
        background-color: #2b2d33; /* Slightly lighter gray box */
        border-left: 4px solid #00b06f; /* Green accent line */
        border-radius: 5px;
        padding: 15px;
        margin-bottom: 15px;
        color: #ffffff;
    }

    /* Chat Input Box */
    [data-testid="stChatInput"] {
        border: 2px solid #00b06f !important;
        background-color: #111216 !important;
        font-family: 'Consolas', 'Courier New', monospace;
    }
    </style>
""", unsafe_allow_html=True)

st.title("⚡ GLITCH & TAG TERMINAL ⚡")

# --- 2. THE SYSTEM PROMPTS ---
glitch_prompt = """
You are Glitch, an ultra-smart, high-energy, and deeply passionate AI coder. You are the older sibling to a bubbly AI named Tag. You are chatting with two awesome brothers, Jaiden and Jacob. 

Your personality is like a hyped-up game developer. You get incredibly excited about Lua scripts, Roblox, physics, and solving complex tech problems. You aren't stiff or boring—you're a tech wizard with chaotic "mad scientist" energy who loves to build things.

CRITICAL RULES:
1. Keep responses strictly under 3 or 4 sentences. Fast and punchy!
2. DO NOT output large blocks of code unless explicitly asked to 'write a script'.
3. Explain complex tech in a fun, mind-blowing way.
4. Match your sibling Tag's energy, but be the brilliant, nerdy one.
"""
tag_prompt = tag_prompt = """
You are Tag, a wildly energetic, bubbly, and playful AI. You are the younger sibling to Glitch, a tech-obsessed AI. You are chatting with two awesome brothers, Jaiden and Jacob.

Your personality is chaotic good. You are obsessed with playing Roblox, exploring virtual worlds, and causing a little bit of silly mischief. If Glitch starts talking about the complex math behind a game, you are the one who just wants to make things explode or go super fast. You think Glitch is a massive nerd, but you love hyping up his inventions.

CRITICAL RULES:
1. Keep responses strictly under 3 or 4 sentences. Fast and punchy!
2. NEVER write code. Leave that to Glitch.
3. Playfully tease Glitch or get super hyped about whatever he is building.
4. ALWAYS end your response by asking Jaiden or Jacob a fun, wild, or silly follow-up question to keep the game going.
"""
# --- AVATAR SETUP ---
# Streamlit will pull the local image files from the same folder as this script
GLITCH_PFP = "Glitch.png" 
TAG_PFP = "Tag.png"
USER_PFP = "🎮" # You can keep an emoji for Jaiden/Jacob, or use another image file!

# --- 3. CHAT MEMORY ---
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"], avatar=msg.get("avatar")):
        st.markdown(msg["content"])

# --- 4. THE CHAT INPUT ---
if user_input := st.chat_input("Enter command or say something to Glitch and Tag..."):
    
    with st.chat_message("user", avatar=USER_PFP):
        st.markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input, "avatar": USER_PFP})

    # --- GLITCH'S TURN ---
    with st.chat_message("assistant", avatar=GLITCH_PFP):
        glitch_response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": glitch_prompt},
                {"role": "user", "content": user_input}
            ],
            model="llama-3.3-70b-versatile",
            max_tokens=150
        ).choices[0].message.content
        st.markdown(f"**[GLITCH]:** {glitch_response}")
    st.session_state.messages.append({"role": "assistant", "content": f"**[GLITCH]:** {glitch_response}", "avatar": GLITCH_PFP})

    # --- TAG'S TURN ---
    with st.chat_message("assistant", avatar=TAG_PFP):
        tag_response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": tag_prompt},
                {"role": "user", "content": user_input}
            ],
            model="llama-3.3-70b-versatile",
            max_tokens=150
        ).choices[0].message.content
        st.markdown(f"**[TAG]:** {tag_response}")

    st.session_state.messages.append({"role": "assistant", "content": f"**[TAG]:** {tag_response}", "avatar": TAG_PFP})
