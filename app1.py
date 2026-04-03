import streamlit as st
from datetime import datetime

import requests
from groq import Groq

# ===== API KEYS (YOU WILL ADD KEYS HERE) =====
NEWS_API_KEY = "991cdd72a29b43aa85b6644138c670b5"
GROQ_API_KEY = "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"
client = Groq(api_key=GROQ_API_KEY)

def fetch_news(category):
    url = f"https://newsapi.org/v2/top-headlines?category={category.lower()}&country=in&pageSize=5&apiKey={NEWS_API_KEY}"
    
    try:
        response = requests.get(url, timeout=5)
        data = response.json()

        if data.get("status") != "ok":
            return [], data.get("message")

        articles = data.get("articles", [])
        return articles, None

    except Exception as e:
        return [], str(e)

def get_response(query, category):
    st.write("DEBUG: calling OpenAI...")
    articles, error = fetch_news(category)

# If news API fails → still allow general AI chat
    news_text = ""
    if articles:
        news_text = "\n".join(
            [f"{i+1}. {a['title']} - {a['description']}" for i, a in enumerate(articles)]
        )

    prompt = f"""
    Answer briefly and clearly.

    User: {query}
    Category: {category}

    News:
    {news_text}
    """

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",   # 🔥 super powerful & free
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        return response.choices[0].message.content

    except Exception as e:
        return f"⚠️ AI Error: {str(e)}"

# Page config
st.set_page_config(
    page_title="NewsGenie",
    page_icon="🗞️",
    layout="wide",
    initial_sidebar_state="expanded"
)

import streamlit.components.v1 as components

components.html("""
<!DOCTYPE html>
<html>
<head>
<style>
body {
    margin: 0;
    overflow: hidden;
}

/* FULL SCREEN BACKGROUND */
#particles-js {
    position: fixed;
    width: 100vw;
    height: 100vh;
    top: 0;
    left: 0;
    background: #020617;
    z-index: -1;
}
</style>
</head>

<body>
<div id="particles-js"></div>

<script src="https://cdn.jsdelivr.net/particles.js/2.0.0/particles.min.js"></script>

<script>
particlesJS("particles-js", {
  "particles": {
    "number": { "value": 100 },
    "color": { "value": "#00ffff" },
    "shape": { "type": "circle" },
    "opacity": { "value": 0.5 },
    "size": { "value": 3 },
    "move": { "enable": true, "speed": 1.5 }
  }
});
</script>
</body>
</html>
""", height=0)   # 🔥 VERY IMPORTANT

st.markdown("""
<style>

/* 🔥 Make iframe act like background */
iframe {
    position: fixed !important;
    top: 0;
    left: 0;
    width: 100vw !important;
    height: 100vh !important;
    z-index: -1 !important;
    pointer-events: none;
}

/* 🔥 Keep app above */
section.main {
    position: relative;
    z-index: 1;
}

</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>

section.main > div {
    background: rgba(0,0,0,0.7);
    backdrop-filter: blur(20px);
    border-radius: 20px;
    padding: 20px;
}

</style>
""", unsafe_allow_html=True)


st.markdown("""
<style>

/* 🌌 Full background */
html, body, [class*="css"] {
    background: transparent !important;
    color: white !important;
}

/* 🔥 Main app container */
section.main > div {
    background: rgba(0, 0, 0, 0.7);
    backdrop-filter: blur(20px);
    border-radius: 20px;
    padding: 20px;
}

/* 💬 Chat bubbles */
.user-bubble {
    background: linear-gradient(135deg, #3b82f6, #2563eb);
    padding: 12px;
    border-radius: 15px;
    margin: 10px 0;
    text-align: right;
    color: white;
}

.bot-bubble {
    background: rgba(30,41,59,0.9);
    padding: 12px;
    border-radius: 15px;
    margin: 10px 0;
    color: white;
}

</style>
""", unsafe_allow_html=True)


