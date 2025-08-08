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

def clone_flask_repo(repo_url, clone_dir):
    try:
        if os.path.exists(clone_dir):
            run_command(f"rm -rf {clone_dir}")
        result = run_command(f"git clone {repo_url} {clone_dir}")
        return result['success']
    except Exception as e:
        st.error(f"Error cloning repository: {str(e)}")
        return False

def flask_cicd_page():
    if 'jenkins_jobs' not in st.session_state:
        st.session_state.jenkins_jobs = []
    st.header("🌐 Flask Web App CI/CD")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Repository Configuration")
        repo_url = st.text_input("Git Repository URL", value="git@github.com:Dubeysatvik123/CICD_Flask.git")
        clone_dir = st.text_input("Clone Directory", value="./flask_app")
        if st.button("📥 Clone Repository"):
            with st.spinner("Cloning repository..."):
                if clone_flask_repo(repo_url, clone_dir):
                    st.success("✅ Repository cloned successfully!")
                else:
                    st.error("❌ Failed to clone repository")
    
    with col2:
        st.subheader("Jenkins Configuration")
        jenkins_url = st.text_input("Jenkins URL", value="http://localhost:8080")
        if st.button("🔐 Test Jenkins Connection"):
            if jenkins_url:
                result = run_command(f"curl -s -o /dev/null -w %{{http_code}} {jenkins_url}/api/json")
                if result['stdout'] == '200':
                    st.success("✅ Jenkins connection successful!")
                else:
                    st.error("❌ Jenkins connection failed!")
            else:
                st.error("Please provide Jenkins URL")
    
    st.subheader("Deployment Operations")
    
    if os.path.exists(clone_dir):
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("🚀 Trigger Jenkins Build"):
                if jenkins_url:
                    with st.spinner("Triggering Jenkins build..."):
                        result = run_command(f"curl -X POST {jenkins_url}/job/flask-app-build/build")
                        if result['success']:
                            st.success("✅ Build triggered!")
                            if 'jenkins_jobs' not in st.session_state:
                                st.session_state.jenkins_jobs = []
                            st.session_state.jenkins_jobs.append({
                                'job': 'flask-app-build',
                                'timestamp': datetime.now().isoformat(),
                                'status': 'TRIGGERED'
                            })
                        else:
                            st.error(f"❌ Failed to trigger build: {result['stderr']}")
                else:
                    st.error("Please provide Jenkins URL")
        
        with col2:
            if st.button("🏗️ Build Docker Image"):
                with st.spinner("Building Docker image..."):
                    result = run_command(f"cd {clone_dir} && docker build -t flask-app:latest .")
                    if result['success']:
                        st.success("✅ Docker image built successfully!")
                    else:
                        st.error(f"❌ Failed to build Docker image: {result['stderr']}")
        
        with col3:
            if st.button("▶️ Run Flask App"):
                with st.spinner("Running Flask app..."):
                    run_command("docker stop flask-app-container")
                    run_command("docker rm flask-app-container")
                    result = run_command(
                        f"docker run -d --name flask-app-container -p 5000:5000 flask-app:latest"
                    )
                    if result['success']:
                        st.success("✅ Flask app is running on http://localhost:5000")
                    else:
                        st.error(f"❌ Failed to run Flask app: {result['stderr']}")
    
    if st.session_state.jenkins_jobs:
        st.subheader("Build History")
        df = pd.DataFrame(st.session_state.jenkins_jobs)
        st.dataframe(df, use_container_width=True)