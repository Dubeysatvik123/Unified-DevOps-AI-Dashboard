import streamlit as st
import subprocess
import os
import json
import psutil
import platform
from pathlib import Path
import requests
import webbrowser

def run():
    """Main function to run the Linux module"""
    
    st.title("🐧 Linux System Management & Analysis")
    st.markdown("Comprehensive Linux system administration and analysis tools")
    
    # Sidebar navigation
    st.sidebar.title("🛠️ Linux Tools")
    
    tool_category = st.sidebar.selectbox(
        "Select Category:",
        ["📊 System Analysis", "🖥️ GUI Analysis", "🎨 Icon Management", "💻 Terminal Enhancement", "📱 Communication", "📝 Documentation"]
    )
    
    if tool_category == "📊 System Analysis":
        show_system_analysis()
    elif tool_category == "🖥️ GUI Analysis":
        show_gui_analysis()
    elif tool_category == "🎨 Icon Management":
        show_icon_management()
    elif tool_category == "💻 Terminal Enhancement":
        show_terminal_enhancement()
    elif tool_category == "📱 Communication":
        show_linux_communication()
    elif tool_category == "📝 Documentation":
        show_linux_documentation()

def show_system_analysis():
    """Show Linux system analysis tools"""
    st.header("📊 Linux System Analysis")
    
    # System Information
    st.subheader("🖥️ System Information")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Basic System Info:**")
        st.write(f"OS: {platform.system()}")
        st.write(f"Release: {platform.release()}")
        st.write(f"Version: {platform.version()}")
        st.write(f"Machine: {platform.machine()}")
        st.write(f"Processor: {platform.processor()}")
    
    with col2:
        st.write("**System Resources:**")
        # CPU Info
        cpu_percent = psutil.cpu_percent(interval=1)
        st.write(f"CPU Usage: {cpu_percent}%")
        
        # Memory Info
        memory = psutil.virtual_memory()
        st.write(f"Memory Usage: {memory.percent}%")
        st.write(f"Available Memory: {memory.available / (1024**3):.2f} GB")
        
        # Disk Info
        disk = psutil.disk_usage('/')
        st.write(f"Disk Usage: {disk.percent}%")
        st.write(f"Free Disk: {disk.free / (1024**3):.2f} GB")
    
    # Process Analysis
    st.subheader("📋 Process Analysis")
    
    if st.button("🔄 Refresh Process List"):
        try:
            processes = []
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
                try:
                    processes.append(proc.info)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass
            
            # Sort by CPU usage
            processes.sort(key=lambda x: x['cpu_percent'], reverse=True)
            
            st.write("**Top 10 Processes by CPU Usage:**")
            for i, proc in enumerate(processes[:10], 1):
                st.write(f"{i}. {proc['name']} (PID: {proc['pid']}) - CPU: {proc['cpu_percent']:.1f}%")
                
        except Exception as e:
            st.error(f"Error getting process list: {str(e)}")
    
    # Network Analysis
    st.subheader("🌐 Network Analysis")
    
    try:
        # Network interfaces
        net_io = psutil.net_io_counters()
        st.write(f"Bytes Sent: {net_io.bytes_sent / (1024**2):.2f} MB")
        st.write(f"Bytes Received: {net_io.bytes_recv / (1024**2):.2f} MB")
        
        # Network connections
        connections = psutil.net_connections()
        st.write(f"Active Connections: {len(connections)}")
        
    except Exception as e:
        st.error(f"Error getting network info: {str(e)}")

def show_gui_analysis():
    """Show GUI program analysis tools"""
    st.header("🖥️ GUI Program Analysis")
    st.markdown("""
    ### Identify Terminal Commands Used by GUI Applications
    
    Select a running GUI application to see the underlying terminal command.
    """)
    # List running GUI apps
    gui_apps = []
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            if proc.info['cmdline'] and (
                'usr/bin' in ' '.join(proc.info['cmdline']) or '/bin/' in ' '.join(proc.info['cmdline'])
            ):
                gui_apps.append(proc.info)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    if gui_apps:
        app_names = [f"{p['name']} (PID: {p['pid']})" for p in gui_apps]
        selected = st.selectbox("Select a running GUI app:", app_names)
        idx = app_names.index(selected)
        st.write(f"**Command:** {' '.join(gui_apps[idx]['cmdline'])}")
    else:
        st.info("No running GUI apps detected.")
    st.markdown("---")
    st.subheader("Manual Command Analysis")
    custom_cmd = st.text_input("Enter a command to analyze:")
    if st.button("Analyze Command") and custom_cmd:
        st.code(f"which {custom_cmd.split()[0]}", language="bash")
        result = subprocess.run(['which', custom_cmd.split()[0]], capture_output=True, text=True)
        if result.returncode == 0:
            st.success(f"Found: {result.stdout.strip()}")
        else:
            st.warning("Not found in PATH.")