custom_css = """
<style>
    * { margin: 0; padding: 0; box-sizing: border-box; }

    .main {
        background: linear-gradient(135deg, #0f0f1a 0%, #1a1a2e 100%);
        min-height: 100vh;
    }
    [data-testid="stSidebar"] {
        background: linear-gradient(135deg, #16213e 0%, #0f3460 100%);
        border-right: 1px solid rgba(79, 172, 254, 0.2);
    }
    [data-testid="stSidebar"] [data-testid="stVerticalBlock"] { gap: 1.5rem; }
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #0f0f1a 0%, #1a1a2e 100%);
    }

    /* SCROLLBAR */
    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(180deg, #4facfe 0%, #00f2fe 100%);
        border-radius: 3px; transition: background 0.2s;
    }
    ::-webkit-scrollbar-thumb:hover { background: rgba(0,212,255,0.7); }
    [data-testid="stChatMessageContainer"], .main .block-container {
        scrollbar-width: thin; scrollbar-color: rgba(0,212,255,0.4) transparent;
    }

    /* TITLE */
    .title-container {
        text-align: center; margin-bottom: 2rem;
        animation: pageIntro 0.6s cubic-bezier(0.16,1,0.3,1) both;
    }
    .title-container h1 {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        background-clip: text; font-size: 2.5rem; margin-bottom: 0.5rem;
        animation: neonGlow 3s ease-in-out infinite, titleDrop 0.7s cubic-bezier(0.34,1.56,0.64,1) both;
        will-change: text-shadow;
    }
    .subtitle { color: rgba(255,255,255,0.6); font-size: 1rem; }

    /* CHAT */
    .chat-container {
        display: flex; flex-direction: column;
        height: calc(100vh - 200px); gap: 1rem;
        padding: 1.5rem; overflow-y: auto;
    }
    .message-wrapper { will-change: transform, opacity; }
    .user-message {
        display: flex; justify-content: flex-end; margin-bottom: 1rem;
        animation: slideInRight 0.4s cubic-bezier(0.16,1,0.3,1) both;
    }
    .assistant-message {
        display: flex; justify-content: flex-start; margin-bottom: 1rem;
        animation: slideInLeft 0.4s cubic-bezier(0.16,1,0.3,1) both;
    }
    .message-bubble {
        max-width: 70%; padding: 1rem 1.25rem;
        border-radius: 12px; word-wrap: break-word; position: relative;
    }
    .user-message .message-bubble {
        background: linear-gradient(135deg, #4facfe 0%, #845ef7 100%);
        color: white; box-shadow: 0 8px 32px rgba(79,172,254,0.3);
    }
    .assistant-message .message-bubble {
        background: rgba(255,255,255,0.05); color: rgba(255,255,255,0.9);
        border: 1px solid rgba(79,172,254,0.2); backdrop-filter: blur(10px);
        border-left: 3px solid #4facfe;
        box-shadow: 0 8px 32px rgba(0,0,0,0.3), inset 0 0 20px rgba(79,172,254,0.1);
    }
    .message-time { font-size: 0.75rem; color: rgba(255,255,255,0.4); margin-top: 0.5rem; }

    /* TYPING */
    .typing-indicator { display: flex; align-items: center; gap: 6px; padding: 1rem 1.25rem; }
    .typing-dot {
        width: 10px; height: 10px; border-radius: 50%; background: #00d4ff;
        animation: typingBounce 1.4s ease-in-out infinite;
        box-shadow: 0 0 8px rgba(0,212,255,0.6); will-change: transform, opacity;
    }
    .typing-dot:nth-child(2) { animation-delay: 0.2s; }
    .typing-dot:nth-child(3) { animation-delay: 0.4s; }
    .typing-text { color: rgba(255,255,255,0.6); font-size: 0.9rem; margin-left: 0.5rem; }

    /* INPUT */
    .stTextInput > div > div > input {
        background: rgba(255,255,255,0.05) !important;
        border: 2px solid rgba(79,172,254,0.3) !important;
        color: black !important; border-radius: 8px !important;
        padding: 0.75rem 1rem !important; font-size: 0.95rem !important;
        transition: all 0.3s ease !important;
        animation: borderGlow 2s ease-in-out infinite; will-change: box-shadow;
    }
    .stTextInput > div > div > input:focus {
        border: 2px solid #4facfe !important;
        box-shadow: 0 0 20px rgba(79,172,254,0.5) !important;
        background: rgba(255,255,255,0.08) !important;
    }

    /* BUTTONS */
    .stButton > button {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%) !important;
        color: white !important; border: none !important;
        padding: 0.75rem 1.5rem !important; border-radius: 8px !important;
        font-weight: 600 !important; transition: all 0.3s ease !important;
        box-shadow: 0 8px 24px rgba(79,172,254,0.3) !important;
        cursor: pointer !important; position: relative; overflow: hidden; will-change: transform;
    }
    .stButton > button:hover {
        transform: scale(1.05) !important;
        box-shadow: 0 12px 32px rgba(79,172,254,0.5) !important;
    }
    .stButton > button:active { transform: scale(0.98) !important; }
    .stButton > button::after {
        content: ''; position: absolute; top: 50%; left: 50%;
        width: 0; height: 0; border-radius: 50%;
        background: rgba(255,255,255,0.3);
        transform: translate(-50%,-50%);
        transition: width 0.4s ease, height 0.4s ease, opacity 0.4s ease; opacity: 0;
    }
    .stButton > button:active::after { width: 200px; height: 200px; opacity: 0; }
    .clear-chat-btn > button {
        background: linear-gradient(135deg, #ff6b6b 0%, #ee5a52 100%) !important;
        box-shadow: 0 8px 24px rgba(255,107,107,0.3) !important;
    }
    .clear-chat-btn > button:hover {
        box-shadow: 0 12px 32px rgba(255,107,107,0.5) !important;
        animation: shake 0.4s ease;
    }

    /* RADIO */
    .stSelectbox > div > div > select, .stRadio > div > label { color: white !important; }
    .stSelectbox > div > div {
        background: rgba(255,255,255,0.05) !important;
        border: 1px solid rgba(79,172,254,0.3) !important; border-radius: 6px !important;
    }
    .stRadio > div { display: flex; flex-direction: column; gap: 0.75rem; }
    .stRadio > div > label {
        padding: 0.75rem 1rem !important;
        background: rgba(79,172,254,0.1) !important;
        border: 1px solid rgba(79,172,254,0.3) !important;
        border-radius: 6px !important; transition: all 0.3s ease !important;
        cursor: pointer !important; position: relative;
    }
    .stRadio > div > label:hover {
        background: rgba(79,172,254,0.2) !important;
        border-color: #4facfe !important;
        box-shadow: 0 0 12px rgba(79,172,254,0.3) !important;
    }
    [data-testid="stSidebar"] .stRadio > div > label::after {
        content: ''; position: absolute; bottom: 0; left: 0;
        width: 100%; height: 2px;
        background: linear-gradient(90deg, #4287f5, #00d4ff);
        transform: scaleX(0); transform-origin: left; transition: transform 0.3s ease;
    }
    [data-testid="stSidebar"] .stRadio > div > label:hover::after { transform: scaleX(1); }

    /* SIDEBAR SLIDE-IN */
    [data-testid="stSidebar"] [data-testid="stMarkdown"],
    [data-testid="stSidebar"] .stRadio > div > label {
        animation: sideSlideIn 0.5s cubic-bezier(0.16,1,0.3,1) both; will-change: transform, opacity;
    }
    [data-testid="stSidebar"] [data-testid="stMarkdown"]:nth-child(1) { animation-delay: 0.05s; }
    [data-testid="stSidebar"] [data-testid="stMarkdown"]:nth-child(2) { animation-delay: 0.10s; }
    [data-testid="stSidebar"] [data-testid="stMarkdown"]:nth-child(3) { animation-delay: 0.15s; }
    [data-testid="stSidebar"] .stRadio > div > label:nth-child(1) { animation-delay: 0.05s; }
    [data-testid="stSidebar"] .stRadio > div > label:nth-child(2) { animation-delay: 0.10s; }
    [data-testid="stSidebar"] .stRadio > div > label:nth-child(3) { animation-delay: 0.15s; }
    [data-testid="stSidebar"] .stRadio > div > label:nth-child(4) { animation-delay: 0.20s; }
    [data-testid="stSidebar"] .stRadio > div > label:nth-child(5) { animation-delay: 0.25s; }

    /* ABOUT */
    .about-section {
        margin-top: 2rem; padding: 1rem;
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(79,172,254,0.2);
        border-radius: 8px; backdrop-filter: blur(10px);
    }
    .about-section h3 { color: #4facfe; margin-bottom: 0.5rem; font-size: 0.95rem; }
    .about-section p  { color: rgba(255,255,255,0.6); font-size: 0.85rem; line-height: 1.5; }

    /* SKELETON */
    .skeleton-loader {
        height: 16px; margin: 8px 0; border-radius: 4px;
        background: linear-gradient(90deg,
            rgba(255,255,255,0.04) 25%, rgba(255,255,255,0.1) 50%, rgba(255,255,255,0.04) 75%);
        background-size: 200% 100%; animation: shimmer 1.5s infinite;
    }

    /* ORBS */
    .gradient-orb { position: fixed; border-radius: 50%; filter: blur(80px); pointer-events: none; z-index: 0; will-change: transform; }
    .orb-1 { width:400px; height:400px; top:10%; left:15%; background:radial-gradient(circle,rgba(30,60,180,0.22),transparent 70%); animation:orbFloat1 12s ease-in-out infinite; }
    .orb-2 { width:350px; height:350px; bottom:20%; right:10%; background:radial-gradient(circle,rgba(130,40,200,0.18),transparent 70%); animation:orbFloat2 15s ease-in-out infinite; }
    .orb-3 { width:300px; height:300px; top:50%; left:50%; background:radial-gradient(circle,rgba(0,200,220,0.15),transparent 70%); animation:orbFloat3 18s ease-in-out infinite; }

    /* PARTICLE CANVAS */
    #particle-canvas { position:fixed; top:0; left:0; width:100%; height:100%; z-index:0; pointer-events:none; }

    /* TEXT OVERRIDES */
    h1,h2,h3,h4,h5,h6 { color: white !important; }
    body, p { color: rgba(255,255,255,0.9) !important; }
    label { color: rgba(255,255,255,0.8) !important; }

    /* KEYFRAMES */
    @keyframes neonGlow {
        0%,100% { text-shadow:0 0 10px rgba(66,135,245,0.8),0 0 20px rgba(66,135,245,0.4),0 0 40px rgba(66,135,245,0.2); }
        33%      { text-shadow:0 0 10px rgba(0,212,255,0.8),0 0 20px rgba(0,212,255,0.4),0 0 40px rgba(0,212,255,0.2); }
        66%      { text-shadow:0 0 10px rgba(160,80,255,0.8),0 0 20px rgba(160,80,255,0.4),0 0 40px rgba(160,80,255,0.2); }
    }
    @keyframes titleDrop {
        from { opacity:0; transform:translateY(-30px); }
        to   { opacity:1; transform:translateY(0); }
    }
    @keyframes pageIntro {
        from { opacity:0; transform:scale(0.97); }
        to   { opacity:1; transform:scale(1); }
    }
    @keyframes slideInLeft {
        from { opacity:0; transform:translateX(-30px) translateY(10px); }
        to   { opacity:1; transform:translateX(0) translateY(0); }
    }
    @keyframes slideInRight {
        from { opacity:0; transform:translateX(30px) translateY(10px); }
        to   { opacity:1; transform:translateX(0) translateY(0); }
    }
    @keyframes sideSlideIn {
        from { opacity:0; transform:translateX(-20px); }
        to   { opacity:1; transform:translateX(0); }
    }
    @keyframes typingBounce {
        0%,60%,100% { transform:translateY(0); opacity:0.4; }
        30%          { transform:translateY(-12px); opacity:1; }
    }
    @keyframes borderGlow {
        0%,100% { box-shadow:0 0 5px rgba(66,135,245,0.5),inset 0 0 3px rgba(66,135,245,0.1); border-color:rgba(66,135,245,0.6); }
        50%      { box-shadow:0 0 10px rgba(0,212,255,0.6),inset 0 0 5px rgba(0,212,255,0.15); border-color:rgba(0,212,255,0.7); }
    }
    @keyframes shake {
        0%,100% { transform:translateX(0) scale(1.05); }
        20%     { transform:translateX(-4px) scale(1.05); }
        40%     { transform:translateX(4px) scale(1.05); }
        60%     { transform:translateX(-3px) scale(1.05); }
        80%     { transform:translateX(3px) scale(1.05); }
    }
    @keyframes shimmer {
        0%   { background-position:200% 0; }
        100% { background-position:-200% 0; }
    }
    @keyframes orbFloat1 {
        0%,100% { transform:translate(0,0) scale(1); }
        33%      { transform:translate(60px,-40px) scale(1.08); }
        66%      { transform:translate(-30px,50px) scale(0.95); }
    }
    @keyframes orbFloat2 {
        0%,100% { transform:translate(0,0) scale(1); }
        33%      { transform:translate(-50px,30px) scale(1.05); }
        66%      { transform:translate(40px,-60px) scale(0.92); }
    }
    @keyframes orbFloat3 {
        0%,100% { transform:translate(0,0) scale(1); }
        50%      { transform:translate(70px,40px) scale(1.1); }
    }
    @keyframes fadeIn { from{opacity:0;} to{opacity:1;} }
    @keyframes bounce {
        0%,80%,100% { transform:translateY(0); }
        40%          { transform:translateY(-10px); }
    }
</style>
"""

