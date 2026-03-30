from app import celery, app

from celery.schedules import crontab
# from helpers.langchain import train_openai_with_resource
from helpers.gemini_langchain import train_gemini_with_resource
from helpers.upload import remove_upload


import os
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


@celery.task
def send_mail(recipients, subject, text, html):
    sender = os.environ.get('MAIL_USERNAME')
    sender_name = "Enter Sender Full Name"
    receiver = ",".join(recipients)
    password = os.environ.get('MAIL_PASSWORD')
    
    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = f'{sender_name} <{sender}>'
    message["To"] = receiver

    # Turn these into plain/html MIMEText objects
    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(part1)
    message.attach(part2)

    # Create secure connection with server and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(os.environ.get('MAIL_SERVER'), os.environ.get('MAIL_PORT'), context=context) as server:
        server.login(sender, password)
        server.sendmail(
            sender, receiver, message.as_string())
        
# @celery.task
# def train_with_resource_in_background(resource_url, organization_shortcode):
#     # train_openai_with_resource(resource_url, organization_shortcode)
#     train_gemini_with_resource(resource_url, organization_shortcode)
    
@celery.task(bind=True)
def train_with_resource_in_background(self, resource_url, filename, user_id, index_identifier, shortcode_id=None, whatsapp_number_id=None):
    
    try:
        train_gemini_with_resource(resource_url, index_identifier)
        
        from app.files.model import Files
        Files.create(
            name=filename, 
            user_id=user_id, 
            file_url=resource_url,
            shortcode_id=shortcode_id, 
            whatsapp_number_id=whatsapp_number_id
        )
        return {"status": "success"}

    except Exception as e:
        # FALLBACK: Delete from S3/DigitalOcean Spaces if training fails
        print(f"Training failed for {filename}: {str(e)}. Cleaning up storage...")
        
        # Extract the file key from the URL (the last part of the path)
        file_key = resource_url.split('/')[-1]
        remove_upload(file_key)
        
        return {"status": "failed", "error": str(e)}


