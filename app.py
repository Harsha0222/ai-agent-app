import streamlit as st
from agent import run_agent

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------

st.set_page_config(
    page_title="AI Agent",
    page_icon="🤖",
    layout="wide"
)

# ---------------------------------------------------
# CUSTOM CSS
# ---------------------------------------------------

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Poppins', sans-serif;
}

/* Main Background */

.stApp {
    background: linear-gradient(
        135deg,
        #0f172a 0%,
        #1e1b4b 25%,
        #312e81 50%,
        #7c3aed 75%,
        #0f172a 100%
    );
}

/* Hide Streamlit Menu */

#MainMenu {
    visibility:hidden;
}

footer {
    visibility:hidden;
}

/* Hero Section */

.hero-title {
    text-align:center;
    font-size:4rem;
    font-weight:700;

    background: linear-gradient(
        90deg,
        #38bdf8,
        #8b5cf6,
        #ec4899
    );

    -webkit-background-clip:text;
    -webkit-text-fill-color:transparent;

    margin-top:10px;
    margin-bottom:10px;
}

.hero-subtitle {
    text-align:center;
    color:white;
    opacity:0.9;
    font-size:1.2rem;
    margin-bottom:30px;
}

/* Sidebar */

section[data-testid="stSidebar"] {

    background: rgba(255,255,255,0.08);

    backdrop-filter: blur(20px);

    border-right:1px solid rgba(255,255,255,0.1);
}

/* Chat Bubbles */

.stChatMessage {

    background: rgba(255,255,255,0.08);

    backdrop-filter: blur(20px);

    border-radius:20px;

    border:1px solid rgba(255,255,255,0.1);

    padding:15px;

    margin-bottom:15px;
}

/* Cards */

.metric-card {

    background: rgba(255,255,255,0.08);

    border-radius:20px;

    padding:20px;

    text-align:center;

    backdrop-filter: blur(20px);

    border:1px solid rgba(255,255,255,0.1);

    color:white;
}

/* Input Box */

.stChatInputContainer {

    background: rgba(255,255,255,0.08);

    backdrop-filter: blur(15px);

    border-radius:20px;
}

/* Buttons */

.stButton > button {

    background: linear-gradient(
        90deg,
        #3b82f6,
        #8b5cf6
    );

    color:white;

    border:none;

    border-radius:12px;

    font-weight:600;

    padding:10px 20px;
}

/* Expander */

.streamlit-expanderHeader {

    background: rgba(255,255,255,0.08);

    border-radius:12px;
}

/* Metrics */

[data-testid="metric-container"] {

    background: rgba(255,255,255,0.08);

    border-radius:18px;

    padding:20px;

    backdrop-filter: blur(20px);

    border:1px solid rgba(255,255,255,0.1);
}

/* Scrollbar */

::-webkit-scrollbar {
    width:8px;
}

::-webkit-scrollbar-thumb {
    background:#8b5cf6;
    border-radius:10px;
}

</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# HEADER
# ---------------------------------------------------

st.markdown("""
<div class="hero-title">
🤖 AI AGENT
</div>

<div class="hero-subtitle">
Weather • Stocks • Tool Calling • Powered by Ollama
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# METRICS
# ---------------------------------------------------

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("⚡ Model", "Ollama")

with col2:
    st.metric("🌦 Weather", "Enabled")

with col3:
    st.metric("📈 Stocks", "Enabled")

with col4:
    st.metric("🧠 Agent", "Active")

st.markdown("<br>", unsafe_allow_html=True)

# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------

with st.sidebar:

    st.markdown("# 🚀 AI Agent")

    st.markdown("---")

    st.markdown("### 🛠 Available Tools")

    st.success("🌦 Weather Search")

    st.success("📈 Stock Market")

    st.success("🧠 Agent Reasoning")

    st.success("⚡ Ollama")

    st.markdown("---")

    st.markdown("### 💡 Example Queries")

    st.info("Weather in Hyderabad")

    st.info("Weather in New York")

    st.info("IBM stock price")

    st.info("Tesla stock price")

    st.info("Apple stock price")

    st.markdown("---")

    st.caption("Built with Streamlit + Ollama")

# ---------------------------------------------------
# CHAT HISTORY
# ---------------------------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------------------------------------------------
# DISPLAY HISTORY
# ---------------------------------------------------

for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ---------------------------------------------------
# CHAT INPUT
# ---------------------------------------------------

prompt = st.chat_input(
    "Ask about weather, stocks, or anything..."
)

if prompt:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):

        with st.spinner("🧠 Thinking..."):

            result = run_agent(prompt)

        answer = result["answer"]

        logs = result["logs"]

        st.markdown(answer)

        with st.expander("🧠 Agent Reasoning"):

            for log in logs:
                st.write(log)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )