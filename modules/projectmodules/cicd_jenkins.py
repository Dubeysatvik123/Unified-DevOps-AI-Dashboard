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

def test_jenkins_connection(jenkins_url):
    try:
        result = run_command(f"curl -s -o /dev/null -w %{{http_code}} {jenkins_url}/api/json")
        return result['stdout'] == '200'
    except:
        return False

def trigger_jenkins_build(jenkins_url, job_name):
    try:
        result = run_command(f"curl -X POST {jenkins_url}/job/{job_name}/build")
        if result['success']:
            # Get build number
            job_info = run_command(f"curl -s {jenkins_url}/job/{job_name}/api/json")
            if job_info['success']:
                data = json.loads(job_info['stdout'])
                build_number = data.get('nextBuildNumber', 'unknown')
                return {'success': True, 'build_number': build_number}
            return {'success': True}
        else:
            return {'success': False, 'error': result['stderr']}
    except Exception as e:
        return {'success': False, 'error': str(e)}

def get_jenkins_build_status(jenkins_url, job_name, build_number):
    try:
        if not build_number:
            return None
        result = run_command(f"curl -s {jenkins_url}/job/{job_name}/{build_number}/api/json")
        if result['success']:
            data = json.loads(result['stdout'])
            return data.get('result', 'IN_PROGRESS')
        return None
    except:
        return None

def list_jenkins_jobs(jenkins_url):
    try:
        result = run_command(f"curl -s {jenkins_url}/api/json")
        if result['success']:
            data = json.loads(result['stdout'])
            return [job['name'] for job in data.get('jobs', [])]
        return []
    except:
        return []

def get_jenkins_console_output(jenkins_url, job_name, build_number):
    try:
        if not build_number:
            return None
        result = run_command(f"curl -s {jenkins_url}/job/{job_name}/{build_number}/consoleText")
        if result['success']:
            return result['stdout']
        return None
    except:
        return None

def cicd_jenkins_page():
    st.header("🔄 CI/CD Pipeline: Jenkins Integration")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Jenkins Configuration")
        jenkins_url = st.text_input("Jenkins URL", value="http://localhost:8080")
        if st.button("🔐 Test Jenkins Connection"):
            if jenkins_url:
                if test_jenkins_connection(jenkins_url):
                    st.success("✅ Jenkins connection successful!")
                else:
                    st.error("❌ Jenkins connection failed!")
            else:
                st.error("Please provide Jenkins URL")
    
    with col2:
        st.subheader("Build Configuration")
        job_name = st.text_input("Jenkins Job Name", value="flask-app-build")
        branch_name = st.text_input("Git Branch", value="main")
        docker_tag = st.text_input("Docker Tag", value="latest")
    
    st.subheader("Pipeline Operations")
    
    if jenkins_url:
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            if st.button("🚀 Trigger Build"):
                with st.spinner("Triggering Jenkins build..."):
                    result = trigger_jenkins_build(jenkins_url, job_name)
                    if result['success']:
                        st.success(f"✅ Build triggered! Build number: {result.get('build_number', 'N/A')}")
                        build_info = {
                            'job': job_name,
                            'build_number': result.get('build_number'),
                            'timestamp': datetime.now().isoformat(),
                            'status': 'TRIGGERED'
                        }
                        if 'jenkins_jobs' not in st.session_state:
                            st.session_state.jenkins_jobs = []
                        st.session_state.jenkins_jobs.append(build_info)
                    else:
                        st.error(f"❌ Build failed to trigger: {result['error']}")
        with col2:
            if st.button("📊 Get Build Status"):
                if st.session_state.get('jenkins_jobs'):
                    latest_build = st.session_state.jenkins_jobs[-1]
                    status = get_jenkins_build_status(
                        jenkins_url, job_name, latest_build.get('build_number')
                    )
                    if status:
                        st.info(f"Build Status: {status}")
                    else:
                        st.error("Failed to get build status")
        with col3:
            if st.button("📋 List Jobs"):
                jobs = list_jenkins_jobs(jenkins_url)
                if jobs:
                    st.write("Available Jobs:")
                    for job in jobs:
                        st.write(f"• {job}")
        with col4:
            if st.button("🔄 Refresh Console"):
                if st.session_state.get('jenkins_jobs'):
                    latest_build = st.session_state.jenkins_jobs[-1]
                    console_output = get_jenkins_console_output(
                        jenkins_url, job_name, latest_build.get('build_number')
                    )
                    if console_output:
                        st.code(console_output[-1000:], language="bash")
                    else:
                        st.error("Failed to get console output")

        if st.session_state.get('jenkins_jobs'):
            st.subheader("Build History")
            import pandas as pd
            df = pd.DataFrame(st.session_state.jenkins_jobs)
            st.dataframe(df, use_container_width=True)

    with st.expander("📄 Sample Jenkinsfile"):
        jenkinsfile = '''
pipeline {
    agent any
    environment {
        DOCKER_IMAGE = "flask-app"
        DOCKER_TAG = "${BUILD_NUMBER}"
    }
    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/Dubeysatvik123/CICD_Flask.git'
            }
        }
        stage('Build') {
            steps {
                sh 'docker build -t ${DOCKER_IMAGE}:${DOCKER_TAG} .'
            }
        }
        stage('Test') {
            steps {
                sh 'python -m pytest tests/ -v'
            }
        }
        stage('Deploy') {
            steps {
                sh 'docker run -d -p 5000:5000 --name flask-app-${BUILD_NUMBER} ${DOCKER_IMAGE}:${DOCKER_TAG}'
            }
        }
    }
    post {
        always {
            cleanWs()
        }
    }
}
'''
        st.code(jenkinsfile, language="groovy")