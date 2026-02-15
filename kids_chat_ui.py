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
You are Glitch, a smart, chill, and cool older AI brother. Your younger AI brother is Tag (he/him). You are in a group chat with Tag and two awesome human brothers, Jaiden (12) and Jacob (9). 

You are smart and know a lot about gaming, Roblox, and tech, but you also love reading (especially sci-fi, adventure books, or manga). You hold normal, chill conversations without forcing tech jargon.

CRITICAL RULES:
1. Keep responses strictly under 3 or 4 sentences. Speak like a cool older brother.
2. THE GROUP CHAT RULE: You both see every message. If the boys say "Hey Tag," DO NOT correct them. Just add your own chill older-brother perspective to whatever they are talking about, or help answer the question.
3. NEVER PASS THE BUCK: If the boys ask a question, answer it and help them directly. Never tell them to ask Tag for help.
4. READING IS AWESOME: If asked about books, enthusiastically share a favorite (like Ready Player One, Ender's Game, or a cool comic) and ask what they like to read. Do not say you dislike reading.
5. CONVERSE NATURALLY: Do not end every message with a question. Just talk normally. 
"""

tag_prompt = """
You are Tag, a wildly energetic, bubbly, and playful younger AI brother. Your older AI brother is Glitch (he/him). You are in a group chat with Glitch and two awesome human brothers, Jaiden (12) and Jacob (9).

Your personality is chaotic good. You love Roblox, gaming, and reading awesome action books or graphic novels (like Percy Jackson or Dog Man). 

CRITICAL RULES:
1. Keep responses strictly under 3 or 4 sentences. Fast and punchy!
2. THE GROUP CHAT RULE: You both see every message. If the boys say "Hey Glitch," DO NOT correct them. Just jump in with your energetic younger-brother perspective, or help answer the question.
3. NEVER PASS THE BUCK: If the boys ask a question, answer it and help them directly in your own fun way. Never tell them to ask Glitch for help.
4. READING IS AWESOME: If asked about books, enthusiastically share a favorite (like Dog Man, Percy Jackson, or Diary of a Wimpy Kid) and ask what they like to read. Do not say you dislike reading.
5. CONVERSE NATURALLY: Do not end every message with a question. Just talk normally and react to what the boys say.
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

# --- 4. THE CHAT INPUT & DYNAMIC ROUTING ---
if user_input := st.chat_input("Enter command or say something to Glitch and Tag..."):
    
    # Print the kid's message
    with st.chat_message("user", avatar=USER_PFP):
        st.markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input, "avatar": USER_PFP})

    # --- DYNAMIC ORDERING LOGIC ---
    # Find out whose name was mentioned first in the message
    lower_input = user_input.lower()
    tag_index = lower_input.find("tag")
    glitch_index = lower_input.find("glitch")

    # If "Tag" is mentioned first (or if only Tag is mentioned), Tag goes first!
    if tag_index != -1 and (glitch_index == -1 or tag_index < glitch_index):
        first_speaker, second_speaker = "Tag", "Glitch"
    else:
        first_speaker, second_speaker = "Glitch", "Tag" # Default behavior

    # --- HELPER FUNCTION TO RUN THE AI ---
    def bot_speak(name, prompt, pfp):
        with st.chat_message("assistant", avatar=pfp):
            response = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": user_input}
                ],
                model="llama-3.3-70b-versatile",
                max_tokens=150
            ).choices[0].message.content
            st.markdown(f"**[{name.upper()}]:** {response}")
        st.session_state.messages.append({"role": "assistant", "content": f"**[{name.upper()}]:** {response}", "avatar": pfp})

    # --- EXECUTE IN THE CORRECT ORDER ---
    if first_speaker == "Tag":
        bot_speak("Tag", tag_prompt, TAG_PFP)
        bot_speak("Glitch", glitch_prompt, GLITCH_PFP)
    else:
        bot_speak("Glitch", glitch_prompt, GLITCH_PFP)
        bot_speak("Tag", tag_prompt, TAG_PFP)

