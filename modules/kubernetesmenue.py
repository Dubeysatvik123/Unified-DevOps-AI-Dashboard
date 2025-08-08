import streamlit as st
import subprocess
import yaml
import requests
import os
import tempfile
import json
import re
from datetime import datetime
import time
import base64

def show_k8s_blog():
    st.header("📖 Kubernetes Case Studies & Blog")
    st.markdown("""
    ### Why Companies Use Kubernetes
    - **Scalability**: Easily scale applications up/down
    - **Portability**: Run anywhere (cloud, on-prem)
    - **Self-healing**: Automatic restarts, rescheduling
    - **Declarative config**: Infrastructure as code
    - **Ecosystem**: Helm, Operators, Service Mesh, etc.
    - **Case studies**: Google, Spotify, Airbnb, CERN, Shopify
    """)
    st.markdown("---")
    st.subheader("Generate Blog Outline")
    if st.button("Generate Blog Outline"):
        st.markdown("""
        **Introduction**
        - What is Kubernetes?
        - Why is it popular?
        
        **Case Studies**
        - Google: Internal Borg to Kubernetes
        - Spotify: Microservices at scale
        - Shopify: Black Friday scaling
        - CERN: Scientific workloads
        
        **Benefits**
        - Cost savings
        - Developer velocity
        - Reliability
        
        **Conclusion**
        - Future of Kubernetes
        """)

def show_k8s_multitier_launcher():
    st.header("🚀 Launch Multi-Tier App on Kubernetes")
    st.markdown("""
    Clone and deploy a 3-tier microservice app from GitHub.
    """)
    if st.button("Clone and Launch 3-Tier App"):
        import subprocess
        repo_url = "https://github.com/Dubeysatvik123/Three_Tier_Microservice.git"
        dest = "Three_Tier_Microservice"
        if not os.path.exists(dest):
            result = subprocess.run(["git", "clone", repo_url], capture_output=True, text=True)
            if result.returncode == 0:
                st.success("✅ Repository cloned successfully!")
            else:
                st.error(f"❌ Error cloning repository: {result.stderr}")
        else:
            st.info("Repository already exists locally")
        
        st.success("Repo ready! Now run the provided Kubernetes manifests to deploy.")
        st.code("kubectl apply -f Three_Tier_Microservice/k8s/", language="bash")
        
        # Add deployment button for the multi-tier app
        if st.button("Deploy Multi-Tier App"):
            if os.path.exists(f"{dest}/k8s/"):
                deploy_result = run_kubectl_command(f"kubectl apply -f {dest}/k8s/")
                st.code(deploy_result)
            else:
                st.warning("Please clone the repository first or check if k8s/ directory exists")

def show_k8s_live_stream():
    st.header("📺 Launch Live Stream Website on Kubernetes")
    st.markdown("""
    Deploy live streaming platforms using open source projects.
    """)
    
    streaming_platform = st.selectbox("Choose Streaming Platform", [
        "Owncast",
        "Ant Media Server",
        "Simple NGINX RTMP"
    ])
    
    if st.button("Deploy Streaming Platform"):
        if streaming_platform == "Owncast":
            # Deploy Owncast
            deployment_yaml = """
apiVersion: apps/v1
kind: Deployment
metadata:
  name: owncast
spec:
  replicas: 1
  selector:
    matchLabels:
      app: owncast
  template:
    metadata:
      labels:
        app: owncast
    spec:
      containers:
      - name: owncast
        image: owncast/owncast:latest
        ports:
        - containerPort: 8080
        - containerPort: 1935
---
apiVersion: v1
kind: Service
metadata:
  name: owncast-service
spec:
  selector:
    app: owncast
  ports:
  - name: web
    port: 8080
    targetPort: 8080
  - name: rtmp
    port: 1935
    targetPort: 1935
  type: NodePort
"""
            result = apply_yaml_content(deployment_yaml, "owncast-deployment")
            st.code(result)
            
        elif streaming_platform == "Simple NGINX RTMP":
            # Deploy NGINX RTMP
            deployment_yaml = """
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-rtmp
spec:
  replicas: 1
  selector:
    matchLabels:
      app: nginx-rtmp
  template:
    metadata:
      labels:
        app: nginx-rtmp
    spec:
      containers:
      - name: nginx-rtmp
        image: tiangolo/nginx-rtmp:latest
        ports:
        - containerPort: 80
        - containerPort: 1935
---
apiVersion: v1
kind: Service
metadata:
  name: nginx-rtmp-service
spec:
  selector:
    app: nginx-rtmp
  ports:
  - name: web
    port: 80
    targetPort: 80
  - name: rtmp
    port: 1935
    targetPort: 1935
  type: NodePort
"""
            result = apply_yaml_content(deployment_yaml, "nginx-rtmp-deployment")
            st.code(result)
            
        st.success(f"✅ {streaming_platform} deployment initiated!")

