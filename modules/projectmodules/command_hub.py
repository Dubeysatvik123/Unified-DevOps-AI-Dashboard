import streamlit as st
import subprocess
import os
import pandas as pd
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

def command_hub_page():
    if 'command_history' not in st.session_state:
        st.session_state.command_history = []
    st.header("⚡ CommandHub - System Command Center")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Command Execution")
        command_input = st.text_input("Enter Command", placeholder="e.g., ping google.com")
        timeout = st.number_input("Timeout (seconds)", min_value=1, max_value=300, value=30)
        if st.button("🚀 Execute Command"):
            if command_input:
                with st.spinner("Executing command..."):
                    result = run_command(command_input, timeout=timeout)
                    if result['success']:
                        st.code(result['stdout'], language="bash")
                        if 'command_history' not in st.session_state:
                            st.session_state.command_history = []
                        st.session_state.command_history.append({
                            'command': command_input,
                            'timestamp': datetime.now().isoformat(),
                            'success': True,
                            'output': result['stdout']
                        })
                    else:
                        st.error(f"Error: {result['stderr']}")
                        st.session_state.command_history.append({
                            'command': command_input,
                            'timestamp': datetime.now().isoformat(),
                            'success': False,
                            'output': result['stderr']
                        })
        
        st.write("**Quick Commands:**")
        quick_commands = {
            "📁 List Files": "ls -la" if os.name != 'nt' else "dir",
            "💾 Disk Usage": "df -h" if os.name != 'nt' else "wmic logicaldisk get size,freespace,caption",
            "🔄 Processes": "ps aux" if os.name != 'nt' else "tasklist /FO CSV",
            "🌐 Network Config": "ifconfig" if os.name != 'nt' else "ipconfig /all",
            "📊 Memory Info": "free -m" if os.name != 'nt' else "systeminfo | findstr Memory",
            "⏰ System Uptime": "uptime" if os.name != 'nt' else "systeminfo | findstr Time"
        }
        
        for label, cmd in quick_commands.items():
            if st.button(label):
                with st.spinner(f"Executing {label}..."):
                    result = run_command(cmd)
                    if result['success']:
                        st.code(result['stdout'], language="bash")
                        if 'command_history' not in st.session_state:
                            st.session_state.command_history = []
                        st.session_state.command_history.append({
                            'command': cmd,
                            'timestamp': datetime.now().isoformat(),
                            'success': True,
                            'output': result['stdout']
                        })
                    else:
                        st.error(f"Error: {result['stderr']}")
                        st.session_state.command_history.append({
                            'command': cmd,
                            'timestamp': datetime.now().isoformat(),
                            'success': False,
                            'output': result['stderr']
                        })
    
    with col2:
        st.subheader("Command History")
        if st.session_state.command_history:
            df = pd.DataFrame(st.session_state.command_history)
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No commands executed yet.")
        if st.button("🗑️ Clear History"):
            st.session_state.command_history = []
            st.rerun()