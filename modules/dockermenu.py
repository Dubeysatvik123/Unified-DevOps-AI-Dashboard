import streamlit as st
from typing import List, Dict, Any, Optional
import subprocess
import pandas as pd
import json
import time
import requests
import os

def run_docker_command(command: str) -> tuple[bool, str]:
    """Execute Docker command and return success status and output"""
    try:
        result = subprocess.run(command.split(), capture_output=True, text=True, timeout=30)
        return result.returncode == 0, result.stdout + result.stderr
    except subprocess.TimeoutExpired:
        return False, "Command timed out"
    except Exception as e:
        return False, str(e)

def get_containers() -> List[Dict[str, Any]]:
    """Get list of Docker containers"""
    try:
        result = subprocess.run(['docker', 'ps', '-a', '--format', 'json'], 
                              capture_output=True, text=True)
        containers = []
        for line in result.stdout.strip().split('\n'):
            if line:
                try:
                    containers.append(json.loads(line))
                except:
                    pass
        return containers
    except:
        return []
    
def get_images() -> List[Dict[str, Any]]:
    """Get list of Docker images"""
    try:
        result = subprocess.run(['docker', 'images', '--format', 'json'], 
                              capture_output=True, text=True)
        images = []
        for line in result.stdout.strip().split('\n'):
            if line:
                try:
                    images.append(json.loads(line))
                except:
                    pass
        return images
    except:
        return []

def get_volumes() -> List[Dict[str, Any]]:
    """Get list of Docker volumes"""
    try:
        result = subprocess.run(['docker', 'volume', 'ls', '--format', 'json'], 
                              capture_output=True, text=True)
        volumes = []
        for line in result.stdout.strip().split('\n'):
            if line:
                try:
                    volumes.append(json.loads(line))
                except:
                    pass
        return volumes
    except:
        return []

def get_networks() -> List[Dict[str, Any]]:
    """Get list of Docker networks"""
    try:
        result = subprocess.run(['docker', 'network', 'ls', '--format', 'json'], 
                              capture_output=True, text=True)
        networks = []
        for line in result.stdout.strip().split('\n'):
            if line:
                try:
                    networks.append(json.loads(line))
                except:
                    pass
        return networks
    except:
        return []

def show_docker_advanced():
    st.header("⚙️ Advanced Docker Tasks")
    st.markdown("Run advanced Docker operations with one click:")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Run systemd/systemctl in Docker"):
            success, output = run_docker_command(
                "docker run --privileged -v /sys/fs/cgroup:/sys/fs/cgroup:ro -d centos/systemd"
            )
            if success:
                st.success("✅ systemd container started!")
            else:
                st.error(f"❌ Error: {output}")

        if st.button("Run GUI Apps in Docker"):
            success, output = run_docker_command(
                "docker run -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix jess/firefox"
            )
            if success:
                st.success("✅ GUI app container started!")
            else:
                st.error(f"❌ Error: {output}")

        if st.button("Sound Card Access in Docker"):
            success, output = run_docker_command(
                "docker run --device /dev/snd -e PULSE_SERVER=unix:${XDG_RUNTIME_DIR}/pulse/native -v ${XDG_RUNTIME_DIR}/pulse/native:${XDG_RUNTIME_DIR}/pulse/native centos"
            )
            if success:
                st.success("✅ Sound card access enabled in container!")
            else:
                st.error(f"❌ Error: {output}")

        if st.button("Docker-in-Docker (DIND)"):
            success, output = run_docker_command(
                "docker run --privileged -d docker:dind"
            )
            if success:
                st.success("✅ Docker-in-Docker started!")
            else:
                st.error(f"❌ Error: {output}")

    with col2:
        if st.button("Run Apache in Docker"):
            success, output = run_docker_command(
                "docker run -d -p 8080:80 httpd:2.4"
            )
            if success:
                st.success("✅ Apache container started!")
            else:
                st.error(f"❌ Error: {output}")

        if st.button("Run Any Tool/Tech in Docker"):
            success, output = run_docker_command(
                "docker run -it python:3.10"
            )
            if success:
                st.success("✅ Python container started!")
            else:
                st.error(f"❌ Error: {output}")

        if st.button("Run Regression/Flask/Menu-based Python in Docker"):
            success, output = run_docker_command(
                "docker run -d python:3.10 python main.py"
            )
            if success:
                st.success("✅ Regression/Flask/Menu-based Python app started!")
            else:
                st.error(f"❌ Error: {output}")

        if st.button("Run Firefox in Docker (with GUI)"):
            success, output = run_docker_command(
                "docker run -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix jess/firefox"
            )
            if success:
                st.success("✅ Firefox container started!")
            else:
                st.error(f"❌ Error: {output}")

