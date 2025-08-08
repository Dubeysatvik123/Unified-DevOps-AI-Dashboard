import streamlit as st
import subprocess
import os
import json
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime

# Correct imports from projectmodules
from modules.projectmodules import (
    chatgpt_automation,
    cicd_jenkins,
    cloud_automation,
    command_hub,
    docker_apache,
    flask_cicd,
    kubernetes_manager,
    microservices
)

def run():
    st.markdown("""
    <style>
        .main-header {
            font-size: 3rem;
            color: #1f77b4;
            text-align: center;
            margin-bottom: 2rem;
        }
        .project-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 1rem;
            border-radius: 10px;
            color: white;
            margin: 1rem 0;
        }
    </style>
    """, unsafe_allow_html=True)

    st.sidebar.title("🚀 DevOps Projects Hub")
    st.sidebar.markdown("---")

    projects = [
        "🏠 Home",
        "🤖 ChatGPT Automation Agent", 
        "☁️ Cloud Automation using Python",
        "🐳 Apache in Docker Container",
        "🔄 CI/CD: Flask + Jenkins + Docker",
        "🎛️ CommandHub - All-in-One Platform",
        "🌐 Flask Web App with CI/CD",
        "🏗️ Containerized Microservices",
        "☸️ Kubernetes Cluster Management"
    ]

    selected_project = st.sidebar.selectbox("Select Project", projects)

    if selected_project == "🏠 Home":
        show_home()
    elif selected_project == "🤖 ChatGPT Automation Agent":
        chatgpt_automation.chatgpt_automation_page()
    elif selected_project == "☁️ Cloud Automation using Python":
        cloud_automation.cloud_automation_page()
    elif selected_project == "🐳 Apache in Docker Container":
        docker_apache.docker_apache_page()
    elif selected_project == "🔄 CI/CD: Flask + Jenkins + Docker":
        cicd_jenkins.cicd_jenkins_page()
    elif selected_project == "🎛️ CommandHub - All-in-One Platform":
        command_hub.command_hub_page()
    elif selected_project == "🌐 Flask Web App with CI/CD":
        flask_cicd.flask_cicd_page()
    elif selected_project == "🏗️ Containerized Microservices":
        microservices.microservices_page()
    elif selected_project == "☸️ Kubernetes Cluster Management":
        kubernetes_manager.kubernetes_manager_page()

    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🔧 Tools & Technologies")
    st.sidebar.markdown("""
    - **Containers**: Docker, Kubernetes
    - **CI/CD**: Jenkins, GitHub Actions
    - **Cloud**: AWS, Python Boto3
    - **Monitoring**: Prometheus, Grafana
    - **Languages**: Python, JavaScript, Go
    - **Frameworks**: Flask, FastAPI, React
    - **Databases**: PostgreSQL, Redis, MongoDB
    """)

    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📊 Quick Stats")
    st.sidebar.metric("Projects Completed", "8/8", "100%")
    st.sidebar.metric("Success Rate", "98.5%", "+2.3%")
    st.sidebar.metric("Automation Level", "Advanced", "🚀")

def show_home():
    st.markdown('<h1 class="main-header">DevOps Projects Hub 🚀</h1>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="project-card">
            <h3>🤖 AI Automation</h3>
            <p>ChatGPT automation agents for intelligent task handling</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="project-card">
            <h3>☁️ Cloud Infrastructure</h3>
            <p>Python-based cloud automation and monitoring</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="project-card">
            <h3>🔄 CI/CD Pipelines</h3>
            <p>Complete deployment automation workflows</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Projects", "8", "2")
    with col2:
        st.metric("Technologies", "15+", "3")
    with col3:
        st.metric("Containers", "Active", "100%")
    with col4:
        st.metric("Automation Level", "Advanced", "↗️")

    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 2rem;">
        <h4>🚀 DevOps Projects Hub</h4>
        <p>Complete automation and container orchestration solutions</p>
        <p>Built with ❤️ using Streamlit, Docker, Kubernetes, and modern DevOps practices</p>
    </div>
    """, unsafe_allow_html=True)