def show_icon_management():
    """Show icon and logo management tools"""
    st.header("🎨 Icon & Logo Management")
    
    st.markdown("""
    ### Change the Logo or Icon of Any Program in Linux
    1. Find the .desktop file for the app (usually in /usr/share/applications or ~/.local/share/applications).
    2. Edit the file and change the Icon= line to your new icon path.
    3. Update icon cache: `sudo gtk-update-icon-cache`.
    """)
    app_name = st.text_input("App name to search for .desktop file:")
    if st.button("Find .desktop file") and app_name:
        found = False
        for base in ["/usr/share/applications", os.path.expanduser("~/.local/share/applications")]:
            for root, dirs, files in os.walk(base):
                for file in files:
                    if app_name.lower() in file.lower() and file.endswith('.desktop'):
                        st.success(f"Found: {os.path.join(root, file)}")
                        found = True
        if not found:
            st.warning("No .desktop file found.")
    
    # Find application icons
    st.subheader("🔍 Find Application Icons")
    
    app_name = st.text_input("Enter application name:", placeholder="firefox")
    
    if st.button("🔍 Find Icons"):
        if app_name:
            try:
                found_icons = []
                
                # Search in common locations
                search_paths = [
                    "/usr/share/applications",
                    "/usr/share/icons",
                    "~/.local/share/applications",
                    "~/.local/share/icons"
                ]
                
                for path in search_paths:
                    expanded_path = os.path.expanduser(path)
                    if os.path.exists(expanded_path):
                        for root, dirs, files in os.walk(expanded_path):
                            for file in files:
                                if app_name.lower() in file.lower():
                                    found_icons.append(os.path.join(root, file))
                
                if found_icons:
                    st.success(f"Found {len(found_icons)} icon files:")
                    for icon in found_icons:
                        st.write(f"📁 {icon}")
                else:
                    st.info("No icon files found for this application")
                    
            except Exception as e:
                st.error(f"Error searching for icons: {str(e)}")
        else:
            st.warning("Please enter an application name")
    
    # Icon modification guide
    st.subheader("📝 Icon Modification Guide")
    
    st.markdown("""
    ### How to Modify Application Icons:
    
    1. **Find the current icon:**
       ```bash
       find /usr/share/applications -name "*application*.desktop"
       ```
    
    2. **Edit the desktop file:**
       ```bash
       sudo nano /usr/share/applications/application.desktop
       ```
    
    3. **Change the Icon line:**
       ```
       Icon=/path/to/your/new/icon.png
       ```
    
    4. **Update icon cache:**
       ```bash
       sudo gtk-update-icon-cache
       ```
    """)

def show_terminal_enhancement():
    """Show terminal enhancement tools"""
    st.header("💻 Terminal Enhancement & GUI Interfaces")
    st.markdown("""
    ### Add More Terminals and GUI Interfaces in Linux
    - **tmux**: `sudo apt install tmux` (terminal multiplexer)
    - **screen**: `sudo apt install screen`
    - **byobu**: `sudo apt install byobu`
    - **guake**: `sudo apt install guake` (dropdown terminal)
    - **terminator**: `sudo apt install terminator` (multi-pane GUI terminal)
    - **xterm**: `sudo apt install xterm`
    - **gnome-terminal**: `sudo apt install gnome-terminal`
    """)
    st.code("sudo apt install tmux screen byobu guake terminator xterm gnome-terminal", language="bash")
    
    # Shell customization
    st.subheader("🐚 Shell Customization")
    
    shell_options = ["bash", "zsh", "fish"]
    selected_shell = st.selectbox("Select Shell:", shell_options)
    
    if selected_shell == "bash":
        st.markdown("**Bash customization:**")
        st.code("""
# Install Oh My Bash
bash -c "$(curl -fsSL https://raw.githubusercontent.com/ohmybash/oh-my-bash/master/tools/install.sh)"

# Customize .bashrc
nano ~/.bashrc
        """, language="bash")
    
    elif selected_shell == "zsh":
        st.markdown("**Zsh customization:**")
        st.code("""
# Install Oh My Zsh
sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"

# Install plugins
git clone https://github.com/zsh-users/zsh-autosuggestions ~/.zsh/plugins/zsh-autosuggestions
git clone https://github.com/zsh-users/zsh-syntax-highlighting.git ~/.zsh/plugins/zsh-syntax-highlighting
        """, language="bash")
    
    elif selected_shell == "fish":
        st.markdown("**Fish shell customization:**")
        st.code("""
# Install Oh My Fish
curl -L https://get.oh-my.fish | fish

# Install themes
omf install agnoster
omf theme agnoster
        """, language="bash")

