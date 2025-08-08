import streamlit as st
import subprocess
import os
import tempfile
import pandas as pd

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

def check_docker_available():
    result = run_command("docker version")
    return result['success']

def build_and_run_apache_container(container_name, host_port, html_content):
    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            dockerfile_content = """
FROM httpd:2.4-alpine
COPY index.html /usr/local/apache2/htdocs/
EXPOSE 80
            """
            with open(os.path.join(temp_dir, 'Dockerfile'), 'w') as f:
                f.write(dockerfile_content)
            with open(os.path.join(temp_dir, 'index.html'), 'w') as f:
                f.write(html_content)
            build_result = run_command(f"docker build -t apache-custom {temp_dir}")
            if not build_result['success']:
                return False
            run_command(f"docker stop {container_name}")
            run_command(f"docker rm {container_name}")
            run_result = run_command(
                f"docker run -d --name {container_name} -p {host_port}:80 apache-custom"
            )
            return run_result['success']
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return False

def get_running_containers():
    result = run_command("docker ps --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}\t{{.Image}}'")
    if result['success'] and result['stdout']:
        lines = result['stdout'].split('\n')[1:]
        containers = []
        for line in lines:
            if line.strip():
                parts = line.split('\t')
                if len(parts) >= 4:
                    containers.append({
                        'Name': parts[0],
                        'Status': parts[1],
                        'Ports': parts[2],
                        'Image': parts[3]
                    })
        return containers
    return []

def docker_apache_page():
    st.header("🐳 Docker Apache Container Management")
    
    docker_available = check_docker_available()
    if not docker_available:
        st.error("❌ Docker is not available or not running. Please install and start Docker.")
        return
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Apache Container Management")
        container_name = st.text_input("Container Name", value="apache-server")
        host_port = st.number_input("Host Port", min_value=1024, max_value=65535, value=8080)
        html_content = st.text_area("Custom HTML Content",
                                   value="<h1>Hello from Apache in Docker!</h1><p>Container managed by Streamlit</p>")
        if st.button("🏗️ Build & Run Apache Container"):
            with st.spinner("Building and starting Apache container..."):
                success = build_and_run_apache_container(container_name, host_port, html_content)
                if success:
                    st.success(f"✅ Apache container '{container_name}' is running on port {host_port}")
                    st.info(f"Access your website at: http://localhost:{host_port}")
                else:
                    st.error("❌ Failed to start Apache container")
        
        col_stop, col_remove = st.columns(2)
        with col_stop:
            if st.button("⏹️ Stop Container"):
                result = run_command(f"docker stop {container_name}")
                if result['success']:
                    st.success(f"✅ Container '{container_name}' stopped")
                else:
                    st.error(f"❌ Failed to stop container: {result['stderr']}")
        with col_remove:
            if st.button("🗑️ Remove Container"):
                result = run_command(f"docker rm -f {container_name}")
                if result['success']:
                    st.success(f"✅ Container '{container_name}' removed")
                else:
                    st.error(f"❌ Failed to remove container: {result['stderr']}")
    
    with col2:
        st.subheader("Container Status")
        if st.button("🔄 Refresh Container Status"):
            containers = get_running_containers()
            if containers:
                st.dataframe(pd.DataFrame(containers), use_container_width=True)
            else:
                st.info("No running containers found")
        if st.button("📋 View Container Logs"):
            result = run_command(f"docker logs {container_name} --tail 20")
            if result['success']:
                st.code(result['stdout'], language="bash")
            else:
                st.error(f"Error getting logs: {result['stderr']}")