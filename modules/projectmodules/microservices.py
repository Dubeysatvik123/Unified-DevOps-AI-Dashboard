import streamlit as st
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

def clone_microservices_repo(repo_url, clone_dir):
    try:
        if os.path.exists(clone_dir):
            run_command(f"rm -rf {clone_dir}")
        result = run_command(f"git clone {repo_url} {clone_dir}")
        return result['success']
    except Exception as e:
        st.error(f"Error cloning repository: {str(e)}")
        return False

def microservices_page():
    st.header("🏛️ Containerized Microservices Architecture")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Repository Configuration")
        repo_url = st.text_input("Git Repository URL", value="git@github.com:Dubeysatvik123/Three_Tier_Microservice.git")
        clone_dir = st.text_input("Clone Directory", value="./microservices")
        if st.button("📥 Clone Repository"):
            with st.spinner("Cloning repository..."):
                if clone_microservices_repo(repo_url, clone_dir):
                    st.success("✅ Repository cloned successfully!")
                else:
                    st.error("❌ Failed to clone repository")
    
    with col2:
        st.subheader("Docker Compose Operations")
        if os.path.exists(clone_dir):
            if st.button("🚀 Start Microservices"):
                with st.spinner("Starting microservices with Docker Compose..."):
                    result = run_command(f"cd {clone_dir} && docker-compose up -d")
                    if result['success']:
                        st.success("✅ Microservices started!")
                    else:
                        st.error(f"❌ Failed to start microservices: {result['stderr']}")
            
            if st.button("⏹️ Stop Microservices"):
                with st.spinner("Stopping microservices..."):
                    result = run_command(f"cd {clone_dir} && docker-compose down")
                    if result['success']:
                        st.success("✅ Microservices stopped!")
                    else:
                        st.error(f"❌ Failed to stop microservices: {result['stderr']}")
        
        if st.button("🔄 Container Status"):
            containers = run_command("docker ps --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}\t{{.Image}}'")
            if containers['success']:
                lines = containers['stdout'].split('\n')[1:]
                container_list = []
                for line in lines:
                    if line.strip():
                        parts = line.split('\t')
                        if len(parts) >= 4:
                            container_list.append({
                                'Name': parts[0],
                                'Status': parts[1],
                                'Ports': parts[2],
                                'Image': parts[3]
                            })
                if container_list:
                    st.dataframe(pd.DataFrame(container_list), use_container_width=True)
                else:
                    st.info("No running containers found")
            else:
                st.error(f"Error getting container status: {containers['stderr']}")
    
    with st.expander("📄 Sample docker-compose.yml"):
        compose_content = '''
version: '3.8'
services:
  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    depends_on:
      - backend
  backend:
    build: ./backend
    ports:
      - "5000:5000"
    depends_on:
      - database
  database:
    image: mysql:8.0
    environment:
      MYSQL_ROOT_PASSWORD: example
    volumes:
      - db_data:/var/lib/mysql
volumes:
  db_data:
        '''
        st.code(compose_content, language="yaml")