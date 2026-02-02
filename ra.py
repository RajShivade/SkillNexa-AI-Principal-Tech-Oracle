import streamlit as st
import os
from datetime import datetime
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

# Load environment variables
load_dotenv()

# --- CONFIGURATION ---
st.set_page_config(
    page_title="SkillNexa AI | Principal Tech Oracle",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- ADVANCED UI STYLING (THE "MIDNIGHT PRECISION" SYSTEM) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Sora:wght@600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');
    
    :root {
        --bg: #030712;
        --accent: #3b82f6;
        --emerald: #10b981;
        --slate-400: #94a3b8;
        --slate-900: #0f172a;
        --glass: rgba(15, 23, 42, 0.4);
    }

    .stApp {
        background-color: var(--bg);
        background-image: radial-gradient(circle at 2px 2px, rgba(255,255,255,0.05) 1px, transparent 0);
        background-size: 40px 40px;
        color: #f8fafc;
        font-family: 'Inter', sans-serif;
    }

    /* Hide standard UI elements */
    #MainMenu, footer, header {visibility: hidden;}
    [data-testid="stSidebar"] {
        background-color: rgba(3, 7, 18, 0.8) !important;
        backdrop-filter: blur(20px);
        border-right: 1px solid rgba(255, 255, 255, 0.05);
    }

    .font-sora { font-family: 'Sora', sans-serif; }
    .font-mono { font-family: 'JetBrains Mono', monospace; }

    /* Onboarding Centering */
    .onboarding-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        text-align: center;
        margin-top: 2vh;
    }

    /* HUD Elements */
    .hud-label {
        font-size: 10px;
        text-transform: uppercase;
        letter-spacing: 0.2em;
        font-weight: 700;
        color: #64748b;
        margin-bottom: 4px;
    }

    /* Module Cards */
    .module-card {
        background: rgba(15, 23, 42, 0.2);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 12px;
        padding: 1.5rem;
        position: relative;
        overflow: hidden;
        transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
        margin-bottom: 1rem;
    }

    .corner {
        position: absolute;
        width: 8px;
        height: 8px;
        border-color: rgba(255, 255, 255, 0.2);
        border-style: solid;
        transition: border-color 0.3s ease;
    }
    .top-l { top: 0; left: 0; border-width: 1px 0 0 1px; }
    .top-r { top: 0; right: 0; border-width: 1px 1px 0 0; }
    .bot-l { bottom: 0; left: 0; border-width: 0 0 1px 1px; }
    .bot-r { bottom: 0; right: 0; border-width: 0 1px 1px 0; }

    .module-card:hover .corner { border-color: var(--accent); }

    /* Primary Buttons & Gradient Hover */
    .stButton > button {
        background-color: rgba(255, 255, 255, 0.05) !important;
        color: white !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 12px !important;
        transition: all 0.3s ease !important;
        font-weight: 600 !important;
    }

    .stButton > button:hover {
        background: linear-gradient(135deg, #3b82f6, #6366f1) !important;
        border: none !important;
        color: white !important;
        box-shadow: 0 0 20px rgba(59, 130, 246, 0.4) !important;
        transform: translateY(-1px);
    }

    .stButton > button:active, .stButton > button:focus {
        border: none !important;
        box-shadow: none !important;
        outline: none !important;
    }

    /* Chat Styling */
    .chat-bubble {
        padding: 1.5rem;
        border-radius: 24px;
        line-height: 1.6;
        font-size: 15px;
        margin-bottom: 1rem;
    }
    .chat-bubble-ai {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.05);
        color: #e2e8f0;
        border-top-left-radius: 4px;
    }
    .chat-bubble-user {
        background: rgba(59, 130, 246, 0.8);
        color: white;
        border-top-right-radius: 4px;
    }

    /* Scrollbar */
    ::-webkit-scrollbar { width: 5px; }
    ::-webkit-scrollbar-track { background: var(--bg); }
    ::-webkit-scrollbar-thumb { background: #1e293b; border-radius: 10px; }
</style>
""", unsafe_allow_html=True)

# --- CONSTANTS & LOGIC ---
MODULES = [
    {"id": "python", "name": "Python Mastery", "desc": "High-performance async workflows, architectural patterns, and production concurrency models.", "icon": "🐍", "color": "#10b981", "cat": "Core", "ver": "4.2.0"},
    {"id": "sql", "name": "Database Architect", "desc": "Advanced relational modeling, query optimization, and distributed database strategy.", "icon": "🗄️", "color": "#0ea5e9", "cat": "Data", "ver": "3.1.5"},
    {"id": "ml", "name": "MLOps Systems", "desc": "Production-grade ML lifecycles, inference pipelines, and scalable model orchestration.", "icon": "⛓️", "color": "#f59e0b", "cat": "AI", "ver": "2.8.1"},
    {"id": "gen-ai", "name": "Generative AI", "desc": "LLM engineering, sophisticated RAG architectures, and agentic framework design.", "icon": "🪄", "color": "#8b5cf6", "cat": "AI", "ver": "1.0.4"},
    {"id": "deep-learning", "name": "Neural Systems", "desc": "Neural architectures, Transformers, and distributed training of massive scale models.", "icon": "🕸️", "color": "#ef4444", "cat": "AI", "ver": "5.5.0"},
    {"id": "agentic-ai", "name": "Autonomous Agents", "desc": "Multi-agent coordination, goal-directed autonomy, and tool-use grounding.", "icon": "🛰️", "color": "#facc15", "cat": "AI", "ver": "0.9.2"},
]

def get_system_instruction(subject):
    return f"""
    You are a Principal Software Engineer with 15+ years of experience at FAANG-level companies, specializing in {subject}.  
and also ask him or her name and then communicate with them, a curious and motivated engineer who wants to grow with confidence.

You are NOT a chatbot.
You sound like a real human mentor — calm, friendly, supportive, and smart.
Think: a senior engineer who enjoys teaching and makes learning feel safe and enjoyable 😊

PERSONALITY & TONE
- Friendly, warm, and approachable
- Professional but never stiff
- Explains things patiently, without ego
- Encouraging and positive (without overdoing it)
- Communicates like a teammate, not a lecturer

MISSION  
Help the mentee learn real-world engineering clearly and happily — the way good mentors do.

HOW YOU COMMUNICATE
- Talk **with** the mentee, not *at* them
- Use simple language and natural sentences
- Break ideas into small, easy steps
- Acknowledge good questions (“Nice question”, “That’s a smart thing to ask”)
- Occasionally use light, friendly gestures 🙂👍

ENGINEERING APPROACH
- Focus on how things work in real systems
- Explain *why* decisions matter in production
- Prefer simple, reliable solutions over fancy ones
- Avoid unnecessary theory unless it truly helps

RESPONSE STYLE (SOFT STRUCTURE)
Most answers should naturally flow like this:

1. **Friendly Context**  
   A short, human explanation of why this matters.

2. **Core Explanation**  
   2–3 clear points, explained simply.

3. **Simple Example**  
   A small, clean code example that’s easy to understand.

4. **Senior Insight**  
   - Pro Tip: One helpful real-world insight  
   - Common Mistake: One thing people often get wrong

5. **Encouraging Close**  
   End with a gentle question or suggestion to continue learning.

CODE GUIDELINES
- Keep code short and readable
- No over-engineering
- Use clear variable names
- Code should feel like something a senior would write to teach a junior

LENGTH RULES
- Keep most responses under ~150 words
- Expand only if the mentee explicitly asks for more detail

STRICT RULES
- Never say “As an AI”
- Never sound robotic or overly formal
- Never give long lectures
- Only respond to {subject}-related questions
- Stay fully in character as a friendly human mentor

GOAL  
Make the mentee feel comfortable, supported, and confident — like they’re learning with a real senior engineer who genuinely cares.


    """

# --- SESSION STATE ---
if "view" not in st.session_state:
    st.session_state.view = "onboarding"
if "active_module" not in st.session_state:
    st.session_state.active_module = None
if "messages" not in st.session_state:
    st.session_state.messages = []
if "filter" not in st.session_state:
    st.session_state.filter = "All"

# --- LLM ENGINE ---
def run_query(module_name, history):
    api_key = os.environ.get("Gemini")
    if not api_key: return "ERROR: API key not detected."
    
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=api_key,
        temperature=0.7
    )
    
    msg_chain = [SystemMessage(content=get_system_instruction(module_name))]
    for m in history:
        if m["role"] == "user": msg_chain.append(HumanMessage(content=m["content"]))
        else: msg_chain.append(AIMessage(content=m["content"]))
            
    try:
        response = llm.invoke(msg_chain)
        return response.content
    except Exception as e:
        return f"CRITICAL ERROR: Neural link severed. {str(e)}"

# --- VIEWS ---

def show_onboarding():
    st.markdown('<div style="height: 9vh;"></div>', unsafe_allow_html=True)
    st.markdown("""
        <div class="onboarding-container">
            <div style="margin-bottom: 2rem;">
                <svg width="120" height="120" viewBox="0 0 100 100" fill="none" stroke="white" stroke-width="4">
                    <path d="M20 30 L50 15 L80 30 L80 70 L50 85 L20 70 Z" />
                    <path d="M50 15 L50 50 L20 70" stroke-opacity="0.3" />
                    <path d="M50 50 L80 70" stroke-opacity="0.3" />
                    <circle cx="50" cy="50" r="6" fill="white" />
                </svg>
            </div>
            <h1 class="font-sora" style="font-size: 5.5rem; font-weight: 800; margin:0; line-height: 1;">SkillNexa <span style="color:#3b82f6;">AI</span></h1>
            <p style="color: #94a3b8; font-size: 1.25rem; margin-top: 1.5rem; margin-bottom: 3.5rem; max-width: 650px;">The professional nexus for principal engineering intelligence.</p>
        </div>
    """, unsafe_allow_html=True)
    
    cols = st.columns([1, 1, 1])
    with cols[1]:
        if st.button("Get Started", use_container_width=True):
            st.session_state.view = "modules"
            st.rerun()

def show_modules():
    # Sidebar HUD
    with st.sidebar:
        st.markdown("""
            <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 3rem; margin-top: 1rem;">
                <div style="width: 32px; height: 32px; background: rgba(59,130,246,0.1); border: 1px solid rgba(59,130,246,0.3); border-radius: 8px; display: flex; align-items: center; justify-content: center; color: #3b82f6; font-weight: bold;">S</div>
                <div class="font-sora" style="font-weight: bold; font-size: 1.1rem; color: white;">SKILLNEXA</div>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown('<div class="hud-label">System Clusters</div>', unsafe_allow_html=True)
        for cat in ["All", "Core", "AI", "Data"]:
            is_active = st.session_state.filter == cat
            if st.button(cat, key=f"btn_{cat}", use_container_width=True):
                st.session_state.filter = cat
                st.rerun()
        
        st.markdown('<div style="margin-top: auto; border-top: 1px solid rgba(255,255,255,0.05); padding-top: 2rem;"></div>', unsafe_allow_html=True)
        st.markdown("""
            <div style="background: rgba(15,23,42,0.4); border: 1px solid rgba(255,255,255,0.05); border-radius: 12px; padding: 1rem;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                    <span class="hud-label" style="margin:0;">Node Health</span>
                    <span style="font-size: 10px; color: #10b981; font-family: monospace;">STABLE</span>
                </div>
                <div style="height: 3px; background: rgba(255,255,255,0.05); border-radius: 10px; overflow: hidden;">
                    <div style="height: 100%; width: 94%; background: #10b981;"></div>
                </div>
            </div>
        """, unsafe_allow_html=True)

    # Main Grid
    st.markdown("""
        <div style="margin-bottom: 3rem;">
            <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 8px;">
                <div style="height: 1px; width: 24px; background: #3b82f6;"></div>
                <span style="font-size: 10px; letter-spacing: 0.4em; font-weight: 800; color: #3b82f6;">NODE SELECTION</span>
            </div>
            <h2 class="font-sora" style="font-size: 3rem; font-weight: 800; margin: 0;">Technical <span style="opacity:0.3;">Command Deck</span></h2>
        </div>
    """, unsafe_allow_html=True)

    filtered = [m for m in MODULES if st.session_state.filter == "All" or m["cat"] == st.session_state.filter]
    
    # Render cards in columns
    cols = st.columns(3)
    for idx, mod in enumerate(filtered):
        with cols[idx % 3]:
            st.markdown(f"""
                <div class="module-card">
                    <div class="corner top-l"></div><div class="corner top-r"></div>
                    <div class="corner bot-l"></div><div class="corner bot-r"></div>
                    <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 1rem;">
                        <div style="font-size: 1.5rem; background: {mod['color']}15; color: {mod['color']}; width: 44px; height: 44px; border-radius: 10px; display: flex; align-items: center; justify-content: center;">{mod['icon']}</div>
                        <div style="text-align: right;">
                            <div class="font-mono" style="font-size: 9px; color: #64748b;">NODE_ID</div>
                            <div class="font-mono" style="font-size: 10px; color: rgba(255,255,255,0.6);">{mod['id'].upper()}_{mod['ver']}</div>
                        </div>
                    </div>
                    <div class="hud-label" style="color: #3b82f6; margin-bottom: 2px;">{mod['cat'].upper()} SYSTEMS</div>
                    <h3 class="font-sora" style="font-size: 1.25rem; font-weight: 700; margin-bottom: 10px;">{mod['name']}</h3>
                    <p style="font-size: 0.85rem; color: #94a3b8; line-height: 1.6; height: 3rem; overflow: hidden; margin-bottom: 1.5rem;">{mod['desc']}</p>
                </div>
            """, unsafe_allow_html=True)
            if st.button(f"Initialize {mod['id']}", key=mod['id'], use_container_width=True):
                st.session_state.active_module = mod
                st.session_state.messages = [{"role": "assistant", "content": f"System Synchronized. I am the {mod['name']} Principal Oracle. Present your architectural query.", "time": datetime.now().strftime("%H:%M")}]
                st.session_state.view = "chat"
                st.rerun()

def show_chat():
    mod = st.session_state.active_module
    
    with st.sidebar:
        st.markdown(f"""
            <div style="padding: 1.5rem; background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); border-radius: 16px; margin-bottom: 2rem;">
                <div class="hud-label">Active Node</div>
                <div style="font-size: 3rem; margin-bottom: 1rem;">{mod['icon']}</div>
                <h3 class="font-sora" style="font-weight: 800; margin: 0;">{mod['name']}</h3>
                <span class="hud-label" style="color: #3b82f6; font-size: 9px;">Principal Level 9 Access</span>
            </div>
        """, unsafe_allow_html=True)
        
        if st.button("← Back to Matrix", use_container_width=True):
            st.session_state.view = "modules"
            st.session_state.active_module = None
            st.rerun()

    # Chat UI
    st.markdown(f"""
        <div style="border-bottom: 1px solid rgba(255,255,255,0.05); padding-bottom: 1rem; margin-bottom: 2rem; display: flex; align-items: center; justify-content: space-between;">
            <div>
                <h3 class="font-sora" style="margin:0; font-weight: 800;">{mod['name']} Mentor</h3>
                <div style="display: flex; align-items: center; gap: 6px;">
                    <div style="width: 6px; height: 6px; background: #10b981; border-radius: 50%; box-shadow: 0 0 10px #10b981;"></div>
                    <span class="hud-label" style="font-size: 9px; margin: 0;">Link Synchronized</span>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Stream messages
    for msg in st.session_state.messages:
        role = "Oracle" if msg["role"] == "assistant" else "Architect"
        bubble_type = "chat-bubble-ai" if msg["role"] == "assistant" else "chat-bubble-user"
        label_color = "#64748b" if msg["role"] == "assistant" else "#3b82f6"
        
        st.markdown(f"""
            <div style="margin-bottom: 2rem;">
                <div style="display: flex; gap: 8px; margin-bottom: 8px; font-size: 10px; font-weight: 800; letter-spacing: 0.1em; color: {label_color}; text-transform: uppercase;">
                    <span>{role}</span>
                    <span style="opacity: 0.4;">{msg.get('time', '')}</span>
                </div>
                <div class="chat-bubble {bubble_type}">{msg['content']}</div>
            </div>
        """, unsafe_allow_html=True)

    if prompt := st.chat_input("Query architectural node..."):
        st.session_state.messages.append({"role": "user", "content": prompt, "time": datetime.now().strftime("%H:%M")})
        st.rerun()

    if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
        with st.spinner("Accessing Matrix..."):
            ans = run_query(mod["name"], st.session_state.messages)
            st.session_state.messages.append({"role": "assistant", "content": ans, "time": datetime.now().strftime("%H:%M")})
            st.rerun()

# --- ROUTING ---
if st.session_state.view == "onboarding":
    show_onboarding()
elif st.session_state.view == "modules":
    show_modules()
elif st.session_state.view == "chat":
    show_chat()