def show_linux_communication():
    """Show Linux communication tools"""
    st.header("📱 Linux Communication Tools")
    
    st.markdown("""
    ### Send Email, WhatsApp, Tweet, and SMS from Linux Terminal
    - **Email**: `echo 'body' | mail -s 'subject' recipient@example.com`
    - **WhatsApp**: Use [yowsup](https://github.com/tgalal/yowsup) or WhatsApp Web automation (selenium, puppeteer)
    - **Tweet**: Use [t](https://github.com/sferik/t) Ruby CLI or [tweepy](https://www.tweepy.org/) in Python
    - **SMS**: Use [Twilio CLI](https://www.twilio.com/docs/twilio-cli/quickstart)
    """)
    st.code("echo 'body' | mail -s 'subject' recipient@example.com", language="bash")
    st.code("twilio api:core:messages:create --to='+1234567890' --from='+0987654321' --body='Hello from terminal!'", language="bash")
    st.code("t update 'Hello from terminal!'", language="bash")
    
    # WhatsApp via terminal
    st.subheader("📱 WhatsApp via Terminal")
    
    st.markdown("""
    ### WhatsApp Web Automation
    
    You can use tools like `whatsapp-web.js` or `selenium` to automate WhatsApp:
    """)
    
    st.code("""
# Install Node.js and whatsapp-web.js
npm install whatsapp-web.js

# Basic script
const { Client } = require('whatsapp-web.js');
const client = new Client();

client.on('ready', () => {
    client.sendMessage('1234567890@c.us', 'Hello from terminal!');
});
    """, language="javascript")
    
    # Twitter via terminal
    st.subheader("🐦 Twitter via Terminal")
    
    st.code("""
# Install tweepy for Python
pip install tweepy

# Basic tweet script
import tweepy
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)
api.update_status("Hello from Linux terminal!")
    """, language="python")
    
    # SMS via terminal
    st.subheader("📱 SMS via Terminal")
    
    st.code("""
# Using Twilio CLI
pip install twilio
twilio api:core:messages:create --to="+1234567890" --from="+0987654321" --body="Hello from terminal!"
    """, language="bash")