st.markdown(custom_css, unsafe_allow_html=True)

# Animated background (orbs + particle canvas)
st.markdown("""
<style>
#particle-canvas {
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    z-index: -1;
    background: transparent;
}
</style>
<div class="gradient-orb orb-1"></div>
<div class="gradient-orb orb-2"></div>
<div class="gradient-orb orb-3"></div>
<canvas id="particle-canvas"></canvas>
<script>
(function(){
    if(window._particlesInit) return;
    window._particlesInit = true;
    const canvas = document.getElementById('particle-canvas');
    if(!canvas) return;
    const ctx = canvas.getContext('2d');
    let w, h, particles=[], mouseX=0, mouseY=0;
    function resize(){ w=canvas.width=window.innerWidth; h=canvas.height=window.innerHeight; }
    resize();
    window.addEventListener('resize', resize);
    document.addEventListener('mousemove', e=>{ mouseX=e.clientX; mouseY=e.clientY; });
    class Particle {
        constructor(){ this.reset(); }
        reset(){
            this.x=Math.random()*w; this.y=Math.random()*h;
            this.vx=(Math.random()-0.5)*0.5; this.vy=(Math.random()-0.5)*0.5;
            this.r=Math.random()*2+1; this.alpha=Math.random()*0.5+0.2;
        }
        update(){
            const dx=mouseX-this.x, dy=mouseY-this.y;
            const dist=Math.sqrt(dx*dx+dy*dy);
            if(dist<200){ this.x-=dx*0.002; this.y-=dy*0.002; }
            this.x+=this.vx; this.y+=this.vy;
            if(this.x<0||this.x>w) this.vx*=-1;
            if(this.y<0||this.y>h) this.vy*=-1;
        }
        draw(){
            ctx.beginPath(); ctx.arc(this.x,this.y,this.r,0,Math.PI*2);
            ctx.fillStyle=`rgba(0,180,255,${this.alpha})`;
            ctx.shadowBlur=8; ctx.shadowColor='rgba(0,200,255,0.5)'; ctx.fill();
        }
    }
    for(let i=0;i<60;i++) particles.push(new Particle());
    function animate(){
        ctx.clearRect(0,0,w,h); ctx.shadowBlur=0;
        for(let i=0;i<particles.length;i++){
            particles[i].update(); particles[i].draw();
            for(let j=i+1;j<particles.length;j++){
                const dx=particles[i].x-particles[j].x, dy=particles[i].y-particles[j].y;
                const d=Math.sqrt(dx*dx+dy*dy);
                if(d<120){
                    ctx.beginPath();
                    ctx.moveTo(particles[i].x,particles[i].y);
                    ctx.lineTo(particles[j].x,particles[j].y);
                    ctx.strokeStyle=`rgba(0,180,255,${0.15*(1-d/120)})`;
                    ctx.lineWidth=0.5; ctx.stroke();
                }
            }
        }
        requestAnimationFrame(animate);
    }
    animate();
})();
</script>
""", unsafe_allow_html=True)

