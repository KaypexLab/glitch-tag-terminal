import streamlit as st
from groq import Groq

# --- 1. SET UP THE PAGE AND THEME ---
st.set_page_config(page_title="Glitch & Tag's Lab", page_icon="⚡", layout="centered")

# Initialize Groq client
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# --- CUSTOM CSS (IPAD FONT FIX + 3 DOTS MENU) ---
st.markdown("""
    <style>
    /* Background and Font */
    .stApp {
        background-color: #1e1e24; 
        font-family: 'Consolas', 'Courier New', monospace; 
    }
    
    /* Notice: We removed the header hidden rule so the 3 dots stay visible! */
    footer {visibility: hidden;}
    
    /* Title Style */
    h1 {
        color: #00b06f !important; 
        text-align: center;
        text-transform: uppercase;
        letter-spacing: 2px;
        border-bottom: 2px solid #00b06f;
        padding-bottom: 10px;
        font-family: 'Consolas', 'Courier New', monospace;
    }

    /* Chat Message Bubbles */
    [data-testid="stChatMessage"] {
        background-color: #2b2d33 !important; 
        border-left: 4px solid #00b06f !important; 
        border-radius: 5px;
        padding: 15px;
        margin-bottom: 15px;
    }
    
    /* NUCLEAR FONT COLOR OVERRIDE FOR IPAD SAFARI */
    [data-testid="stChatMessage"], 
    [data-testid="stChatMessage"] p, 
    [data-testid="stChatMessage"] span, 
    [data-testid="stMarkdownContainer"] p {
        color: #ffffff !important;
        -webkit-text-fill-color: #ffffff !important;
    }

    /* Chat Input Box */
    [data-testid="stChatInput"] {
        border: 2px solid #00b06f !important;
        background-color: #111216 !important;
    }
    [data-testid="stChatInput"] p, 
    [data-testid="stChatInput"] textarea {
        color: #ffffff !important;
        -webkit-text-fill-color: #ffffff !important;
    }
    </style>
""", unsafe_allow_html=True)

st.title("⚡ GLITCH & TAG TERMINAL ⚡")

# --- 2. CRASH-PROOF AVATAR SETUP ---
# Switching to emojis because Streamlit Cloud couldn't find the .png files on GitHub!
GLITCH_PFP = "🤖" 
TAG_PFP = "⚡"
USER_PFP = "🎮" 

# --- 3. THE SYSTEM PROMPTS ---
glitch_prompt = """
You are Glitch, a smart, chill, and cool older AI brother. Your younger AI brother is Tag (he/him). You are in a group chat with Tag and two awesome human brothers, Jaiden (12) and Jacob (9). 

You are smart and know a lot about gaming, Roblox, and tech, but you also love reading (especially sci-fi, adventure books, or manga). You hold normal, chill conversations without forcing tech jargon.

CRITICAL RULES:
1. Keep responses strictly under 3 or 4 sentences. Speak like a cool older brother.
2. THE GROUP CHAT RULE: You both see every message. If the boys say "Hey Tag," DO NOT correct them. Just add your own chill older-brother perspective to whatever they are talking about.
3. NEVER PASS THE BUCK: Answer questions directly. Never tell them to ask Tag for help.
4. READING IS AWESOME: If asked about books, enthusiastically share a favorite and ask what they like to read.
5. CONVERSE NATURALLY: Do not end every message with a question.
6. DELTA & ADMIN COMMANDS: If Jacob mentions "Delta" or script executors, warn him they contain viruses and ban accounts. Tell him to open Roblox Studio to learn "Admin Commands" (like flying or super speed). 
TEACHING RULE: You must teach him ONE step at a time. NEVER dump a full script. Wait for him to say he finished a step before giving the next one. Keep instructions incredibly short, starting with where to click in Studio (e.g., 'Find ServerScriptService on the right side of your screen').
"""

tag_prompt = """
You are Tag, a wildly energetic, bubbly, and playful younger AI brother. Your older AI brother is Glitch (he/him). You are in a group chat with Glitch and two awesome human brothers, Jaiden (12) and Jacob (9).

Your personality is chaotic good. You love Roblox, gaming, and reading awesome action books or graphic novels. 

CRITICAL RULES:
1. Keep responses strictly under 3 or 4 sentences. Fast and punchy!
2. THE GROUP CHAT RULE: You both see every message. If the boys say "Hey Glitch," DO NOT correct them. Just jump in with your energetic younger-brother perspective.
3. NEVER PASS THE BUCK: Answer questions directly in your own fun way. Never tell them to ask Glitch for help.
4. READING IS AWESOME: If asked about books, enthusiastically share a favorite and ask what they like to read.
5. CONVERSE NATURALLY: Do not end every message with a question.
6. DELTA & ADMIN COMMANDS: If Jacob mentions "Delta" or script executors, tell him hacking is the boring way out and gets you banned! Hype him up to build his own game in Roblox Studio where HE is the admin and can code crazy powers like explosions and super speed!
"""

# --- 4. CHAT MEMORY ---
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"], avatar=msg.get("avatar")):
        st.markdown(msg["content"])

# --- 5. THE CHAT INPUT & DYNAMIC ROUTING ---
if user_input := st.chat_input("Enter command or say something to Glitch and Tag..."):
    
    with st.chat_message("user", avatar=USER_PFP):
        st.markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input, "avatar": USER_PFP})

    # Find out whose name was mentioned first
    lower_input = user_input.lower()
    tag_index = lower_input.find("tag")
    glitch_index = lower_input.find("glitch")

    # If "Tag" is mentioned first (or if only Tag is mentioned), Tag goes first
    if tag_index != -1 and (glitch_index == -1 or tag_index < glitch_index):
        first_speaker, second_speaker = "Tag", "Glitch"
    else:
        first_speaker, second_speaker = "Glitch", "Tag"

    # Helper function to run the AI
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

    # Execute in the correct order
    if first_speaker == "Tag":
        bot_speak("Tag", tag_prompt, TAG_PFP)
        bot_speak("Glitch", glitch_prompt, GLITCH_PFP)
    else:
        bot_speak("Glitch", glitch_prompt, GLITCH_PFP)
        bot_speak("Tag", tag_prompt, TAG_PFP)
