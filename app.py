import streamlit as st
from PIL import Image
import time
import sys
import traceback
import importlib
from modules import project

# ================= Page Configuration =================
st.set_page_config(
    page_title="Unified DevOps + AI Dashboard",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ================= Module Loading System =================
def safe_import_module(module_name, module_path):
    """Safely import a module and return the module object"""
    try:
        module = importlib.import_module(module_path)
        return module
    except Exception as e:
        st.sidebar.error(f"⚠️ Failed to load {module_name}: {str(e)}")
        return None

# Define module mappings
MODULE_MAPPINGS = {
    "dockermenu": "modules.dockermenu", 
    "GENAI": "modules.GENAI",
    "github_automation": "modules.github_automation",
    "iac": "modules.iac",
    "kubernetesmenue": "modules.kubernetesmenue",
    "linux": "modules.linux",
    "ml_regress": "modules.ml_regress",
    "promptengineeing": "modules.promptengineeing",
    "pythonmenu": "modules.pythonmenu",
    "testingagent": "modules.testingagent",
    "project": "modules.project",
    "webdev": "modules.webdev"
}

# Load all modules
loaded_modules = {}
for module_name, module_path in MODULE_MAPPINGS.items():
    module = safe_import_module(module_name, module_path)
    if module:
        loaded_modules[module_name] = module

# ================= Enhanced Modern CSS =================
st.markdown("""
<style>
    /* Modern CSS Variables */
    :root {
        --primary-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        --secondary-gradient: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        --success-gradient: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        --warning-gradient: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
        --danger-gradient: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
        --dark-bg: #0f0f23;
        --card-bg: rgba(255, 255, 255, 0.1);
        --text-primary: #ffffff;
        --text-secondary: #b0b0b0;
        --border-radius: 15px;
        --shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        --transition: all 0.3s ease;
    }
    
    /* Global Styles */
    .main {
        background: var(--dark-bg);
        color: var(--text-primary);
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Enhanced Sidebar */
    .css-1d391kg {
        background: var(--primary-gradient);
        backdrop-filter: blur(10px);
    }
    
    /* Profile Card */
    .profile-card {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(15px);
        border-radius: var(--border-radius);
        padding: 2rem;
        margin-bottom: 2rem;
        border: 1px solid rgba(255, 255, 255, 0.2);
        text-align: center;
        box-shadow: var(--shadow);
    }
    
    .profile-image {
        border-radius: 50%;
        border: 4px solid rgba(255, 255, 255, 0.3);
        margin-bottom: 1rem;
        transition: var(--transition);
    }
    
    .profile-image:hover {
        transform: scale(1.05);
        border-color: rgba(255, 255, 255, 0.6);
    }
    
    /* Hero Section */
    .hero-container {
        background: var(--primary-gradient);
        padding: 4rem 2rem;
        border-radius: var(--border-radius);
        margin-bottom: 3rem;
        text-align: center;
        box-shadow: var(--shadow);
        position: relative;
        overflow: hidden;
    }
    
    .hero-title {
        font-size: 3.5rem;
        font-weight: 800;
        margin-bottom: 1rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
        position: relative;
        z-index: 1;
    }
    
    .hero-subtitle {
        font-size: 1.5rem;
        margin-bottom: 2rem;
        opacity: 0.9;
        position: relative;
        z-index: 1;
    }
    
    .hero-description {
        font-size: 1.2rem;
        max-width: 800px;
        margin: 0 auto 2rem;
        line-height: 1.8;
        position: relative;
        z-index: 1;
    }
    
    /* Feature Cards */
    .feature-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
        gap: 2rem;
        margin: 3rem 0;
    }
    
    .feature-card {
        background: var(--card-bg);
        backdrop-filter: blur(15px);
        border-radius: var(--border-radius);
        padding: 2.5rem;
        box-shadow: var(--shadow);
        border: 1px solid rgba(255, 255, 255, 0.1);
        transition: var(--transition);
        position: relative;
        overflow: hidden;
    }
    
    .feature-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: var(--primary-gradient);
    }
    
    .feature-card:hover {
        transform: translateY(-10px);
        box-shadow: 0 15px 40px rgba(0, 0, 0, 0.4);
        border-color: rgba(255, 255, 255, 0.3);
    }
    
    .feature-icon {
        font-size: 3rem;
        margin-bottom: 1.5rem;
        display: block;
    }
    
    .feature-title {
        font-size: 1.5rem;
        font-weight: 700;
        margin-bottom: 1rem;
        color: var(--text-primary);
    }
    
    .feature-description {
        color: var(--text-secondary);
        line-height: 1.6;
        font-size: 1rem;
    }
    
    /* Statistics Cards */
    .stats-container {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 1.5rem;
        margin: 3rem 0;
    }
    
    .stat-card {
        background: var(--card-bg);
        backdrop-filter: blur(15px);
        padding: 2rem;
        border-radius: var(--border-radius);
        text-align: center;
        box-shadow: var(--shadow);
        border: 1px solid rgba(255, 255, 255, 0.1);
        transition: var(--transition);
    }
    
    .stat-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4);
    }
    
    .stat-number {
        font-size: 2.5rem;
        font-weight: 800;
        margin-bottom: 0.5rem;
        background: var(--primary-gradient);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .stat-label {
        font-size: 1rem;
        color: var(--text-secondary);
        font-weight: 500;
    }
    
    /* Status Indicators */
    .status-indicator {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.75rem 1.5rem;
        border-radius: 25px;
        font-size: 0.9rem;
        font-weight: 600;
        margin: 0.5rem 0;
    }
    
    .status-online {
        background: rgba(46, 204, 113, 0.2);
        color: #27ae60;
        border: 2px solid rgba(46, 204, 113, 0.4);
    }
    
    .status-dot {
        width: 10px;
        height: 10px;
        border-radius: 50%;
        background: currentColor;
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0% { opacity: 1; transform: scale(1); }
        50% { opacity: 0.5; transform: scale(1.2); }
        100% { opacity: 1; transform: scale(1); }
    }
    
    /* Animations */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .animate-fade-in {
        animation: fadeInUp 0.8s ease-out;
    }
    
    /* Navigation Menu */
    .nav-menu {
        background: var(--card-bg);
        backdrop-filter: blur(15px);
        border-radius: var(--border-radius);
        padding: 1.5rem;
        margin: 1rem 0;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .nav-item {
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 10px;
        transition: var(--transition);
        cursor: pointer;
        border: 1px solid transparent;
    }
    
    .nav-item:hover {
        background: rgba(255, 255, 255, 0.1);
        border-color: rgba(255, 255, 255, 0.2);
    }
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .hero-title {
            font-size: 2.5rem;
        }
        
        .feature-grid {
            grid-template-columns: 1fr;
        }
        
        .stats-container {
            grid-template-columns: repeat(2, 1fr);
        }
    }
    
    /* Custom Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: var(--primary-gradient);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: var(--secondary-gradient);
    }
</style>
""", unsafe_allow_html=True)

# ================= Enhanced Sidebar =================
with st.sidebar:
    st.markdown("""
    <div class="profile-card animate-fade-in">
        <img src="https://github.com/Dubeysatvik123/Images/blob/main/Satvik.jpg?raw=true" 
             class="profile-image" width="120" alt="Profile">
        <h3 style="color: white; margin: 0.5rem 0; font-weight: 600;">Satvik Dubey</h3>
        <p style="color: rgba(255,255,255,0.8); margin: 0.5rem 0; font-size: 0.9rem;">Team No: 73</p>
        <div class="status-indicator status-online">
            <div class="status-dot"></div>
            System Online
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Enhanced navigation with categories
    st.markdown("### 🎯 Navigation")
    
    # Main Categories
    categories = {
        "🏠 Home": "home",
        "🤖 AI & Machine Learning": "ai_ml",

        "📈 ML Regression": "ml_regress", 
        "🛠️ DevOps & Infrastructure": "devops",
        "🐳 Docker Automation": "dockermenu",
        "☸️ Kubernetes Automation": "kubernetesmenue",
        "🔁 AIOps": "aiops",
        "🧱 Infrastructure as Code": "iac",
        "💻 Development Tools": "dev_tools",
        "🐧 Linux Tools": "linux",
        "🐍 Python MultiTool": "pythonmenu",
        "🤖 GenAI": "GENAI",
        "🧑‍💻 Agentic AI": "testingagent",
        "✍️ Prompt Engineering": "promptengineeing",
        "🌐 Github Automation": "github_automation",
        "🌐 Web Development": "webdev",
        "📝 Projects": "project"
    }
    
    selected = st.selectbox("Select a Module", list(categories.keys()))
    
    # Module status in sidebar
    st.markdown("---")
    st.markdown("### 📈 Module Status")
    loaded_count = sum(1 for module in loaded_modules.values() if module is not None)
    total_count = len(loaded_modules)
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Loaded", loaded_count, f"/{total_count}")
    with col2:
        percentage = (loaded_count / total_count) * 100 if total_count > 0 else 0
        st.metric("Success", f"{percentage:.0f}%")

# ================= Enhanced Home Page =================
def show_home():
    st.markdown("""
    <div class="hero-container animate-fade-in">
        <div class="hero-title">🚀 Unified DevOps + AI Dashboard</div>
        <div class="hero-subtitle">The Ultimate Productivity Suite for Modern Development</div>
        <div class="hero-description">
            Experience the future of integrated development with our comprehensive platform that seamlessly 
            combines Machine Learning, DevOps automation, and AI tools in one powerful interface. 
            Streamline your workflow from development to deployment with cutting-edge technologies.
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Statistics overview
    st.markdown("""
    <div class="stats-container">
        <div class="stat-card">
            <div class="stat-number">15+</div>
            <div class="stat-label">Integrated Modules</div>
        </div>
        <div class="stat-card">
            <div class="stat-number">100%</div>
            <div class="stat-label">Python Powered</div>
        </div>
        <div class="stat-card">
            <div class="stat-number">24/7</div>
            <div class="stat-label">Availability</div>
        </div>
        <div class="stat-card">
            <div class="stat-number">∞</div>
            <div class="stat-label">Possibilities</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Feature highlights
    st.markdown("## ✨ Key Features")
    
    features = [
        {
            "icon": "🧠",
            "title": "Machine Learning Suite",
            "description": "Advanced ML models including ANN, Linear Regression, and Classification algorithms with interactive dashboards and real-time analytics."
        },
        {
            "icon": "🐳",
            "title": "Container Orchestration",
            "description": "Automated Docker and Kubernetes management with deployment pipelines, monitoring capabilities, and AI-powered optimization."
        },
        {
            "icon": "☁️",
            "title": "Cloud Integration",
            "description": "Seamless AWS automation with Infrastructure as Code (IaC) for scalable cloud deployments and cost optimization."
        },
        {
            "icon": "🤖",
            "title": "AI-Powered Tools",
            "description": "GenAI capabilities, Agentic AI systems, and advanced prompt engineering for intelligent automation and decision making."
        },
        {
            "icon": "💻",
            "title": "Development Toolkit",
            "description": "Comprehensive Python tools, Linux utilities, and automated testing frameworks for enhanced developer productivity."
        },
        {
            "icon": "📊",
            "title": "Real-time Analytics",
            "description": "Live dashboards and monitoring systems with AIOps integration for proactive issue resolution and performance optimization."
        }
    ]
    
    # Create feature cards grid
    cols = st.columns(2)
    for i, feature in enumerate(features):
        with cols[i % 2]:
            st.markdown(f"""
            <div class="feature-card">
                <div class="feature-icon">{feature['icon']}</div>
                <div class="feature-title">{feature['title']}</div>
                <div class="feature-description">{feature['description']}</div>
            </div>
            """, unsafe_allow_html=True)
    
    # Getting started section
    st.markdown("---")
    st.markdown("## 🚀 Getting Started")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="nav-menu">
            <h4>🎯 Step 1: Choose a Module</h4>
            <p>Select from our comprehensive suite of tools in the sidebar navigation menu</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="nav-menu">
            <h4>🔧 Step 2: Explore Features</h4>
            <p>Discover interactive tools and advanced capabilities tailored for your needs</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="nav-menu">
            <h4>⚡ Step 3: Leverage Power</h4>
            <p>Utilize integrated capabilities to accelerate your development workflow</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; padding: 3rem; color: var(--text-secondary);">
        <p style="font-size: 1.1rem; margin-bottom: 1rem;">🌟 Built with ❤️ by <strong>Satvik Dubey</strong> (Team 73)</p>
        <p style="font-style: italic; font-size: 1rem; margin: 0;">"Empowering innovation through integrated technology solutions"</p>
    </div>
    """, unsafe_allow_html=True)

# ================= Enhanced Routing =================
def show_loading():
    with st.spinner("🔄 Loading module..."):
        time.sleep(0.5)

def run_module_safely(module_name):
    """Safely run a module with error handling"""
    if module_name in loaded_modules:
        try:
            module = loaded_modules[module_name]
            if hasattr(module, 'run'):
                module.run()
            else:
                st.error(f"Module {module_name} does not have a 'run' function")
        except Exception as e:
            st.error(f"Error running {module_name}: {str(e)}")
            st.code(traceback.format_exc())
    else:
        st.error(f"Module {module_name} not found or failed to load")

# Route handling with categories
category = categories.get(selected, "home")

if category == "home":
    show_home()
elif category == "ai_ml":
    st.title("🤖 AI & Machine Learning Hub")
    st.info("Select a specific ML module from the sidebar to continue.")
    ml_modules = [
        {"name": "📈 ML Regression", "desc": "Advanced regression analysis with data visualization"}
    ]
    for module in ml_modules:
        st.markdown(f"**{module['name']}**: {module['desc']}")

elif category == "ml_regress":
    show_loading()
    run_module_safely("ml_regress")
elif category == "devops":
    st.title("🛠️ DevOps & Infrastructure Hub")
    st.info("Select a specific DevOps tool from the sidebar to continue.")
elif category == "dockermenu":
    show_loading()
    run_module_safely("dockermenu")
elif category == "kubernetesmenue":
    show_loading()
    run_module_safely("kubernetesmenue")
elif category == "aiops":
    show_loading()
    run_module_safely("testingagent")
elif category == "iac":
    show_loading()
    run_module_safely("iac")
elif category == "dev_tools":
    st.title("💻 Development Tools Hub")
    st.info("Select a specific development tool from the sidebar to continue.")
elif category == "linux":
    show_loading()
    run_module_safely("linux")
elif category == "pythonmenu":
    show_loading()
    run_module_safely("pythonmenu")
elif category == "GENAI":
    show_loading()
    run_module_safely("GENAI")
elif category == "testingagent":
    show_loading()
    run_module_safely("testingagent")
elif category == "promptengineeing":
    show_loading()
    run_module_safely("promptengineeing")
elif category == "github_automation":
    show_loading()
    run_module_safely("github_automation")
elif category == "webdev":
    show_loading()
    run_module_safely("webdev")
elif category == "project":
    show_loading()
    project.run()

def show_webdev_tools():
    st.header("🌐 Web Development & JavaScript Tools")
    st.markdown("Comprehensive web development tools with JavaScript functionality")
    
    tool_category = st.selectbox(
        "Select Category:",
        ["📷 Media Capture", "🎤 Speech & Audio", "🤖 AI Integration", "📱 Social Media", "🔍 Search & Scraping"]
    )
    
    if tool_category == "📷 Media Capture":
        st.subheader("📷 Media Capture Tools")
        st.code("""
async function accessCamera() {
    const stream = await navigator.mediaDevices.getUserMedia({ video: true });
    document.getElementById('video').srcObject = stream;
}
function takePhoto() {
    const video = document.getElementById('video');
    const canvas = document.getElementById('canvas');
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    canvas.getContext('2d').drawImage(video, 0, 0);
    return canvas.toDataURL('image/png');
}
        """, language="javascript")
    
    elif tool_category == "🎤 Speech & Audio":
        st.subheader("🎤 Speech Recognition")
        st.code("""
function startSpeechRecognition() {
    if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        const recognition = new SpeechRecognition();
        
        recognition.continuous = true;
        recognition.interimResults = true;
        recognition.lang = 'en-US';
        
        recognition.onresult = (event) => {
            let finalTranscript = '';
            for (let i = event.resultIndex; i < event.results.length; i++) {
                const transcript = event.results[i][0].transcript;
                if (event.results[i].isFinal) {
                    finalTranscript += transcript;
                }
            }
            document.getElementById('finalTranscript').textContent = finalTranscript;
        };
        
        recognition.start();
    }
}
        """, language="javascript")
    
    elif tool_category == "🤖 AI Integration":
        st.subheader("🤖 ChatGPT Integration")
        st.code("""
async function sendToChatGPT(prompt, apiKey) {
    try {
        const response = await fetch('https://api.openai.com/v1/chat/completions', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${apiKey}`
            },
            body: JSON.stringify({
                model: 'gpt-3.5-turbo',
                messages: [{ role: 'user', content: prompt }],
                max_tokens: 1000
            })
        });
        
        const data = await response.json();
        return data.choices[0].message.content;
    } catch (error) {
        console.error('Error calling ChatGPT:', error);
        return 'Error: Unable to get response from ChatGPT';
    }
}
        """, language="javascript")
    
    elif tool_category == "📱 Social Media":
        st.subheader("📱 Social Media Integration")
        st.code("""
function shareToWhatsApp(message, phoneNumber) {
    const whatsappUrl = `https://wa.me/${phoneNumber}?text=${encodeURIComponent(message)}`;
    window.open(whatsappUrl, '_blank');
}

function shareToInstagram(imageUrl, caption) {
    const instagramUrl = `instagram://library?AssetPath=${encodeURIComponent(imageUrl)}&InstagramCaption=${encodeURIComponent(caption)}`;
    window.location.href = instagramUrl;
}
        """, language="javascript")
    
    elif tool_category == "🔍 Search & Scraping":
        st.subheader("🔍 Google Search Integration")
        st.code("""
async function searchGoogle(query, apiKey, searchEngineId) {
    try {
        const response = await fetch(`https://www.googleapis.com/customsearch/v1?key=${apiKey}&cx=${searchEngineId}&q=${encodeURIComponent(query)}`);
        const data = await response.json();
        return data.items || [];
    } catch (error) {
        console.error('Error searching Google:', error);
        return [];
    }
}
        """, language="javascript")