def show_volume_management():
    """Show volume management page"""
    st.header("💾 Volume Management")
    
    # Volume operations
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📂 Create Volume")
        volume_name = st.text_input("Volume Name:", placeholder="my-volume")
        volume_driver = st.selectbox("Driver:", ["local", "nfs", "other"])
        
        if st.button("➕ Create Volume"):
            if volume_name:
                command = f"docker volume create"
                if volume_driver != "local":
                    command += f" --driver {volume_driver}"
                command += f" {volume_name}"
                
                success, output = run_docker_command(command)
                if success:
                    st.code(dockerfile_content, language='dockerfile')
            
            st.download_button(
                label="💾 Download Dockerfile",
                data=dockerfile_content,
                file_name="Dockerfile",
                mime="text/plain"
            )
        else:
            st.warning("⚠️ Please describe your application")

def show_ai_assistant():
    """Show AI assistant page"""
    st.header("🤖 AI Assistant")
    
    st.markdown("### 🧠 Natural Language to Docker Commands")
    
    user_request = st.text_area(
        "Describe your Docker task:",
        placeholder="Start a nginx container on port 80, or list all running containers...",
        height=100
    )
    
    if st.button("🤖 Generate Command"):
        if user_request:
            # Simple pattern matching
            request_lower = user_request.lower()
            
            if "list" in request_lower and "container" in request_lower:
                command = "docker ps -a"
            elif "start" in request_lower and "container" in request_lower:
                command = "docker start"
            elif "stop" in request_lower and "container" in request_lower:
                command = "docker stop"
            elif "remove" in request_lower and "container" in request_lower:
                command = "docker rm"
            elif "list" in request_lower and "image" in request_lower:
                command = "docker images"
            elif "build" in request_lower and "image" in request_lower:
                command = "docker build -t"
            elif "pull" in request_lower and "image" in request_lower:
                command = "docker pull"
            elif "volume" in request_lower and "list" in request_lower:
                command = "docker volume ls"
            elif "network" in request_lower and "list" in request_lower:
                command = "docker network ls"
            elif "prune" in request_lower or "cleanup" in request_lower:
                command = "docker system prune"
            elif "logs" in request_lower:
                command = "docker logs"
            elif "stats" in request_lower:
                command = "docker stats"
            else:
                command = "docker ps"
            
            st.code(command, language='bash')
            
            # Execute command option
            if st.button("▶️ Execute Command"):
                success, output = run_docker_command(command)
                if success:
                    st.success("✅ Command executed successfully!")
                    st.text(output)
                else:
                    st.error(f"❌ Error: {output}")
        else:
            st.warning("⚠️ Please describe your Docker task")

