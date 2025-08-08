import streamlit as st
import subprocess
import os
from datetime import datetime, timedelta

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

def test_aws_connection(access_key, secret_key, region):
    try:
        env = os.environ.copy()
        env['AWS_ACCESS_KEY_ID'] = access_key
        env['AWS_SECRET_ACCESS_KEY'] = secret_key
        env['AWS_DEFAULT_REGION'] = region
        result = subprocess.run(
            ['aws', 'ec2', 'describe-instances', '--max-items', '1'],
            capture_output=True,
            text=True,
            env=env,
            timeout=30
        )
        return result.returncode == 0
    except:
        return False

def launch_ec2_instance(access_key, secret_key, region, instance_type, ami_id, key_pair, security_group):
    try:
        env = os.environ.copy()
        env['AWS_ACCESS_KEY_ID'] = access_key
        env['AWS_SECRET_ACCESS_KEY'] = secret_key
        env['AWS_DEFAULT_REGION'] = region
        cmd = [
            'aws', 'ec2', 'run-instances',
            '--image-id', ami_id,
            '--count', '1',
            '--instance-type', instance_type,
            '--key-name', key_pair,
            '--security-group-ids', security_group
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, env=env, timeout=60)
        if result.returncode == 0:
            response = json.loads(result.stdout)
            instance_id = response['Instances'][0]['InstanceId']
            return {'success': True, 'instance_id': instance_id}
        else:
            return {'success': False, 'error': result.stderr}
    except Exception as e:
        return {'success': False, 'error': str(e)}

def stop_ec2_instance(access_key, secret_key, region, instance_id):
    try:
        env = os.environ.copy()
        env['AWS_ACCESS_KEY_ID'] = access_key
        env['AWS_SECRET_ACCESS_KEY'] = secret_key
        env['AWS_DEFAULT_REGION'] = region
        result = subprocess.run(
            ['aws', 'ec2', 'stop-instances', '--instance-ids', instance_id],
            capture_output=True,
            text=True,
            env=env,
            timeout=30
        )
        return {'success': result.returncode == 0, 'error': result.stderr if result.returncode != 0 else ''}
    except Exception as e:
        return {'success': False, 'error': str(e)}

def start_ec2_instance(access_key, secret_key, region, instance_id):
    try:
        env = os.environ.copy()
        env['AWS_ACCESS_KEY_ID'] = access_key
        env['AWS_SECRET_ACCESS_KEY'] = secret_key
        env['AWS_DEFAULT_REGION'] = region
        result = subprocess.run(
            ['aws', 'ec2', 'start-instances', '--instance-ids', instance_id],
            capture_output=True,
            text=True,
            env=env,
            timeout=30
        )
        return {
            'success': result.returncode == 0,
            'error': result.stderr if result.returncode != 0 else ''
        }
    except Exception as e:
        return {'success': False, 'error': str(e)}

def list_ec2_instances(access_key, secret_key, region):
    try:
        env = os.environ.copy()
        env['AWS_ACCESS_KEY_ID'] = access_key
        env['AWS_SECRET_ACCESS_KEY'] = secret_key
        env['AWS_DEFAULT_REGION'] = region
        result = subprocess.run(
            ['aws', 'ec2', 'describe-instances', '--query',
             'Reservations[*].Instances[*].[InstanceId,InstanceType,State.Name,LaunchTime]',
             '--output', 'json'],
            capture_output=True,
            text=True,
            env=env,
            timeout=30
        )
        if result.returncode == 0:
            data = json.loads(result.stdout)
            instances = []
            for reservation in data:
                for instance in reservation:
                    instances.append({
                        'InstanceId': instance[0],
                        'InstanceType': instance[1],
                        'State': instance[2],
                        'LaunchTime': instance[3]
                    })
            return instances
        return []
    except:
        return []

def list_s3_buckets(access_key, secret_key, region):
    try:
        env = os.environ.copy()
        env['AWS_ACCESS_KEY_ID'] = access_key
        env['AWS_SECRET_ACCESS_KEY'] = secret_key
        env['AWS_DEFAULT_REGION'] = region
        result = subprocess.run(
            ['aws', 's3api', 'list-buckets', '--query', 'Buckets[*].Name', '--output', 'json'],
            capture_output=True,
            text=True,
            env=env,
            timeout=30
        )
        if result.returncode == 0:
            buckets = json.loads(result.stdout)
            return [{'BucketName': bucket} for bucket in buckets]
        return []
    except:
        return []

