import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import requests
import sys

def get_user_email(github_token, username):
    """
    Get the user's email from GitHub API
    """
    headers = {
        'Authorization': f'token {github_token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    
    # Try to get public email first
    response = requests.get(f'https://api.github.com/users/{username}', headers=headers)
    if response.status_code == 200:
        user_data = response.json()
        if user_data.get('email'):
            return user_data['email']
    
    # If no public email, try to get from user's emails (requires user scope)
    response = requests.get('https://api.github.com/user/emails', headers=headers)
    if response.status_code == 200:
        emails = response.json()
        # Get primary email
        for email in emails:
            if email.get('primary', False):
                return email['email']
        # If no primary, get first verified email
        for email in emails:
            if email.get('verified', False):
                return email['email']
    
    return None

def send_email(recipient_email, subject, body, smtp_server, smtp_port, sender_email, sender_password):
    """
    Send email using SMTP
    """
    try:
        # Create message
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = recipient_email
        message["Subject"] = subject
        
        # Add body to email
        message.attach(MIMEText(body, "html"))
        
        # Create SMTP session
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # Enable security
        
        # Send email
        text = message.as_string()
        server.sendmail(sender_email, recipient_email, text)
        server.quit()
        
        print(f"✅ Email sent successfully to {recipient_email}")
        return True
        
    except Exception as e:
        print(f"❌ Error sending email: {str(e)}")
        return False

def main():
    # Get environment variables
    github_token = os.getenv('GITHUB_TOKEN')
    triggered_by = os.getenv('GITHUB_ACTOR')
    repository = os.getenv('GITHUB_REPOSITORY')
    workflow_name = os.getenv('GITHUB_WORKFLOW')
    run_id = os.getenv('GITHUB_RUN_ID')
    
    # Email configuration
    smtp_server = os.getenv('SMTP_SERVER', 'smtp.intel.com')
    smtp_port = int(os.getenv('SMTP_PORT', '25'))
    sender_email = os.getenv('SENDER_EMAIL')
    sender_password = os.getenv('SENDER_PASSWORD')
    
    # Validate required environment variables
    required_vars = {
        'GITHUB_TOKEN': github_token,
        'SENDER_EMAIL': sender_email,
        'SENDER_PASSWORD': sender_password
    }
    
    print(f"🔍 Workflow triggered by: {triggered_by}")
    print(f"📦 Repository: {repository}")
    print(f"⚡ Workflow: {workflow_name}")
    
    # Get user's email
    recipient_email = get_user_email(github_token, triggered_by)
    
    if not recipient_email:
        print(f"❌ Could not retrieve email for user: {triggered_by}")
        print("💡 Make sure the GitHub token has appropriate permissions or the user has a public email")
        sys.exit(1)
    
    print(f"📧 Found email: {recipient_email}")
    
    # Prepare email content
    subject = f"GitHub Actions Workflow Notification - {workflow_name}"
    
    body = f"""
    <html>
        <body>
            <h2>🚀 GitHub Actions Workflow Notification</h2>
            <p>Hello <strong>{triggered_by}</strong>,</p>
            
            <p>Your workflow has been triggered successfully!</p>
            
            <h3>📋 Workflow Details:</h3>
            <ul>
                <li><strong>Repository:</strong> {repository}</li>
                <li><strong>Workflow:</strong> {workflow_name}</li>
                <li><strong>Triggered by:</strong> {triggered_by}</li>
                <li><strong>Run ID:</strong> {run_id}</li>
                <li><strong>Time:</strong> {os.getenv('GITHUB_RUN_ATTEMPT', 'N/A')}</li>
            </ul>
            
            <p>🔗 <a href="https://github.com/{repository}/actions/runs/{run_id}">View workflow run</a></p>
            
            <hr>
            <p><em>This email was sent automatically by GitHub Actions.</em></p>
        </body>
    </html>
    """
    
    # Send email
    success = send_email(
        recipient_email=recipient_email,
        subject=subject,
        body=body,
        smtp_server=smtp_server,
        smtp_port=smtp_port,
        sender_email=sender_email,
        sender_password=sender_password
    )
    
    if success:
        print("✅ Email notification sent successfully!")
    else:
        print("❌ Failed to send email notification")
        sys.exit(1)

if __name__ == "__main__":
    main()