def show_system_info():
    """Show system information page"""
    st.header("📊 Docker System Information")
    
    # Docker version and info
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🐳 Docker Version")
        success, output = run_docker_command("docker --version")
        if success:
            st.text(output)
        else:
            st.error(f"❌ Error: {output}")
    
    with col2:
        st.subheader("🔧 Docker Compose Version")
        success, output = run_docker_command("docker-compose --version")
        if success:
            st.text(output)
        else:
            st.info("Docker Compose not installed or not found")
    
    # Docker info
    st.subheader("🐳 Docker System Info")
    success, output = run_docker_command("docker info")
    if success:
        st.text(output)
    else:
        st.error(f"❌ Error: {output}")
    
    # System stats
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📦 Images")
        images = get_images()
        if images:
            df = pd.DataFrame(images)
            st.dataframe(df[['Repository', 'Tag', 'Size']] if 'Repository' in df.columns else df)
        else:
            st.info("No images found")
    
    with col2:
        st.subheader("🌐 Networks")
        networks = get_networks()
        if networks:
            df = pd.DataFrame(networks)
            st.dataframe(df[['Name', 'Driver', 'Scope']] if 'Name' in df.columns else df)
        else:
            st.info("No networks found")
    
    # Container stats
    st.subheader("📊 Container Statistics")
    containers = get_containers()
    if containers:
        df = pd.DataFrame(containers)
        st.dataframe(df[['Names', 'Image', 'Status', 'Ports']] if 'Names' in df.columns else df)
    else:
        st.info("No containers found")

def show_volume_management():
    """Show volume management page"""
    st.header("💾 Volume Management")
    
    # Volume operations
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📂 Create Volume")
        volume_name = st.text_input("Volume Name:", placeholder="my-volume")
        volume_driver = st.selectbox("Driver:", ["local", "nfs", "other"])
        
        if st.button("➕ Create Volume"):
            if volume_name:
                command = f"docker volume create"
                if volume_driver != "local":
                    command += f" --driver {volume_driver}"
                command += f" {volume_name}"
                
                success, output = run_docker_command(command)
                if success:
                    st.success("✅ Volume created successfully!")
                else:
                    st.error(f"❌ Error: {output}")
            else:
                st.warning("⚠️ Please enter a volume name")
    
    with col2:
        st.subheader("🗑️ Remove Volume")
        volumes = get_volumes()
        if volumes:
            volume_names = [v.get('Name', 'Unknown') for v in volumes]
            selected_volume = st.selectbox("Select Volume:", volume_names)
            
            if st.button("🗑️ Remove Volume"):
                success, output = run_docker_command(f"docker volume rm {selected_volume}")
                if success:
                    st.success("✅ Volume removed!")
                else:
                    st.error(f"❌ Error: {output}")
        else:
            st.info("No volumes found")
    
    # Volume list
    st.subheader("📋 Volume List")
    volumes = get_volumes()
    if volumes:
        df = pd.DataFrame(volumes)
        st.dataframe(df)
    else:
        st.info("No volumes found")
    
    # Volume inspection
    st.subheader("🔍 Volume Inspection")
    if volumes:
        volume_names = [v.get('Name', 'Unknown') for v in volumes]
        inspect_volume = st.selectbox("Select Volume to Inspect:", volume_names, key="inspect_volume")
        
        if st.button("🔍 Inspect Volume"):
            success, output = run_docker_command(f"docker volume inspect {inspect_volume}")
            if success:
                try:
                    volume_info = json.loads(output)
                    st.json(volume_info)
                except:
                    st.text(output)
            else:
                st.error(f"❌ Error: {output}")

def show_network_management():
    """Show network management page"""
    st.header("🌐 Network Management")
    
    # Network operations
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📡 Create Network")
        network_name = st.text_input("Network Name:", placeholder="my-network")
        network_driver = st.selectbox("Driver:", ["bridge", "host", "overlay", "macvlan", "none"])
        subnet = st.text_input("Subnet (optional):", placeholder="172.20.0.0/16")
        
        if st.button("➕ Create Network"):
            if network_name:
                command = f"docker network create --driver {network_driver}"
                if subnet:
                    command += f" --subnet {subnet}"
                command += f" {network_name}"
                
                success, output = run_docker_command(command)
                if success:
                    st.success("✅ Network created successfully!")
                else:
                    st.error(f"❌ Error: {output}")
            else:
                st.warning("⚠️ Please enter a network name")
    
    with col2:
        st.subheader("🗑️ Remove Network")
        networks = get_networks()
        if networks:
            network_names = [n.get('Name', 'Unknown') for n in networks if n.get('Name') not in ['bridge', 'host', 'none']]
            if network_names:
                selected_network = st.selectbox("Select Network:", network_names)
                
                if st.button("🗑️ Remove Network"):
                    success, output = run_docker_command(f"docker network rm {selected_network}")
                    if success:
                        st.success("✅ Network removed!")
                    else:
                        st.error(f"❌ Error: {output}")
            else:
                st.info("No removable networks found")
        else:
            st.info("No networks found")
    
    # Network list
    st.subheader("📋 Network List")
    networks = get_networks()
    if networks:
        df = pd.DataFrame(networks)
        st.dataframe(df)
    else:
        st.info("No networks found")

