import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import dotenv
def send_email(recipient, subject, body):
    
    dotenv.load_dotenv()
    smtp_server = "smtp.gmail.com"
    port = 587  # TLS port
    sender_email = "rajpurohitabhirajsingh@gmail.com"         # Replace with your email
    password = os.getenv("MAIL_ID_PASSWORD")                  # Replace with your app password (if using Gmail, set up 2FA and generate an app password)
    receiver_email = recipient
    subject = subject
    body = body
    print('done 2')
    # Create the email message
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = receiver_email
    print('done 3')
    # Connect to the SMTP server and send the email
    with smtplib.SMTP(smtp_server, port) as server:
        print('done 4')
        server.starttls()             # Secure the connection using TLS
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())

    return f"email was sent by {sender_email} to {receiver_email} and  subject was {subject}, body was {body}"