def show_linux_documentation():
    """Show Linux documentation and blog tools"""
    st.header("📝 Linux Documentation & Signals")
    st.markdown("""
    ### Ctrl+C and Ctrl+Z Signal Handling
    - **Ctrl+C** sends SIGINT (interrupts process)
    - **Ctrl+Z** sends SIGTSTP (suspends process)
    - Use `trap` in shell scripts to handle signals:
    ```bash
    trap 'echo Interrupted!' INT
    trap 'echo Stopped!' TSTP
    ```
    - Use `jobs`, `fg`, `bg`, `kill` for job control
    """)
    
    # Companies using Linux
    st.subheader("🏢 Companies Using Linux")
    
    companies_data = {
        "Google": {
            "usage": "Android OS, Chrome OS, internal infrastructure",
            "benefits": "Cost savings, customization, security, scalability"
        },
        "Amazon": {
            "usage": "AWS infrastructure, Kindle devices, internal systems",
            "benefits": "Reliability, performance, cost-effectiveness"
        },
        "Facebook/Meta": {
            "usage": "Server infrastructure, data centers, development",
            "benefits": "Open source collaboration, flexibility, performance"
        },
        "Netflix": {
            "usage": "Content delivery, streaming infrastructure",
            "benefits": "Scalability, reliability, cost savings"
        },
        "Tesla": {
            "usage": "Vehicle operating systems, infotainment systems",
            "benefits": "Real-time performance, security, customization"
        }
    }
    
    selected_company = st.selectbox("Select Company:", list(companies_data.keys()))
    
    if selected_company:
        company_info = companies_data[selected_company]
        st.write(f"**{selected_company} Linux Usage:**")
        st.write(f"**Usage:** {company_info['usage']}")
        st.write(f"**Benefits:** {company_info['benefits']}")
    
    # Blog post generator
    st.subheader("📝 Blog Post Generator")
    
    blog_topic = st.selectbox("Select Blog Topic:", [
        "Why Companies Choose Linux",
        "Linux vs Windows in Enterprise",
        "Linux Security Benefits",
        "Linux Cost Savings Analysis"
    ])
    
    if st.button("📝 Generate Blog Outline"):
        if blog_topic == "Why Companies Choose Linux":
            st.markdown("""
            ### Why Companies Choose Linux: A Comprehensive Analysis
            
            **Introduction:**
            - Brief overview of Linux adoption in enterprise
            - Current market trends
            
            **1. Cost Benefits:**
            - No licensing fees
            - Reduced hardware requirements
            - Lower total cost of ownership
            
            **2. Security Advantages:**
            - Open source transparency
            - Rapid security updates
            - Community-driven security
            
            **3. Performance Benefits:**
            - Efficient resource utilization
            - Better scalability
            - Optimized for specific workloads
            
            **4. Customization and Flexibility:**
            - Tailored solutions
            - Vendor independence
            - Integration capabilities
            
            **5. Case Studies:**
            - Google's Linux infrastructure
            - Amazon's AWS platform
            - Netflix's streaming architecture
            
            **Conclusion:**
            - Future of Linux in enterprise
            - Recommendations for adoption
            """)
        
        elif blog_topic == "Linux vs Windows in Enterprise":
            st.markdown("""
            ### Linux vs Windows in Enterprise: A Detailed Comparison
            
            **Introduction:**
            - Overview of both operating systems
            - Enterprise adoption trends
            
            **1. Cost Comparison:**
            - Licensing costs
            - Hardware requirements
            - Maintenance costs
            
            **2. Security Analysis:**
            - Vulnerability statistics
            - Update mechanisms
            - Security features
            
            **3. Performance Metrics:**
            - Resource utilization
            - Scalability
            - Reliability
            
            **4. Management and Administration:**
            - Administrative tools
            - Automation capabilities
            - Learning curve
            
            **5. Use Case Scenarios:**
            - Web servers
            - Database systems
            - Development environments
            
            **Conclusion:**
            - When to choose each OS
            - Hybrid approaches
            """)
    
    # Technical documentation
    st.subheader("🔧 Technical Documentation")
    
    doc_topic = st.selectbox("Select Technical Topic:", [
        "Ctrl+C and Ctrl+Z Signal Handling",
        "Linux Process Management",
        "File System Permissions",
        "Network Configuration"
    ])
    
    if st.button("📋 Generate Technical Doc"):
        if doc_topic == "Ctrl+C and Ctrl+Z Signal Handling":
            st.markdown("""
            ### Linux Signal Handling: Ctrl+C and Ctrl+Z
            
            **Signal Types:**
            - SIGINT (Ctrl+C): Interrupt signal
            - SIGTSTP (Ctrl+Z): Stop signal
            
            **How They Work:**
            1. User presses Ctrl+C/Z
            2. Terminal driver sends signal to foreground process
            3. Process receives signal and handles it
            
            **Default Behavior:**
            - SIGINT: Terminates the process
            - SIGTSTP: Suspends the process
            
            **Custom Signal Handling:**
            ```bash
            # In shell scripts
            trap 'echo "Interrupted!"' INT
            trap 'echo "Stopped!"' TSTP
            ```
            
            **Process States:**
            - Running: Active execution
            - Stopped: Suspended (Ctrl+Z)
            - Terminated: Killed (Ctrl+C)
            
            **Job Control Commands:**
            - `jobs`: List background jobs
            - `fg`: Bring job to foreground
            - `bg`: Continue job in background
            - `kill`: Send signals to processes
            """)