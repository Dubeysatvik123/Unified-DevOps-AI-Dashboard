import streamlit as st
import requests
import subprocess
import os
from datetime import datetime

def run_command(command, timeout=30, shell=True):
    try:
        result = subprocess.run(
            command,
            shell=shell,
            capture_output=True,
            text=True,
            timeout=timeout
        )
        return {
            "success": result.returncode == 0,
            "stdout": result.stdout,
            "stderr": result.stderr
        }
    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "stdout": "",
            "stderr": "Timeout expired"
        }
    except Exception as e:
        return {
            "success": False,
            "stdout": "",
            "stderr": str(e)
        }

def is_port_open(host, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        result = sock.connect_ex((host, port))
        sock.close()
        return result == 0
    except:
        return False

def get_system_metrics():
    try:
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        return {
            'CPU Usage': f"{cpu_percent:.1f}%",
            'Memory Usage': f"{memory.percent:.1f}%",
            'Disk Usage': f"{(disk.used/disk.total)*100:.1f}%",
            'Available Memory': f"{memory.available / (1024**3):.1f} GB"
        }
    except Exception as e:
        return {'Error': str(e)}

def call_openai_api(prompt, api_key):
    try:
        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }
        data = {
            'model': 'gpt-3.5-turbo',
            'messages': [{'role': 'user', 'content': prompt}],
            'max_tokens': 150
        }
        response = requests.post(
            'https://api.openai.com/v1/chat/completions',
            headers=headers,
            json=data,
            timeout=30
        )
        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content']
        else:
            return f"API Error: {response.status_code} - {response.text}"
    except Exception as e:
        return f"Error calling OpenAI API: {str(e)}"

def chatgpt_automation_page():
    st.header("🤖 ChatGPT Automation Agent")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        api_key = st.text_input("OpenAI API Key", type="password", help="Enter your OpenAI API key")
        
        if 'chat_history' not in st.session_state:
            st.session_state.chat_history = []
        
        st.subheader("Chat Interface")
        chat_container = st.container()
        with chat_container:
            for message in st.session_state.chat_history:
                with st.chat_message(message["role"]):
                    st.write(message["content"])
        
        if prompt := st.chat_input("Enter your message..."):
            st.session_state.chat_history.append({"role": "user", "content": prompt})
            if api_key:
                response = call_openai_api(prompt, api_key)
            else:
                response = "Please provide your OpenAI API key to enable AI responses."
            st.session_state.chat_history.append({"role": "assistant", "content": response})
            st.rerun()
    
    with col2:
        st.subheader("Automation Tools")
        
        with st.expander("🧮 Calculator"):
            calc_expression = st.text_input("Enter expression (e.g., 2+2*3):")
            if st.button("Calculate") and calc_expression:
                try:
                    allowed_chars = set('0123456789+-*/.() ')
                    if all(c in allowed_chars for c in calc_expression):
                        result = eval(calc_expression)
                        st.success(f"Result: {result}")
                        st.session_state.chat_history.append({
                            "role": "assistant",
                            "content": f"Calculation: {calc_expression} = {result}"
                        })
                    else:
                        st.error("Invalid characters in expression")
                except Exception as e:
                    st.error(f"Error: {str(e)}")
        
        with st.expander("⚡ Quick Commands"):
            if st.button("📅 Current Date/Time"):
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                st.info(f"Current time: {current_time}")
                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": f"Current date and time: {current_time}"
                })
            
            if st.button("💾 System Info"):
                info = get_system_metrics()
                st.json(info)
                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": f"System metrics retrieved: {info}"
                })
        
        with st.expander("📁 File Operations"):
            if st.button("📂 List Current Directory"):
                result = run_command("ls -la" if os.name != 'nt' else "dir")
                if result['success']:
                    st.code(result['stdout'])
                else:
                    st.error(result['stderr'])
        
        if st.button("🗑️ Clear Chat"):
            st.session_state.chat_history = []
            st.rerun()