def show_maintenance_cleanup():
    """Show maintenance and cleanup page"""
    st.header("🧹 Maintenance & Cleanup")
    
    # System cleanup
    st.subheader("🗑️ System Cleanup")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### 🐳 Container Cleanup")
        if st.button("🧹 Remove Stopped Containers"):
            success, output = run_docker_command("docker container prune -f")
            if success:
                st.success("✅ Stopped containers removed!")
                st.text(output)
            else:
                st.error(f"❌ Error: {output}")
    
    with col2:
        st.markdown("### 🖼️ Image Cleanup")
        if st.button("🧹 Remove Unused Images"):
            success, output = run_docker_command("docker image prune -f")
            if success:
                st.success("✅ Unused images removed!")
                st.text(output)
            else:
                st.error(f"❌ Error: {output}")
        
        if st.button("🧹 Remove All Unused Images"):
            success, output = run_docker_command("docker image prune -a -f")
            if success:
                st.success("✅ All unused images removed!")
                st.text(output)
            else:
                st.error(f"❌ Error: {output}")
    
    with col3:
        st.markdown("### 💾 Volume Cleanup")
        if st.button("🧹 Remove Unused Volumes"):
            success, output = run_docker_command("docker volume prune -f")
            if success:
                st.success("✅ Unused volumes removed!")
                st.text(output)
            else:
                st.error(f"❌ Error: {output}")
    
    # Network cleanup
    st.subheader("🌐 Network Cleanup")
    if st.button("🧹 Remove Unused Networks"):
        success, output = run_docker_command("docker network prune -f")
        if success:
            st.success("✅ Unused networks removed!")
            st.text(output)
        else:
            st.error(f"❌ Error: {output}")
    
    # Complete system cleanup
    st.subheader("⚠️ Complete System Cleanup")
    st.warning("⚠️ This will remove all unused containers, networks, images, and volumes!")
    if st.button("🧹 System Prune (Complete Cleanup)", type="secondary"):
        success, output = run_docker_command("docker system prune -a -f --volumes")
        if success:
            st.success("✅ Complete system cleanup completed!")
            st.text(output)
        else:
            st.error(f"❌ Error: {output}")
    
    # Disk usage
    st.subheader("📊 Disk Usage")
    if st.button("📊 Show Docker Disk Usage"):
        success, output = run_docker_command("docker system df")
        if success:
            st.text(output)
        else:
            st.error(f"❌ Error: {output}")

def show_logs_monitoring():
    """Show logs and monitoring page"""
    st.header("📊 Logs & Monitoring")
    
    # Container logs
    st.subheader("📜 Container Logs")
    containers = get_containers()
    if containers:
        container_names = [c.get('Names', 'Unknown') for c in containers]
        selected_container = st.selectbox("Select Container for Logs:", container_names)
        
        col1, col2 = st.columns(2)
        with col1:
            tail_lines = st.number_input("Number of lines to tail:", min_value=10, max_value=1000, value=50)
        with col2:
            follow_logs = st.checkbox("Follow logs (real-time)")
        
        if st.button("📜 Show Logs"):
            command = f"docker logs --tail {tail_lines}"
            if follow_logs:
                command += " -f"
            command += f" {selected_container}"
            
            success, output = run_docker_command(command)
            if success:
                st.text(output)
            else:
                st.error(f"❌ Error: {output}")
    else:
        st.info("No containers found")
    
    # Container stats
    st.subheader("📈 Container Statistics")
    if containers:
        if st.button("📈 Show Container Stats"):
            success, output = run_docker_command("docker stats --no-stream")
            if success:
                st.text(output)
            else:
                st.error(f"❌ Error: {output}")
    
    # Container inspection
    st.subheader("🔍 Container Inspection")
    if containers:
        inspect_container = st.selectbox("Select Container to Inspect:", container_names, key="inspect_container")
        
        if st.button("🔍 Inspect Container"):
            success, output = run_docker_command(f"docker inspect {inspect_container}")
            if success:
                try:
                    container_info = json.loads(output)
                    st.json(container_info)
                except:
                    st.text(output)
            else:
                st.error(f"❌ Error: {output}")

