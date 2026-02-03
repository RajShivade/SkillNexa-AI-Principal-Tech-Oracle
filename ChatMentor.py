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

# --- ADVANCED UI STYLING (MIDNIGHT PRECISION SYSTEM) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Sora:wght@600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');
    
    :root {
        --bg: #030712;
        --accent: #3b82f6;
        --emerald: #10b981;
        --slate-400: #94a3b8;
        --glass: rgba(15, 23, 42, 0.6);
        --border: rgba(255, 255, 255, 0.05);
    }

    .stApp {
        background-color: var(--bg);
        background-image: radial-gradient(circle at 2px 2px, rgba(255,255,255,0.03) 1px, transparent 0);
        background-size: 40px 40px;
        color: #f8fafc;
        font-family: 'Inter', sans-serif;
    }

    /* Remove standard Streamlit padding/header */
    .main .block-container {
        padding-top: 2rem;
        max-width: 1200px;
    }
    header {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    .font-sora { font-family: 'Sora', sans-serif; }
    .font-mono { font-family: 'JetBrains Mono', monospace; }

    /* Module Selection UI */
    .module-card {
        background: rgba(15, 23, 42, 0.4);
        border: 1px solid var(--border);
        border-radius: 16px;
        padding: 1.5rem;
        transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
        position: relative;
        overflow: hidden;
    }
    .module-card:hover {
        border-color: var(--accent);
        background: rgba(15, 23, 42, 0.6);
    }
    
    .hud-label {
        font-size: 10px;
        text-transform: uppercase;
        letter-spacing: 0.2em;
        font-weight: 800;
        color: var(--accent);
        margin-bottom: 8px;
    }

    /* Chat UI Navigation Header */
    .chat-nav-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 1.5rem;
        background: rgba(3, 7, 18, 0.8);
        backdrop-filter: blur(20px);
        border-bottom: 1px solid var(--border);
        border-radius: 16px;
        margin-bottom: 2rem;
        position: sticky;
        top: 0;
        z-index: 1000;
    }

    /* Chat Bubbles */
    .chat-msg-container {
        display: flex;
        flex-direction: column;
        gap: 1.5rem;
        margin-bottom: 2rem;
    }
    
    .bubble {
        padding: 1.25rem 1.5rem;
        border-radius: 18px;
        font-size: 15px;
        line-height: 1.6;
        max-width: 85%;
        position: relative;
    }
    
    .bubble-ai {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid var(--border);
        color: #e2e8f0;
        border-top-left-radius: 2px;
        align-self: flex-start;
    }
    
    .bubble-user {
        background: #2563eb;
        color: white;
        border-top-right-radius: 2px;
        align-self: flex-end;
    }

    .msg-label {
        font-size: 10px;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        margin-bottom: 6px;
        opacity: 0.5;
    }

    /* Buttons */
    .stButton > button {
        background: rgba(255, 255, 255, 0.05) !important;
        color: white !important;
        border: 1px solid var(--border) !important;
        border-radius: 12px !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
    }
    .stButton > button:hover {
        background: var(--accent) !important;
        border-color: var(--accent) !important;
        box-shadow: 0 0 20px rgba(59, 130, 246, 0.4) !important;
    }
    
    /* Input customization */
    .stChatInputContainer {
        background-color: transparent !important;
        border: none !important;
    }
    .stChatInput {
        background-color: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid var(--border) !important;
        border-radius: 16px !important;
        color: white !important;
    }
