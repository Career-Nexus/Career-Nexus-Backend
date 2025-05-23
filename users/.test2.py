import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# AWS SES SMTP endpoint (you should use the correct endpoint for your region)
smtp_server = "smtp.mail.us-east-1.awsapps.com"  # Change this to the appropriate region
smtp_port = 465  # Typically 587 for TLS
smtp_username = "no-reply@career-nexus.com"  # Replace with your SMTP username
smtp_password = "Hhlbbcnofns1$"  # Replace with your SMTP password

# Sender and recipient information
sender_email = "no-reply@career-nexus.com"
receiver_email = "saliuoazeez@gmail.com"
subject = "Test Email from AWS SES using smtplib"
body = "Hello, this is a test email sent using AWS SES with Python smtplib."

# Create the email 
msg = MIMEMultipart()
msg['From'] = sender_email
msg['To'] = receiver_email
msg['Subject'] = subject
msg.attach(MIMEText(body, 'plain'))

# Send the email
try:
    with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
        #server.starttls()  # Encrypts the connection
        server.login(smtp_username, smtp_password)  # Log in to the server
        text = msg.as_string()  # Convert the message to a string
        server.sendmail(sender_email, receiver_email, text)  # Send the email
        print("Email sent successfully!")
except Exception as e:
    print(f"Error: {e}")