def show_image_management():
    """Show comprehensive image management page"""
    st.header("🖼️ Image Management")
    
    # Image operations
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("⬇️ Pull Image")
        pull_image = st.text_input("Image to Pull:", placeholder="nginx:latest")
        
        if st.button("⬇️ Pull Image"):
            if pull_image:
                success, output = run_docker_command(f"docker pull {pull_image}")
                if success:
                    st.success("✅ Image pulled successfully!")
                else:
                    st.error(f"❌ Error: {output}")
            else:
                st.warning("⚠️ Please enter an image name")
    
    with col2:
        st.subheader("🗑️ Remove Image")
        images = get_images()
        if images:
            image_names = [f"{img.get('Repository', 'Unknown')}:{img.get('Tag', 'latest')}" for img in images]
            selected_image = st.selectbox("Select Image:", image_names)
            force_remove = st.checkbox("Force remove")
            
            if st.button("🗑️ Remove Image"):
                command = "docker rmi"
                if force_remove:
                    command += " -f"
                command += f" {selected_image}"
                
                success, output = run_docker_command(command)
                if success:
                    st.success("✅ Image removed!")
                else:
                    st.error(f"❌ Error: {output}")
        else:
            st.info("No images found")
    
    # Build image
    st.subheader("🔨 Build Image")
    build_tag = st.text_input("Image Tag:", placeholder="my-app:latest")
    dockerfile_path = st.text_input("Dockerfile Path:", placeholder=".")
    
    if st.button("🔨 Build Image"):
        if build_tag:
            command = f"docker build -t {build_tag} {dockerfile_path if dockerfile_path else '.'}"
            success, output = run_docker_command(command)
            if success:
                st.success("✅ Image built successfully!")
            else:
                st.error(f"❌ Error: {output}")
        else:
            st.warning("⚠️ Please enter an image tag")
    
    # Image list with detailed info
    st.subheader("📋 Image List")
    images = get_images()
    if images:
        df = pd.DataFrame(images)
        st.dataframe(df)
    else:
        st.info("No images found")
    
    # Image inspection
    st.subheader("🔍 Image Inspection")
    if images:
        image_names = [f"{img.get('Repository', 'Unknown')}:{img.get('Tag', 'latest')}" for img in images]
        inspect_image = st.selectbox("Select Image to Inspect:", image_names, key="inspect_image")
        
        if st.button("🔍 Inspect Image"):
            success, output = run_docker_command(f"docker inspect {inspect_image}")
            if success:
                try:
                    image_info = json.loads(output)
                    st.json(image_info)
                except:
                    st.text(output)
            else:
                st.error(f"❌ Error: {output}")