# Session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "selected_category" not in st.session_state:
    st.session_state.selected_category = "General"
if "is_loading" not in st.session_state:
    st.session_state.is_loading = False

# Sidebar
with st.sidebar:
    st.markdown("### 📰 Category Selection")
    categories = ["General","Business","Technology","Sports","Entertainment","Health","Science"]
    st.session_state.selected_category = st.radio("Select a news category:", categories, label_visibility="collapsed")
    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🗑️ Clear Chat", key="clear_btn", use_container_width=True):
            st.session_state.messages = []
            st.rerun()
    st.markdown("---")
    st.markdown("""
    <div class="about-section">
        <h3>ℹ️ About NewsGenie</h3>
        <p>Your AI-powered news assistant, bringing you the latest news and insights tailored to your interests.</p>
    </div>
    """, unsafe_allow_html=True)

# Main
col1, col2, col3 = st.columns([1,2,1])
with col2:
    st.markdown("""
    <div class="title-container">
        <h1>NewsGenie 🗞️</h1>
        <p class="subtitle">Your AI-powered news assistant</p>
    </div>
    """, unsafe_allow_html=True)

# Chat display
chat_placeholder = st.container()
with chat_placeholder:
    if len(st.session_state.messages) == 0:
        st.markdown("""
        <div style="text-align:center;padding:3rem 1rem;color:rgba(255,255,255,0.5);animation:fadeIn 0.8s ease-in;">
            <p style="font-size:1.1rem;">👋 Welcome to NewsGenie!</p>
            <p>Start by asking me anything about the latest news in your selected category.</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        for i, message in enumerate(st.session_state.messages):
            delay = f"animation-delay:{i*0.05}s;"
            if message["role"] == "user":
                st.markdown(f"""
                <div class="message-wrapper" style="{delay}">
                    <div class="user-message">
                        <div class="message-bubble">
                            {message["content"]}
                            <div class="message-time">{message.get('timestamp','')}</div>
                        </div>
                    </div>
                </div>""", unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="message-wrapper" style="{delay}">
                    <div class="assistant-message">
                        <div class="message-bubble">
                            {message["content"]}
                            <div class="message-time">{message.get('timestamp','')}</div>
                        </div>
                    </div>
                </div>""", unsafe_allow_html=True)
                
def send_message():
    user_input = st.session_state.user_input

    if user_input.strip():
        timestamp = datetime.now().strftime("%H:%M")

        st.session_state.messages.append({
            "role": "user",
            "content": user_input,
            "timestamp": timestamp
        })

        # clear input BEFORE rerun
        st.session_state.user_input = ""
        st.session_state.is_loading = True
# Input
st.markdown("---")
col1, col2 = st.columns([5,1])

with col1:
    st.text_input(
        "Ask me anything...",
        key="user_input",
        placeholder="Type your question here...",
        disabled=st.session_state.is_loading,
        label_visibility="collapsed"
    )

with col2:
    st.button(
        "Send 🚀",
        key="send_btn",
        use_container_width=True,
        disabled=st.session_state.is_loading,
        on_click=send_message   # 🔥 THIS FIXES EVERYTHING
    )


if st.session_state.is_loading:
    user_query = st.session_state.messages[-1]["content"]
    selected_category = st.session_state.selected_category

    response = get_response(user_query, selected_category)

    timestamp = datetime.now().strftime("%H:%M")

    st.session_state.messages.append({
        "role": "assistant",
        "content": response,
        "timestamp": timestamp
    })

    st.session_state.is_loading = False
    st.rerun()
    
    
