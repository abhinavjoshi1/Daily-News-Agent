"""
File name :
Description : 
"""

# ------------------------- Imports -------------------------
import os
from smtplib import SMTP
from dotenv import load_dotenv
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

load_dotenv()

SENDER_EMAIL = os.getenv("SENDER_EMAIL")
RECIPIENT_EMAIL = os.getenv("RECIPIENT_EMAIL")
SUBJECT = "AI News Test Mail"


PASSWORD = os.getenv("EMAIL_PASSWORD")



def send_email(body):
    """
        Sends an email with the given body content.

        Parameters:
        body (str): The message content to be sent in the email.
    """
    msg = MIMEMultipart()
    msg["From"] = SENDER_EMAIL
    msg["To"] = RECIPIENT_EMAIL
    msg["Subject"] = SUBJECT

    msg.attach(MIMEText(body, "plain"))

    try:
        server = SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(SENDER_EMAIL, PASSWORD)
        server.send_message(msg)
        server.quit()
        print("Sent Success.")
    
    except Exception as e:
        print("Error :", e)

