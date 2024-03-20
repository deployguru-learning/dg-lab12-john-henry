from flask import Flask, jsonify
import boto3
import requests

# Initialize Boto3 client
ec2_client = boto3.client('ec2', region_name='ap-south-1')

# Define authorized email addresses
AUTHORIZED_EMAILS = ['henryowino517@gmail.com', 'hjowino@gmal.com.com']

app = Flask(__name__)

# Function to list EC2 instances
def list_instances():
    """
    Retrieve information about EC2 instances.
    """
    try:
        response = ec2_client.describe_instances()
        instances = []
        for reservation in response['Reservations']:
            for instance in reservation['Instances']:
                instances.append({
                    'InstanceId': instance['InstanceId'],
                    'LaunchTime': instance['LaunchTime']
                })
        return instances
    except Exception as e:
        print(f"Error in list_instances(): {e}")
        return []

# Function to verify email
def verify_email(email):
    """
    Verify if the email address is authorized.
    """
    return email in AUTHORIZED_EMAILS

# Function to monitor EC2 instance launches
def monitor_ec2_instance_launches():
    """
    Monitor EC2 instance launches and verify authorized users.
    """
    try:
        instances = list_instances()
        output = []
        for instance in instances:
            email = AUTHORIZED_EMAILS  # Replace with actual email obtained from instance details
            if verify_email(email):
                # Authorized user launched an EC2 instance
                output.append({
                    'status': 'Authorized',
                    'user_email': email,
                    'instance_id': instance['InstanceId'],
                    'launch_time': instance['LaunchTime']
                })
            else:
                # Unauthorized user attempted to launch an EC2 instance
                output.append({
                    'status': 'Unauthorized',
                    'user_email': email,
                    'instance_id': instance['InstanceId'],
                    'launch_time': instance['LaunchTime']
                })
        return output
    except Exception as e:
        print(f"Error in monitor_ec2_instance_launches(): {e}")
        return []

# Route to display EC2 instance launches in JSON format
@app.route('/')
def display_instance_launches():
    output = monitor_ec2_instance_launches()
    return jsonify(output)

if __name__ == "__main__":
    app.run(debug=True)