def run():
    """Main function to run the Docker menu module (for app.py compatibility)"""
    try:
        st.set_page_config(
            page_title="Docker Management Dashboard",
            page_icon="🐳",
            layout="wide",
            initial_sidebar_state="expanded"
        )
    except:
        pass  # Page config may have already been set

    # Initialize session state for module
    if 'docker_module_state' not in st.session_state:
        st.session_state.docker_module_state = {
            'page': 'home',
            'last_refresh': time.time()
        }

    # Sidebar navigation (for app.py integration, use st.sidebar directly)
    with st.sidebar:
        st.markdown("## 🐳 Docker Management")
        page = st.radio(
            "Select Page:",
            [
                "🏠 Home", 
                "📦 Container Management",
                "🖼️ Image Management",
                "💾 Volume Management",
                "🌐 Network Management",
                "📊 Logs & Monitoring",
                "🧹 Maintenance",
                "⚙️ Advanced",
                "🔄 Docker Compose",
                "📄 Dockerfile Generator",
                "🤖 AI Assistant",
                "📊 System Info"
            ]
        )

    # Page routing logic
    if page == "🏠 Home":
        show_home_page()
    elif page == "📦 Container Management":
        show_container_management()
    elif page == "🖼️ Image Management":
        show_image_management()
    elif page == "💾 Volume Management":
        show_volume_management()
    elif page == "🌐 Network Management":
        show_network_management()
    elif page == "📊 Logs & Monitoring":
        show_logs_monitoring()
    elif page == "🧹 Maintenance":
        show_maintenance_cleanup()
    elif page == "⚙️ Advanced":
        show_docker_advanced()
    elif page == "🔄 Docker Compose":
        show_docker_compose()
    elif page == "📄 Dockerfile Generator":
        show_dockerfile_generator()
    elif page == "🤖 AI Assistant":
        show_ai_assistant()
    elif page == "📊 System Info":
        show_system_info()

    # Add error handling wrapper
    try:
        # Refresh data periodically
        if time.time() - st.session_state.docker_module_state['last_refresh'] > 30:
            st.session_state.docker_module_state['last_refresh'] = time.time()
            st.rerun()
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")

def show_home_page():
    """Show the home page with overview"""
    st.header("🏠 Welcome to DOX")
    st.markdown("""
    **DOX** is your comprehensive Docker automation tool with the following features:
    
    - 📦 **Container Management**: Create, start, stop, and manage containers
    - 🖼️ **Image Management**: Pull, build, remove, and inspect Docker images
    - 💾 **Volume Management**: Create, remove, and manage Docker volumes
    - 🌐 **Network Management**: Create, remove, and manage Docker networks
    - 📊 **Logs & Monitoring**: View container logs, stats, and inspect resources
    - 🧹 **Maintenance & Cleanup**: System cleanup, pruning, and disk usage monitoring
    - 🔄 **Docker Compose**: Generate and manage multi-container applications
    - 📄 **Dockerfile Generator**: Create Dockerfiles with AI assistance
    - 🤖 **AI Assistant**: Natural language to Docker commands
    - 📊 **System Info**: Monitor Docker system resources
    """)
    
    # Quick stats
    st.subheader("📊 Quick Overview")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        containers = get_containers()
        running_containers = len([c for c in containers if 'running' in c.get('State', '').lower()])
        st.metric("Running Containers", running_containers, len(containers) - running_containers)
    
    with col2:
        images = get_images()
        st.metric("Total Images", len(images))
    
    with col3:
        volumes = get_volumes()
        st.metric("Volumes", len(volumes))
    
    with col4:
        networks = get_networks()
        st.metric("Networks", len(networks))

