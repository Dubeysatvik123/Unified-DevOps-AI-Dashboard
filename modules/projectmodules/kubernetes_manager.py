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

def check_kubernetes_available():
    result = run_command("kubectl version --client")
    return result['success']

def kubernetes_manager_page():
    st.header("☸️ Kubernetes Cluster Management")
    
    if not check_kubernetes_available():
        st.error("❌ kubectl is not available. Please install kubectl and ensure a cluster is configured.")
        return
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Kubernetes Configuration")
        kubeconfig_path = st.text_input("Kubeconfig Path", value="~/.kube/config")
        namespace = st.text_input("Namespace", value="default")
        
        try:
            os.environ['KUBECONFIG'] = kubeconfig_path
            result = run_command("kubectl cluster-info")
            if result['success']:
                st.success("✅ Kubernetes cluster connection successful!")
            else:
                st.error(f"❌ Failed to connect to cluster: {result['stderr']}")
        except Exception as e:
            st.error(f"❌ Failed to load kubeconfig: {str(e)}")
            return
    
    with col2:
        st.subheader("Sample Application YAML")
        app_yaml = '''
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment
  namespace: default
spec:
  replicas: 3
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx
        image: nginx:latest
        ports:
        - containerPort: 80
---
apiVersion: v1
kind: Service
metadata:
  name: nginx-service
  namespace: default
spec:
  selector:
    app: nginx
  ports:
    - protocol: TCP
      port: 80
      targetPort: 80
  type: ClusterIP
        '''
        st.code(app_yaml, language="yaml")
    
    st.subheader("Kubernetes Operations")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("🚀 Deploy Application"):
            with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
                f.write(app_yaml)
                f.flush()
                result = run_command(f"kubectl apply -f {f.name} -n {namespace}")
                os.unlink(f.name)
                if result['success']:
                    st.success("✅ Application deployed!")
                else:
                    st.error(f"❌ Deployment failed: {result['stderr']}")
    
    with col2:
        replicas = st.number_input("Replicas", min_value=1, max_value=10, value=3)
        if st.button("📈 Scale Deployment"):
            result = run_command(f"kubectl scale deployment nginx-deployment -n {namespace} --replicas={replicas}")
            if result['success']:
                st.success(f"✅ Deployment scaled to {replicas} replicas!")
            else:
                st.error(f"❌ Scaling failed: {result['stderr']}")
    
    with col3:
        if st.button("📊 Pod Status"):
            result = run_command(f"kubectl get pods -n {namespace} -o wide")
            if result['success']:
                st.code(result['stdout'], language="bash")
            else:
                st.error(f"❌ Failed to get pod status: {result['stderr']}")
    
    with col4:
        if st.button("🗑️ Delete Resources"):
            result = run_command(f"kubectl delete deployment nginx-deployment -n {namespace} && kubectl delete service nginx-service -n {namespace}")
            if result['success']:
                st.success("✅ Resources deleted!")
            else:
                st.error(f"❌ Deletion failed: {result['stderr']}")
    
    st.subheader("Pod Logs")
    pod_name = st.text_input("Pod Name for Logs")
    if st.button("📋 View Pod Logs"):
        if pod_name:
            result = run_command(f"kubectl logs {pod_name} -n {namespace} --tail=50")
            if result['success']:
                st.code(result['stdout'], language="bash")
            else:
                st.error(f"❌ Failed to get logs: {result['stderr']}")