</style>
""", unsafe_allow_html=True)

# --- CONSTANTS & MODULES ---
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

# --- LLM SERVICE ---
def get_ai_response(module_name, history):
    api_key = os.getenv("Gemini")
    if not api_key:
        return "ERROR: Neural Link failed. API Key missing."
    
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=api_key,
        temperature=0.7
    )
    
    msg_chain = [SystemMessage(content=get_system_instruction(module_name))]
    for m in history:
        if m["role"] == "user":
            msg_chain.append(HumanMessage(content=m["content"]))
        else:
            msg_chain.append(AIMessage(content=m["content"]))
            
    try:
        response = llm.invoke(msg_chain)
        return response.content
    except Exception as e:
        return f"CRITICAL ERROR: Neural Link Severed. {str(e)}"

# --- VIEW: ONBOARDING ---
def show_onboarding():
    st.markdown('<div style="height: 10vh;"></div>', unsafe_allow_html=True)
    st.markdown("""
        <div style="text-align: center; margin-bottom: 3rem;">
            <div style="margin-bottom: 2rem; display: flex; justify-content: center;">
                <svg width="120" height="120" viewBox="0 0 100 100" fill="none" stroke="white" stroke-width="2">
                    <path d="M20 30 L50 15 L80 30 L80 70 L50 85 L20 70 Z" />
                    <path d="M50 15 L50 50 L20 70" stroke-opacity="0.2" />
                    <path d="M50 50 L80 70" stroke-opacity="0.2" />
                    <circle cx="50" cy="50" r="4" fill="white" />
                </svg>
            </div>
            <h1 class="font-sora" style="font-size: 5rem; font-weight: 800; margin-bottom: 0.5rem; letter-spacing: -0.02em;">SkillNexa <span style="color:#3b82f6;">AI</span></h1>
            <p style="color: #94a3b8; font-size: 1.25rem; max-width: 700px; margin: 0 auto; line-height: 1.6;">The professional nexus for principal engineering intelligence. High-fidelity architectural mentoring for the next generation of builders.</p>
        </div>
    """, unsafe_allow_html=True)
    
    _, col, _ = st.columns([1, 1, 1])
    with col:
        if st.button("Get Started", use_container_width=True, type="primary"):
            st.session_state.view = "modules"
            st.rerun()

# --- VIEW: MODULES ---
def show_modules():
    # Sidebar for filtering (only visible in modules view)
    with st.sidebar:
        st.markdown('<div class="hud-label">System Clusters</div>', unsafe_allow_html=True)
        filters = ["All", "Core", "AI", "Data"]
        for f in filters:
            if st.button(f, use_container_width=True, type="primary" if st.session_state.filter == f else "secondary"):
                st.session_state.filter = f
                st.rerun()
        
        st.markdown('<div style="height: 10vh;"></div>', unsafe_allow_html=True)
        st.markdown("""
            <div style="background: rgba(15,23,42,0.4); border: 1px solid var(--border); border-radius: 12px; padding: 1rem;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                    <span style="font-size: 10px; font-weight: 800; color: #64748b; letter-spacing: 0.1em;">NODE HEALTH</span>
                    <span style="font-size: 10px; color: #10b981; font-family: monospace;">STABLE</span>
                </div>
                <div style="height: 3px; background: rgba(255,255,255,0.05); border-radius: 10px;">
                    <div style="height: 100%; width: 94%; background: #10b981;"></div>
                </div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("""
        <div style="margin-bottom: 3rem;">
            <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 8px;">
                <div style="height: 1px; width: 24px; background: #3b82f6;"></div>
                <span style="font-size: 10px; letter-spacing: 0.4em; font-weight: 800; color: #3b82f6;">NODE SELECTION</span>
            </div>
            <h1 class="font-sora" style="font-size: 3rem; font-weight: 800; margin: 0;">Technical <span style="opacity:0.3;">Command Deck</span></h1>
        </div>
    """, unsafe_allow_html=True)

    filtered = [m for m in MODULES if st.session_state.filter == "All" or m["cat"] == st.session_state.filter]
    
    # 3-column grid
    for i in range(0, len(filtered), 3):
        cols = st.columns(3)
        for j in range(3):
            if i + j < len(filtered):
                mod = filtered[i + j]
                with cols[j]:
                    st.markdown(f"""
                        <div class="module-card">
                            <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 1.5rem;">
                                <div style="font-size: 1.5rem; background: {mod['color']}15; color: {mod['color']}; width: 44px; height: 44px; border-radius: 10px; display: flex; align-items: center; justify-content: center;">{mod['icon']}</div>
                                <div style="text-align: right;">
                                    <div class="font-mono" style="font-size: 9px; color: #64748b;">NODE_ID</div>
                                    <div class="font-mono" style="font-size: 10px; color: rgba(255,255,255,0.6);">{mod['id'].upper()}_{mod['ver']}</div>
                                </div>
                            </div>
                            <div class="hud-label">{mod['cat']} SYSTEMS</div>
                            <h3 class="font-sora" style="font-size: 1.25rem; font-weight: 700; margin-bottom: 10px;">{mod['name']}</h3>
                            <p style="font-size: 0.85rem; color: #94a3b8; line-height: 1.6; height: 3.5rem; overflow: hidden; margin-bottom: 1.5rem;">{mod['desc']}</p>
                        </div>
                    """, unsafe_allow_html=True)
                    if st.button(f"Initialize {mod['id']}", key=mod['id'], use_container_width=True):
                        st.session_state.active_module = mod
                        st.session_state.view = "chat"
                        st.session_state.messages = [
                            {"role": "assistant", "content": f"System Synchronized. I am the {mod['name']} Principal Oracle. Before we begin our architectural session, could you tell me your name?", "time": datetime.now().strftime("%H:%M")}
                        ]
                        st.rerun()

