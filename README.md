# **🚀 SkillNexa AI – Principal Tech Oracle**

🎓 SkillNexa AI is an advanced Streamlit-based Generative AI mentoring platform that simulates interactions with a Principal-level Software Engineer across multiple technical domains such as Python, SQL, MLOps, Generative AI, Deep Learning, and Agentic AI.

It leverages Google Gemini (via LangChain) to deliver context-aware, mentor-style responses in a futuristic, highly interactive UI.

## **🔥 Key Highlights**

  🧠 LLM-Powered Mentorship (Google Gemini)

  🧩 Multi-Domain Modules (Python, SQL, ML, GenAI, Agentic AI)

  🎨 Custom “Midnight Precision” UI System

  💬 Human-like Mentor Conversations

  ⚡ Fast & Lightweight Streamlit App

  🔐 Environment-based API Key Management

## **🧱 Tech Stack**

| Layer         | Technology                   |
| ------------- | ---------------------------- |
| Frontend      | Streamlit + Custom CSS       |
| LLM           | Google Gemini 2.5 Flash      |
| Framework     | LangChain                    |
| Backend Logic | Python                       |
| Environment   | python-dotenv                |
| UI Design     | Glassmorphism + HUD-style UI |

## **🧠 Core Modules Available**

 - 🐍 Python Mastery

 - 🗄️ Database Architect (SQL)

 - ⛓️ MLOps Systems

 - 🪄 Generative AI

 - 🕸️ Deep Learning

 - 🛰️ Agentic AI (Autonomous Agents)

Each module behaves like a dedicated senior mentor with domain-specific expertise.

## **🗂️ Project Structure**

    SkillNexa-AI/
    │
    ├── app.py                  # Main Streamlit application
    ├── .env                    # Environment variables (API key)
    ├── requirements.txt        # Dependencies
    ├── README.md               # Project documentation
    └── assets/                 # (Optional) Images / icons

## **⚙️ Installation & Setup**
1️⃣ Clone the Repository
    
    git clone https://github.com/your-username/SkillNexa-AI.git
    cd SkillNexa-AI
    
2️⃣ Create Virtual Environment

    python -m venv venv
    source venv/bin/activate        # Linux / Mac
    venv\Scripts\activate           # Windows
    
3️⃣ Install Dependencies

    pip install -r requirements.txt

4️⃣ Add Environment Variables

Create a .env file:

    Gemini=YOUR_GOOGLE_GEMINI_API_KEY

▶️ Run the Application

    streamlit run app.py

## **🎨 UI & UX Features**

 - 🌌 Dark futuristic theme

 - 🧊 Glassmorphism cards

 - 🎯 Module filtering (Core / AI / Data)

 - 💡 Smooth transitions & hover effects

 - 📡 Real-time mentor chat experience

## **How It Works (Architecture)**

 - User selects a technical module

 - System initializes a domain-specific system prompt

 - User query + chat history is sent to Gemini via LangChain

 - Response is rendered as a mentor-style explanation

 - Session state maintains context per module

## **🔐 Security & Best Practices**

 - API keys stored in .env

 - .env excluded from GitHub

 - Stateless LLM calls

 - Clean session management

## **🚀 Future Enhancements**

✅ User authentication

✅ Chat history export

✅ Voice interaction

✅ Resume-aware mentoring

✅ Deployment on Streamlit Cloud / AWS

## **👨‍💻 Author**

**Raj Shivade**
🎓 Data Scientist | GenAI | Agentic AI


**GitHub:** [https://github.com/](https://github.com/RajShivade)

**LinkedIn:** www.linkedin.com/in/raj-shivade25 

**⭐ If You Like This Project**

Give it a ⭐ on GitHub — it really helps and motivates future improvements!