def get_cloudwatch_metrics(access_key, secret_key, region, instance_id):
    try:
        env = os.environ.copy()
        env['AWS_ACCESS_KEY_ID'] = access_key
        env['AWS_SECRET_ACCESS_KEY'] = secret_key
        env['AWS_DEFAULT_REGION'] = region
        result = subprocess.run(
            ['aws', 'cloudwatch', 'get-metric-statistics',
             '--namespace', 'AWS/EC2',
             '--metric-name', 'CPUUtilization',
             '--dimensions', f'Name=InstanceId,Value={instance_id}',
             '--start-time', (datetime.now() - timedelta(hours=1)).isoformat(),
             '--end-time', datetime.now().isoformat(),
             '--period', '300',
             '--statistics', 'Average',
             '--output', 'json'],
            capture_output=True,
            text=True,
            env=env,
            timeout=30
        )
        if result.returncode == 0:
            data = json.loads(result.stdout)
            return data.get('Datapoints', [])
        return []
    except:
        return []

def cloud_automation_page():
    st.header("☁️ AWS Cloud Automation")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("AWS Configuration")
        aws_access_key = st.text_input("AWS Access Key ID", type="password")
        aws_secret_key = st.text_input("AWS Secret Access Key", type="password")
        aws_region = st.selectbox("AWS Region", [
            "us-east-1", "us-west-2", "eu-west-1", "ap-southeast-1", "us-east-2"
        ])
        if st.button("🔐 Test AWS Connection"):
            if aws_access_key and aws_secret_key:
                success = test_aws_connection(aws_access_key, aws_secret_key, aws_region)
                if success:
                    st.success("✅ AWS connection successful!")
                else:
                    st.error("❌ AWS connection failed!")
            else:
                st.error("Please provide AWS credentials")
    
    with col2:
        st.subheader("Instance Configuration")
        instance_type = st.selectbox("Instance Type", [
            "t2.micro", "t2.small", "t2.medium", "t3.micro", "t3.small", "t3.medium"
        ])
        ami_id = st.text_input("AMI ID", value="ami-0abcdef1234567890")
        key_pair = st.text_input("Key Pair Name")
        security_group = st.text_input("Security Group ID", value="sg-default")
    
    st.subheader("AWS Operations")
    
    if aws_access_key and aws_secret_key:
        tab1, tab2, tab3 = st.tabs(["EC2 Operations", "S3 Buckets", "CloudWatch Metrics"])
        
        with tab1:
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                if st.button("🚀 Launch Instance"):
                    with st.spinner("Launching EC2 instance..."):
                        result = launch_ec2_instance(
                            aws_access_key, aws_secret_key, aws_region,
                            instance_type, ami_id, key_pair, security_group
                        )
                        if result['success']:
                            st.success(f"✅ Instance launched: {result['instance_id']}")
                        else:
                            st.error(f"❌ Launch failed: {result['error']}")
            with col2:
                instance_id_stop = st.text_input("Instance ID to stop:", key="stop_id")
                if st.button("⏸️ Stop Instance"):
                    if instance_id_stop:
                        result = stop_ec2_instance(aws_access_key, aws_secret_key, aws_region, instance_id_stop)
                        if result['success']:
                            st.success("✅ Instance stopped!")
                        else:
                            st.error(f"❌ Stop failed: {result['error']}")
            with col3:
                instance_id_start = st.text_input("Instance ID to start:", key="start_id")
                if st.button("▶️ Start Instance"):
                    if instance_id_start:
                        result = start_ec2_instance(aws_access_key, aws_secret_key, aws_region, instance_id_start)
                        if result['success']:
                            st.success("✅ Instance started!")
                        else:
                            st.error(f"❌ Start failed: {result['error']}")
            with col4:
                if st.button("🔄 List Instances"):
                    instances = list_ec2_instances(aws_access_key, aws_secret_key, aws_region)
                    if instances:
                        st.dataframe(pd.DataFrame(instances), use_container_width=True)
                    else:
                        st.info("No instances found or error occurred")
        
        with tab2:
            if st.button("🗳️ List S3 Buckets"):
                buckets = list_s3_buckets(aws_access_key, aws_secret_key, aws_region)
                if buckets:
                    st.dataframe(pd.DataFrame(buckets), use_container_width=True)
                else:
                    st.info("No buckets found or error occurred")
        
        with tab3:
            instance_id_metrics = st.text_input("Instance ID for Metrics:", key="metrics_id")
            if st.button("📊 Fetch CloudWatch Metrics"):
                if instance_id_metrics:
                    metrics = get_cloudwatch_metrics(aws_access_key, aws_secret_key, aws_region, instance_id_metrics)
                    if metrics:
                        df = pd.DataFrame(metrics)
                        st.dataframe(df, use_container_width=True)
                    else:
                        st.info("No metrics found or error occurred")
    else:
        st.warning("Please provide AWS credentials to use AWS operations")