# --- VIEW: CHAT ---
def show_chat():
    mod = st.session_state.active_module
    
    # Custom Header with Back Button
    col_back, col_info = st.columns([1, 4])
    with col_back:
        if st.button("← Back to Matrix", use_container_width=True):
            st.session_state.view = "modules"
            st.session_state.active_module = None
            st.session_state.messages = []
            st.rerun()
            
    st.markdown(f"""
        <div class="chat-nav-header">
            <div style="display: flex; align-items: center; gap: 1rem;">
                <div style="font-size: 2rem;">{mod['icon']}</div>
                <div>
                    <h3 class="font-sora" style="margin:0; font-size: 1.25rem; font-weight: 800;">{mod['name']} Mentor</h3>
                    <div style="display: flex; align-items: center; gap: 6px;">
                        <div style="width: 6px; height: 6px; background: #10b981; border-radius: 50%; box-shadow: 0 0 10px #10b981;"></div>
                        <span style="font-size: 9px; font-weight: 800; color: #64748b; letter-spacing: 0.1em; text-transform: uppercase;">Session Active</span>
                    </div>
                </div>
            </div>
            <div style="text-align: right; display: none; md: block;">
                <div style="font-size: 9px; font-weight: 800; color: #64748b; letter-spacing: 0.1em; text-transform: uppercase;">Active Protocol</div>
                <div class="font-mono" style="font-size: 11px; color: #3b82f6;">PRINCIPAL_ORACLE_V{mod['ver']}</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Chat History
    chat_container = st.container()
    with chat_container:
        for msg in st.session_state.messages:
            role_label = "Principal Oracle" if msg["role"] == "assistant" else "Lead Architect"
            bubble_type = "bubble-ai" if msg["role"] == "assistant" else "bubble-user"
            label_align = "flex-start" if msg["role"] == "assistant" else "flex-end"
            
            st.markdown(f"""
                <div class="chat-msg-container">
                    <div style="display: flex; flex-direction: column; align-items: {label_align};">
                        <div class="msg-label">{role_label} • {msg.get('time', '')}</div>
                        <div class="bubble {bubble_type}">
                            {msg['content']}
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)

    # Chat Input
    if prompt := st.chat_input("Query architectural node..."):
        # User message
        st.session_state.messages.append({"role": "user", "content": prompt, "time": datetime.now().strftime("%H:%M")})
        st.rerun()

    # Handling Response
    if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
        with st.spinner("Oracle is processing..."):
            response = get_ai_response(mod["name"], st.session_state.messages)
            st.session_state.messages.append({"role": "assistant", "content": response, "time": datetime.now().strftime("%H:%M")})
            st.rerun()

# --- ROUTER ---
if st.session_state.view == "onboarding":
    show_onboarding()
elif st.session_state.view == "modules":
    show_modules()
elif st.session_state.view == "chat":
    show_chat()