def show_container_management():
    """Show container management page"""
    st.header("📦 Container Management")
    
    # Container operations
    st.subheader("🔧 Container Operations")
    
    col1, col2 = st.columns(2)
        
    with col1:
        st.markdown("### 🚀 Create & Run Container")
        image_name = st.text_input("Image Name:", placeholder="nginx:latest")
        container_name = st.text_input("Container Name (optional):", placeholder="my-nginx")
        port_mapping = st.text_input("Port Mapping (optional):", placeholder="80:80")
        
        if st.button("🐳 Run Container"):
            if image_name:
                command = f"docker run -d"
                if container_name:
                    command += f" --name {container_name}"
                if port_mapping:
                    command += f" -p {port_mapping}"
                command += f" {image_name}"
                
                success, output = run_docker_command(command)
                if success:
                    st.success("✅ Container started successfully!")
                else:
                    st.error(f"❌ Error: {output}")
            else:
                st.warning("⚠️ Please enter an image name")
            
    with col2:
        st.markdown("### 🛑 Container Control")
        containers = get_containers()
        if containers:
            container_names = [c.get('Names', 'Unknown') for c in containers]
            selected_container = st.selectbox("Select Container:", container_names)
            
            col_a, col_b, col_c = st.columns(3)
            
            with col_a:
                if st.button("▶️ Start"):
                    success, output = run_docker_command(f"docker start {selected_container}")
                    if success:
                        st.success("✅ Container started!")
                    else:
                        st.error(f"❌ Error: {output}")
            
            with col_b:
                if st.button("⏹️ Stop"):
                    success, output = run_docker_command(f"docker stop {selected_container}")
                    if success:
                        st.success("✅ Container stopped!")
                    else:
                        st.error(f"❌ Error: {output}")
            
            with col_c:
                if st.button("🗑️ Remove"):
                    success, output = run_docker_command(f"docker rm {selected_container}")
                    if success:
                        st.success("✅ Container removed!")
                    else:
                        st.error(f"❌ Error: {output}")
        else:
            st.info("No containers found")
    
    # Container list
    st.subheader("📋 Container List")
    containers = get_containers()
    if containers:
        df = pd.DataFrame(containers)
        st.dataframe(df[['Names', 'Image', 'Status', 'Ports']] if 'Names' in df.columns else df)
    else:
        st.info("No containers found")

def show_docker_compose():
    """Show Docker Compose page"""
    st.header("🔄 Docker Compose")
    
    st.markdown("### 📝 Docker Compose Generator")
    
    # Service configuration
    service_name = st.text_input("Service Name:", placeholder="web")
    image = st.text_input("Image:", placeholder="nginx:latest")
    ports = st.text_input("Ports (optional):", placeholder="80:80")
    environment = st.text_area("Environment Variables (optional):", placeholder="NODE_ENV=production")
    volumes = st.text_area("Volumes (optional):", placeholder="./app:/app")
    
    if st.button("📄 Generate Docker Compose"):
        compose_content = f"""version: '3.8'

services:
  {service_name}:
    image: {image}
    ports:
      - "{ports}"
    environment:
      - {environment}
    volumes:
      - {volumes}
"""
        
        st.code(compose_content, language='yaml')
        
        # Download button
        st.download_button(
            label="💾 Download docker-compose.yml",
            data=compose_content,
            file_name="docker-compose.yml",
            mime="text/yaml"
        )

def show_dockerfile_generator():
    """Show Dockerfile generator page"""
    st.header("📄 Dockerfile Generator")
    
    st.markdown("### 🤖 AI-Powered Dockerfile Generation")
    
    app_description = st.text_area(
        "Describe your application:",
        placeholder="A Python Flask web application with Redis cache and PostgreSQL database...",
        height=100
    )
            
    if st.button("🤖 Generate Dockerfile"):
        if app_description:
            if "python" in app_description.lower() or "flask" in app_description.lower():
                dockerfile_content = """# Use the official Python runtime as a parent image
FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \\
    gcc \\
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . /app/

# Expose port
EXPOSE 5000

# Run the application
CMD ["python", "app.py"]"""
            else:
                dockerfile_content = """# Use a base image
FROM ubuntu:20.04

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive

# Update package list and install dependencies
RUN apt-get update && apt-get install -y \\
    curl \\
    wget \\
    && rm -rf /var/lib/apt/lists/*

# Set work directory
WORKDIR /app

# Copy application files
COPY . /app/

# Expose port
EXPOSE 8080

# Run the application
CMD ["echo", "Please customize this Dockerfile for your application"]"""
            
            st.code(dockerfile_content, language='dockerfile')
            
            st.download_button(
                label="💾 Download Dockerfile",
                data=dockerfile_content,
                file_name="Dockerfile",
                mime="text/plain"
            )
        else:
            st.warning("⚠️ Please describe your application")

if __name__ == "__main__":
    run()