def show_home():
    st.header("☸️ Kubernetes Automation")
    st.markdown("""
    Welcome to the Kubernetes Automation module!
    - Create, manage, and monitor clusters
    - Deploy applications
    - View cluster status and resources
    """)

def show_cluster_management():
    st.subheader("🔧 Cluster Management")
    st.write("Cluster creation, scaling, and deletion tools coming soon.")

def show_app_deployment():
    st.subheader("🚀 Application Deployment")
    st.write("Deploy your apps to Kubernetes clusters (feature coming soon).")

def show_monitoring():
    st.subheader("📊 Monitoring & Logs")
    st.write("View cluster and pod logs, resource usage, and health.")

def run():
    """Main function to run the Kubernetes menu module"""
    # Streamlit Dashboard Setup
    st.set_page_config(
        page_title="Kubernetes Automation",
        page_icon="☸️",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    with st.sidebar:
        page = st.radio(
            "Kubernetes Menu",
            [
                "🏠 Home",
                "📖 Kubernetes Blog", 
                "🚀 Multi-Tier App", 
                "📺 Live Stream Platform", 
                "🔧 Cluster Management", 
                "📊 Resource Monitoring", 
                "🛠️ YAML Generator", 
                "🔍 Resource Explorer",
                "🔐 Security & RBAC",
                "🌐 Networking",
                "💾 Storage Management",
                "🎛️ Advanced Operations",
                "📦 Package Management",
                "🔧 Maintenance & Ops"
            ]
        )
    
    if page == "🏠 Home":
        show_home()
    elif page == "📖 Kubernetes Blog":
        show_k8s_blog()
        
    elif page == "🚀 Multi-Tier App":
        show_k8s_multitier_launcher()
        
    elif page == "📺 Live Stream Platform":
        show_k8s_live_stream()
        
    elif page == "🔧 Cluster Management":
        st.subheader("🔧 Cluster Management")
        
        # Cluster Overview
        st.subheader("Cluster Overview")
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🔍 Get Cluster Info"):
                cluster_info = run_kubectl_command("kubectl cluster-info")
                st.code(cluster_info)
        
        with col2:
            if st.button("📋 Get Nodes"):
                nodes = run_kubectl_command("kubectl get nodes -o wide")
                st.code(nodes)

        st.markdown("---")
        
        # Pod Management
        st.subheader("Pod Management")
        pod_cols = st.columns(4)
        
        with pod_cols[0]:
            if st.button("📦 List All Pods"):
                pods = run_kubectl_command("kubectl get pods --all-namespaces")
                st.code(pods)
        
        with pod_cols[1]:
            if st.button("🔄 List Running Pods"):
                running_pods = run_kubectl_command("kubectl get pods --field-selector=status.phase=Running")
                st.code(running_pods)
        
        with pod_cols[2]:
            if st.button("⚠️ List Failed Pods"):
                failed_pods = run_kubectl_command("kubectl get pods --field-selector=status.phase=Failed")
                st.code(failed_pods)
        
        with pod_cols[3]:
            if st.button("🔄 List Pending Pods"):
                pending_pods = run_kubectl_command("kubectl get pods --field-selector=status.phase=Pending")
                st.code(pending_pods)

        # Service Management
        st.subheader("Service Management")
        service_cols = st.columns(3)
        
        with service_cols[0]:
            if st.button("🌐 List Services"):
                services = run_kubectl_command("kubectl get services")
                st.code(services)
        
        with service_cols[1]:
            if st.button("🔗 List Endpoints"):
                endpoints = run_kubectl_command("kubectl get endpoints")
                st.code(endpoints)
        
        with service_cols[2]:
            if st.button("🔧 List Ingress"):
                ingress = run_kubectl_command("kubectl get ingress")
                st.code(ingress)

        # Deployment Management
        st.subheader("Deployment Management")
        deploy_cols = st.columns(4)
        
        with deploy_cols[0]:
            if st.button("🚀 List Deployments"):
                deployments = run_kubectl_command("kubectl get deployments")
                st.code(deployments)
        
        with deploy_cols[1]:
            if st.button("📊 List ReplicaSets"):
                replicasets = run_kubectl_command("kubectl get replicasets")
                st.code(replicasets)
        
        with deploy_cols[2]:
            if st.button("⚙️ List DaemonSets"):
                daemonsets = run_kubectl_command("kubectl get daemonsets")
                st.code(daemonsets)
        
        with deploy_cols[3]:
            if st.button("🎯 List StatefulSets"):
                statefulsets = run_kubectl_command("kubectl get statefulsets")
                st.code(statefulsets)

        # Quick Actions
        st.subheader("Quick Actions")
        action_cols = st.columns(3)
        
        with action_cols[0]:
            st.write("**Scale Deployment**")
            deployment_name = st.text_input("Deployment Name:", key="scale_deploy")
            replicas = st.number_input("Replicas:", min_value=0, max_value=100, value=3, key="replicas")
            if st.button("Scale", key="scale_btn"):
                if deployment_name:
                    result = run_kubectl_command(f"kubectl scale deployment {deployment_name} --replicas={replicas}")
                    st.code(result)
        
        with action_cols[1]:
            st.write("**Delete Resource**")
            resource_type = st.selectbox("Resource Type:", ["pod", "service", "deployment", "configmap", "secret"], key="del_type")
            resource_name = st.text_input("Resource Name:", key="del_name")
            if st.button("Delete", key="del_btn"):
                if resource_name:
                    result = run_kubectl_command(f"kubectl delete {resource_type} {resource_name}")
                    st.code(result)
        
        with action_cols[2]:
            st.write("**Restart Deployment**")
            restart_deployment = st.text_input("Deployment Name:", key="restart_deploy")
            if st.button("Restart", key="restart_btn"):
                if restart_deployment:
                    result = run_kubectl_command(f"kubectl rollout restart deployment/{restart_deployment}")
                    st.code(result)

    elif page == "📊 Resource Monitoring":
        st.header("📊 Resource Monitoring")
        
        # Real-time metrics
        monitor_cols = st.columns(4)
        
        with monitor_cols[0]:
            if st.button("📈 Node Resource Usage"):
                node_usage = run_kubectl_command("kubectl top nodes")
                st.code(node_usage)
        
        with monitor_cols[1]:
            if st.button("📊 Pod Resource Usage"):
                pod_usage = run_kubectl_command("kubectl top pods")
                st.code(pod_usage)
        
        with monitor_cols[2]:
            if st.button("🔍 Cluster Events"):
                events = run_kubectl_command("kubectl get events --sort-by=.metadata.creationTimestamp")
                st.code(events)
        
        with monitor_cols[3]:
            if st.button("⚠️ Problem Pods"):
                problem_pods = run_kubectl_command("kubectl get pods --all-namespaces | grep -v Running | grep -v Completed")
                st.code(problem_pods)

        # Logs and Debugging
        st.subheader("Logs and Debugging")
        log_cols = st.columns(2)
        
        with log_cols[0]:
            st.write("**Pod Logs**")
            log_pod_name = st.text_input("Pod Name:", key="log_pod")
            if st.button("Get Logs", key="get_logs"):
                if log_pod_name:
                    logs = run_kubectl_command(f"kubectl logs {log_pod_name}")
                    st.text_area("Pod Logs:", logs, height=200)
        
        with log_cols[1]:
            st.write("**Describe Resource**")
            desc_resource_type = st.selectbox("Resource Type:", ["pod", "service", "deployment", "node"], key="desc_type")
            desc_resource_name = st.text_input("Resource Name:", key="desc_name")
            if st.button("Describe", key="desc_btn"):
                if desc_resource_name:
                    description = run_kubectl_command(f"kubectl describe {desc_resource_type} {desc_resource_name}")
                    st.text_area("Resource Description:", description, height=200)

    elif page == "🛠️ YAML Generator":
        st.header("🛠️ YAML Generator")
        
        # YAML Generator
        yaml_type = st.selectbox("Select Resource Type:", [
            "Deployment",
            "Service",
            "ConfigMap",
            "Secret",
            "Ingress",
            "PersistentVolume",
            "PersistentVolumeClaim",
            "CronJob",
            "Job",
            "HorizontalPodAutoscaler"
        ])
        
        if yaml_type == "Deployment":
            st.subheader("Generate Deployment YAML")
            dep_name = st.text_input("Deployment Name:", "my-app")
            dep_image = st.text_input("Container Image:", "nginx:latest")
            dep_replicas = st.number_input("Replicas:", min_value=1, max_value=10, value=3)
            dep_port = st.number_input("Container Port:", min_value=1, max_value=65535, value=80)
            
            if st.button("Generate Deployment YAML"):
                deployment_yaml = f"""
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {dep_name}
  labels:
    app: {dep_name}
spec:
  replicas: {dep_replicas}
  selector:
    matchLabels:
      app: {dep_name}
  template:
    metadata:
      labels:
        app: {dep_name}
    spec:
      containers:
      - name: {dep_name}
        image: {dep_image}
        ports:
        - containerPort: {dep_port}
"""
                st.code(deployment_yaml, language="yaml")
                
                if st.button("Apply This YAML"):
                    result = apply_yaml_content(deployment_yaml, f"{dep_name}-deployment")
                    st.code(result)
        
        elif yaml_type == "Service":
            st.subheader("Generate Service YAML")
            svc_name = st.text_input("Service Name:", "my-service")
            svc_app = st.text_input("Target App Label:", "my-app")
            svc_port = st.number_input("Service Port:", min_value=1, max_value=65535, value=80)
            svc_target_port = st.number_input("Target Port:", min_value=1, max_value=65535, value=80)
            svc_type = st.selectbox("Service Type:", ["ClusterIP", "NodePort", "LoadBalancer"])
            
            if st.button("Generate Service YAML"):
                service_yaml = f"""
apiVersion: v1
kind: Service
metadata:
  name: {svc_name}
spec:
  selector:
    app: {svc_app}
  ports:
  - port: {svc_port}
    targetPort: {svc_target_port}
  type: {svc_type}
"""
                st.code(service_yaml, language="yaml")
                
                if st.button("Apply This YAML"):
                    result = apply_yaml_content(service_yaml, f"{svc_name}-service")
                    st.code(result)
        
        # Custom YAML Editor
        st.subheader("Custom YAML Editor")
        custom_yaml = st.text_area("Enter your YAML manifest:", height=200)
        
        if st.button("Apply Custom YAML"):
            if custom_yaml.strip():
                result = apply_yaml_content(custom_yaml, "custom-manifest")
                st.code(result)
            else:
                st.warning("Please enter a YAML manifest")

    elif page == "🔍 Resource Explorer":
        st.header("🔍 Resource Explorer")
        
        # Resource details
        explore_cols = st.columns(2)
        
        with explore_cols[0]:
            st.subheader("Get Resource Details")
            resource_type = st.selectbox("Resource Type:", [
                "pods", "services", "deployments", "configmaps", 
                "secrets", "ingress", "nodes", "namespaces",
                "persistentvolumes", "persistentvolumeclaims"
            ])
            
            output_format = st.selectbox("Output Format:", ["table", "yaml", "json", "wide"])
            
            if st.button("Get Resources"):
                if output_format == "table":
                    cmd = f"kubectl get {resource_type}"
                else:
                    cmd = f"kubectl get {resource_type} -o {output_format}"
                
                result = run_kubectl_command(cmd)
                st.code(result)
        
        with explore_cols[1]:
            st.subheader("Resource Filtering")
            
            # Label selector
            label_selector = st.text_input("Label Selector (e.g., app=nginx):")
            field_selector = st.text_input("Field Selector (e.g., status.phase=Running):")
            
            if st.button("Apply Filters"):
                cmd = f"kubectl get pods"
                if label_selector:
                    cmd += f" -l {label_selector}"
                if field_selector:
                    cmd += f" --field-selector={field_selector}"
                
                result = run_kubectl_command(cmd)
                st.code(result)

        # Port forwarding
        st.subheader("Port Forwarding")
        pf_cols = st.columns(3)
        
        with pf_cols[0]:
            pf_resource = st.text_input("Resource (pod/service):", "pod/my-pod")
        with pf_cols[1]:
            pf_local_port = st.number_input("Local Port:", min_value=1000, max_value=65535, value=8080)
        with pf_cols[2]:
            pf_remote_port = st.number_input("Remote Port:", min_value=1, max_value=65535, value=80)
        
        if st.button("Start Port Forward"):
            st.info(f"To start port forwarding, run this command in your terminal:")
            st.code(f"kubectl port-forward {pf_resource} {pf_local_port}:{pf_remote_port}")

        # Exec into pods
        st.subheader("Execute Commands in Pods")
        exec_cols = st.columns(2)
        
        with exec_cols[0]:
            exec_pod = st.text_input("Pod Name:", "my-pod")
            exec_command = st.text_input("Command:", "/bin/bash")
        
        with exec_cols[1]:
            if st.button("Generate Exec Command"):
                st.code(f"kubectl exec -it {exec_pod} -- {exec_command}")

    elif page == "🔐 Security & RBAC":
        st.header("🔐 Security & RBAC Management")
        
        # RBAC Overview
        st.subheader("RBAC Resources")
        rbac_cols = st.columns(4)
        
        with rbac_cols[0]:
            if st.button("👥 List ServiceAccounts"):
                sa = run_kubectl_command("kubectl get serviceaccounts --all-namespaces")
                st.code(sa)
        
        with rbac_cols[1]:
            if st.button("🎭 List Roles"):
                roles = run_kubectl_command("kubectl get roles --all-namespaces")
                st.code(roles)
        
        with rbac_cols[2]:
            if st.button("🌐 List ClusterRoles"):
                cluster_roles = run_kubectl_command("kubectl get clusterroles")
                st.code(cluster_roles)
        
        with rbac_cols[3]:
            if st.button("🔗 List RoleBindings"):
                role_bindings = run_kubectl_command("kubectl get rolebindings --all-namespaces")
                st.code(role_bindings)

        # Security Policies
        st.subheader("Security Policies")
        security_cols = st.columns(3)
        
        with security_cols[0]:
            if st.button("🛡️ List NetworkPolicies"):
                net_policies = run_kubectl_command("kubectl get networkpolicies --all-namespaces")
                st.code(net_policies)
        
        with security_cols[1]:
            if st.button("🔒 List PodSecurityPolicies"):
                psp = run_kubectl_command("kubectl get podsecuritypolicies")
                st.code(psp)
        
        with security_cols[2]:
            if st.button("🔐 List Secrets"):
                secrets = run_kubectl_command("kubectl get secrets --all-namespaces")
                st.code(secrets)

        # Create RBAC Resources
        st.subheader("Create RBAC Resources")
        
        # ServiceAccount Creation
        col1, col2 = st.columns(2)
        with col1:
            st.write("**Create ServiceAccount**")
            sa_name = st.text_input("ServiceAccount Name:", "my-service-account")
            sa_namespace = st.text_input("Namespace:", "default", key="sa_ns")
            if st.button("Create ServiceAccount"):
                result = run_kubectl_command(f"kubectl create serviceaccount {sa_name} -n {sa_namespace}")
                st.code(result)
        
        with col2:
            st.write("**Create Secret**")
            secret_name = st.text_input("Secret Name:", "my-secret")
            secret_type = st.selectbox("Secret Type:", ["generic", "docker-registry", "tls"])
            if secret_type == "generic":
                key = st.text_input("Key:", "username")
                value = st.text_input("Value:", "admin", type="password")
                if st.button("Create Generic Secret"):
                    result = run_kubectl_command(f"kubectl create secret generic {secret_name} --from-literal={key}={value}")
                    st.code(result)

        # RBAC Generator
        st.subheader("RBAC YAML Generator")
        rbac_type = st.selectbox("RBAC Resource Type:", ["Role", "ClusterRole", "RoleBinding", "ClusterRoleBinding"])
        
        if rbac_type in ["Role", "ClusterRole"]:
            role_name = st.text_input("Role Name:", "my-role")
            verbs = st.multiselect("Verbs:", ["get", "list", "create", "update", "patch", "delete", "watch"])
            resources = st.multiselect("Resources:", ["pods", "services", "deployments", "configmaps", "secrets"])
            
            if st.button(f"Generate {rbac_type} YAML"):
                if rbac_type == "Role":
                    rbac_yaml = f"""
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: {role_name}
  namespace: {selected_namespace}
rules:
- apiGroups: [""]
  resources: {json.dumps(resources)}
  verbs: {json.dumps(verbs)}
"""
                else:
                    rbac_yaml = f"""
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: {role_name}
rules:
- apiGroups: [""]
  resources: {json.dumps(resources)}
  verbs: {json.dumps(verbs)}
"""
                st.code(rbac_yaml, language="yaml")
                if st.button(f"Apply {rbac_type}"):
                    result = apply_yaml_content(rbac_yaml, f"{role_name}-{rbac_type.lower()}")
                    st.code(result)

        # Security Scanning
        st.subheader("Security Scanning")
        scan_cols = st.columns(2)
        
        with scan_cols[0]:
            if st.button("🔍 Check Pod Security"):
                # Check for pods running as root
                root_pods = run_kubectl_command("kubectl get pods -o jsonpath='{range .items[*]}{.metadata.name}{\"\\t\"}{.spec.securityContext.runAsUser}{\"\\n\"}{end}'")
                st.code(root_pods)
        
        with scan_cols[1]:
            if st.button("🛡️ Check Resource Limits"):
                # Check pods without resource limits
                no_limits = run_kubectl_command("kubectl get pods -o jsonpath='{range .items[*]}{.metadata.name}{\"\\t\"}{.spec.containers[*].resources.limits}{\"\\n\"}{end}'")
                st.code(no_limits)

    elif page == "🌐 Networking":
        st.header("🌐 Network Management")
        
        # Network Overview
        st.subheader("Network Resources")
        net_cols = st.columns(4)
        
        with net_cols[0]:
            if st.button("🌐 List Services"):
                services = run_kubectl_command("kubectl get services --all-namespaces")
                st.code(services)
        
        with net_cols[1]:
            if st.button("🔗 List Endpoints"):
                endpoints = run_kubectl_command("kubectl get endpoints --all-namespaces")
                st.code(endpoints)
        
        with net_cols[2]:
            if st.button("🚪 List Ingress"):
                ingress = run_kubectl_command("kubectl get ingress --all-namespaces")
                st.code(ingress)
        
        with net_cols[3]:
            if st.button("🛡️ List NetworkPolicies"):
                netpol = run_kubectl_command("kubectl get networkpolicies --all-namespaces")
                st.code(netpol)

        # DNS and Service Discovery
        st.subheader("DNS & Service Discovery")
        dns_cols = st.columns(3)
        
        with dns_cols[0]:
            if st.button("🔍 Check CoreDNS"):
                coredns = run_kubectl_command("kubectl get pods -n kube-system -l k8s-app=kube-dns")
                st.code(coredns)
        
        with dns_cols[1]:
            if st.button("🔄 Restart CoreDNS"):
                restart_coredns = run_kubectl_command("kubectl rollout restart deployment coredns -n kube-system")
                st.code(restart_coredns)
        
        with dns_cols[2]:
            if st.button("📜 View CoreDNS Logs"):
                coredns_logs = run_kubectl_command("kubectl logs -l k8s-app=kube-dns -n kube-system")
                st.text_area("CoreDNS Logs:", coredns_logs, height=200)

        # Network Troubleshooting
        st.subheader("Network Troubleshooting")
        troubleshoot_cols = st.columns(2)
        
        with troubleshoot_cols[0]:
            st.write("**Check Pod-to-Pod Connectivity**")
            pod_a = st.text_input("Pod A Name:", "pod-a")
            pod_b = st.text_input("Pod B Name:", "pod-b")
            if st.button("Test Connectivity"):
                if pod_a and pod_b:
                    result = run_kubectl_command(f"kubectl exec {pod_a} -- ping -c 4 {pod_b}")
                    st.code(result)
        
        with troubleshoot_cols[1]:
            st.write("**Check Service Endpoints**")
            service_name = st.text_input("Service Name:", "my-service")
            if st.button("Get Endpoints"):
                if service_name:
                    endpoints = run_kubectl_command(f"kubectl get service {service_name} -o jsonpath='{{.spec.clusterIP}}'")
                    st.code(endpoints)

        # Network Policy Management
        st.subheader("Network Policy Management")
        np_cols = st.columns(2)
        
        with np_cols[0]:
            st.write("**Create Network Policy**")
            np_name = st.text_input("Network Policy Name:", "my-network-policy")
            pod_selector = st.text_input("Pod Selector (e.g., app=myapp):", "app=myapp")
            ingress_from = st.text_input("Ingress From (e.g., pod-ip-or-namespace):", "")
            egress_to = st.text_input("Egress To (e.g., pod-ip-or-namespace):", "")
            
            if st.button("Generate Network Policy YAML"):
                np_yaml = f"""
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: {np_name}
spec:
  podSelector:
    matchLabels:
      {pod_selector}
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - {{"podSelector": {{"matchLabels": {{"app": "myapp"}}}}}}
  egress:
  - to:
    - {{"podSelector": {{"matchLabels": {{"app": "myapp"}}}}}}
"""
                st.code(np_yaml, language="yaml")
                
                if st.button("Apply Network Policy"):
                    result = apply_yaml_content(np_yaml, f"{np_name}-network-policy")
                    st.code(result)
        
        with np_cols[1]:
            st.write("**View Network Policies**")
            if st.button("List Network Policies"):
                np_list = run_kubectl_command("kubectl get networkpolicies --all-namespaces")
                st.code(np_list)

        # Service Mesh
        st.subheader("Service Mesh Integration")
        mesh_cols = st.columns(2)
        
        with mesh_cols[0]:
            st.write("**Install Istio**")
            if st.button("Install Istio"):
                istio_install = run_kubectl_command("curl -L https://istio.io/downloadIstio | sh -")
                st.code(istio_install)
        
        with mesh_cols[1]:
            st.write("**Configure Istio Ingress**")
            gateway_name = st.text_input("Gateway Name:", "my-gateway")
            service_name = st.text_input("Service Name:", "my-service")
            if st.button("Configure Gateway"):
                if gateway_name and service_name:
                    gateway_yaml = f"""
apiVersion: networking.istio.io/v1alpha3
kind: Gateway
metadata:
  name: {gateway_name}
spec:
  selector:
    istio: ingressgateway # use Istio's default gateway implementation
  ports:
  - name: http
    port: 80
    protocol: HTTP
  - name: https
    port: 443
    protocol: HTTPS
---
apiVersion: networking.istio.io/v1alpha3
kind: VirtualService
metadata:
  name: {service_name}
spec:
  hosts:
  - "*"
  gateways:
  - {gateway_name}
  http:
  - match:
    - uri:
        prefix: "/"
    route:
    - destination:
        host: {service_name}
        port:
          number: 80
"""
                    st.code(gateway_yaml, language="yaml")
                    
                    if st.button("Apply Gateway Configuration"):
                        result = apply_yaml_content(gateway_yaml, f"{gateway_name}-gateway")
                        st.code(result)

    elif page == "💾 Storage Management":
        st.header("💾 Storage Management")
        
        # Storage Overview
        st.subheader("Storage Resources")
        storage_cols = st.columns(4)
        
        with storage_cols[0]:
            if st.button("📦 List Persistent Volumes"):
                pvs = run_kubectl_command("kubectl get pv")
                st.code(pvs)
        
        with storage_cols[1]:
            if st.button("📂 List Persistent Volume Claims"):
                pvc = run_kubectl_command("kubectl get pvc --all-namespaces")
                st.code(pvc)
        
        with storage_cols[2]:
            if st.button("🗄️ List Storage Classes"):
                storage_classes = run_kubectl_command("kubectl get storageclass")
                st.code(storage_classes)
        
        with storage_cols[3]:
            if st.button("🔍 Describe Storage Resource"):
                resource_name = st.text_input("Resource Name:", "my-pvc")
                if resource_name:
                    description = run_kubectl_command(f"kubectl describe pvc {resource_name}")
                    st.text_area("Resource Description:", description, height=200)

        # Volume Management
        st.subheader("Volume Management")
        volume_cols = st.columns(2)
        
        with volume_cols[0]:
            st.write("**Create Persistent Volume**")
            pv_name = st.text_input("PV Name:", "my-pv")
            pv_capacity = st.text_input("Capacity (e.g., 10Gi):", "10Gi")
            pv_access_modes = st.selectbox("Access Modes:", ["ReadWriteOnce", "ReadOnlyMany", "ReadWriteMany"])
            pv_reclaim_policy = st.selectbox("Reclaim Policy:", ["Delete", "Retain", "Recycle"])
            
            if st.button("Generate PV YAML"):
                pv_yaml = f"""
apiVersion: v1
kind: PersistentVolume
metadata:
  name: {pv_name}
spec:
  capacity:
    storage: {pv_capacity}
  accessModes:
    - {pv_access_modes}
  persistentVolumeReclaimPolicy: {pv_reclaim_policy}
  hostPath:
    path: "/data/{pv_name}"
"""
                st.code(pv_yaml, language="yaml")
                
                if st.button("Apply PV YAML"):
                    result = apply_yaml_content(pv_yaml, f"{pv_name}-pv")
                    st.code(result)
        
        with volume_cols[1]:
            st.write("**Create Persistent Volume Claim**")
            pvc_name = st.text_input("PVC Name:", "my-pvc")
            pvc_namespace = st.text_input("Namespace:", "default", key="pvc_ns")
            pvc_access_modes = st.selectbox("Access Modes:", ["ReadWriteOnce", "ReadOnlyMany", "ReadWriteMany"], key="pvc_access")
            pvc_resources = st.text_input("Resources (e.g., requests.storage=5Gi):", "requests.storage=5Gi")
            
            if st.button("Generate PVC YAML"):
                pvc_yaml = f"""
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: {pvc_name}
  namespace: {pvc_namespace}
spec:
  accessModes:
    - {pvc_access_modes}
  resources:
    requests:
      {pvc_resources}
"""
                st.code(pvc_yaml, language="yaml")
                
                if st.button("Apply PVC YAML"):
                    result = apply_yaml_content(pvc_yaml, f"{pvc_name}-pvc")
                    st.code(result)

    elif page == "🎛️ Advanced Operations":
        st.header("🎛️ Advanced Kubernetes Operations")
        
        # Node Management
        st.subheader("Node Management")
        node_cols = st.columns(3)
        
        with node_cols[0]:
            if st.button("➕ Add Node"):
                st.write("Feature coming soon.")
        
        with node_cols[1]:
            if st.button("➖ Remove Node"):
                st.write("Feature coming soon.")
        
        with node_cols[2]:
            if st.button("⚙️ Drain Node"):
                node_name = st.text_input("Node Name:", "my-node")
                if node_name and st.button("Drain"):
                    result = run_kubectl_command(f"kubectl drain {node_name} --ignore-daemonsets")
                    st.code(result)

        # Cluster Autoscaler
        st.subheader("Cluster Autoscaler")
        if st.button("Enable Cluster Autoscaler"):
            st.write("Feature coming soon.")

        # Custom Metrics Server
        st.subheader("Custom Metrics Server")
        if st.button("Deploy Metrics Server"):
            metrics_server_yaml = """
apiVersion: apps/v1
kind: Deployment
metadata:
  name: metrics-server
  namespace: kube-system
spec:
  replicas: 1
  selector:
    matchLabels:
      app: metrics-server
  template:
    metadata:
      labels:
        app: metrics-server
    spec:
      containers:
      - name: metrics-server
        image: k8s.gcr.io/metrics-server/metrics-server:v0.4.4
        ports:
        - containerPort: 443
        args:
        - --cert-dir=/tmp
        - --secure-port=443
        - --kubelet-insecure-tls
        - --metric-resolution=15s
"""
            result = apply_yaml_content(metrics_server_yaml, "metrics-server-deployment")
            st.code(result)

    elif page == "📦 Package Management":
        st.header("📦 Kubernetes Package Management")
        
        # Helm Overview
        st.subheader("Helm Package Manager")
        if st.button("Install Helm"):
            helm_install = run_kubectl_command("curl https://raw.githubusercontent.com/helm/helm/master/scripts/get-helm-3 | bash")
            st.code(helm_install)
        
        if st.button("List Helm Releases"):
            releases = run_kubectl_command("helm list --all-namespaces")
            st.code(releases)

        # Sample Helm Chart Deployment
        st.subheader("Deploy Sample Helm Chart")
        if st.button("Deploy WordPress Helm Chart"):
            wordpress_chart = run_kubectl_command("helm repo add bitnami https://charts.bitnami.com/bitnami")
            wordpress_install = run_kubectl_command("helm install my-wordpress bitnami/wordpress --set wordpressUsername=admin,wordpressPassword=admin123")
            st.code(wordpress_chart)
            st.code(wordpress_install)

    elif page == "🔧 Maintenance & Ops":
        st.header("🔧 Kubernetes Maintenance & Operations")
        
        # Backup and Restore
        st.subheader("Backup and Restore")
        if st.button("Backup Cluster"):
            st.write("Feature coming soon.")
        
        if st.button("Restore Cluster"):
            st.write("Feature coming soon.")

        # Upgrade Kubernetes
        st.subheader("Upgrade Kubernetes")
        if st.button("Upgrade to Latest Version"):
            st.write("Feature coming soon.")

        # View Cluster Events
        st.subheader("View Cluster Events")
        if st.button("Get Events"):
            events = run_kubectl_command("kubectl get events --all-namespaces --sort-by=.metadata.creationTimestamp")
            st.code(events)

        # Maintenance Window
        st.subheader("Set Maintenance Window")
        if st.button("Configure Maintenance Window"):
            st.write("Feature coming soon.")