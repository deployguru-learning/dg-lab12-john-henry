import shutil
import os
from datetime import datetime
import requests
import json

def create_backup(source_folder, destination_folder, webhook_url):
    # Create a unique name for the backup folder based on the current date and time
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_folder = os.path.join(destination_folder, f'backup_{timestamp}')

    try:
        # Check if the backup folder already exists
        if os.path.exists(backup_folder):
            raise FileExistsError(f"Backup folder '{backup_folder}' already exists.")

        # # Create the backup folder
        # os.makedirs(backup_folder)

        # Perform the backup using shutil
        shutil.copytree(source_folder, backup_folder)
        print(f"Backup successfully created at: {backup_folder}")

        # Send Slack notification
        message_text = "Backup process completed successfully!"
        send_slack_notification(webhook_url, message_text)

    except Exception as e:
        print(f"Error creating backup: {e}")
        

def send_slack_notification(webhook_url, message_text):
    slack_url = webhook_url
    sender_name="henry"
    file_name="backup_file"
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    attachment = {
        'fallback': f"{sender_name} backed up {file_name} at {timestamp}",
        'color': '#36a64f',  # You can customize the color
        'pretext': f"{sender_name} backed up a file",
        'title': f"Backup Information",
        'text': f"Backup Time: {timestamp}\nFile Name: {file_name}",
        'footer': 'Backup Bot',
        'ts': int(datetime.now().timestamp())
    }
    payload = {
        'text': message_text,
        'username': sender_name,
        'icon_emoji': ':robot_face:',
        'attachments': [attachment]
    }

    try:
        response = requests.post(slack_url, data=json.dumps(payload), headers={'Content-Type': 'application/json'})
        if response.status_code == 200:
            print("Slack notification sent successfully.")
        else:
            print(f"Error sending Slack notification. Status code: {response.status_code}")
    except Exception as e:
        print(f"Error sending Slack notification: {e}")

if __name__ == "__main__":
    source_folder = '/var/www/html'
    destination_folder = '/opt/new/'
    webhook_url = 'https://hooks.slack.com/services/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'

    create_backup(source_folder, destination_folder, webhook_url)