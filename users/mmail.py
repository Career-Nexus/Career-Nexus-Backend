import smtplib
import re
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import time

import os
from dotenv import load_dotenv

load_dotenv()

class Agent():
    def __init__(self,client="smtp.zoho.com",email="info@career-nexus.com",password=os.getenv("GENERAL_PASSWORD")):
        self.client = client
        self.email = email
        self.password = password
        self.message = MIMEMultipart()
        self.message["From"] = email
        self.server = None
        #self.warmup()

    def warmup(self):
        try:
            self.server = smtplib.SMTP_SSL(self.client,465)
            self.server.login(self.email,self.password)
        except smtplib.SMTPAuthenticationError:
            print("Failed to authenticate")
        except Exception:
            print("Warmup failed")

    def close_connection(self):
        if self.server:
            self.server.quit()
            self.server = None

    def check_connection(self,max_retries=3):
        retry = 0
        while retry < max_retries:
            if self.server is None:
                self.warmup()
            elif self.server.sock is None:
                self.server.close()
                self.server = None
                self.warmup()

            if self.server and self.server.sock:
                return True
            else:
                retry += 1 
                print("Trying to reconnect to server")
                time.sleep(2)
        print("Maximum Retries Reached")
        return False



    def send_email(self,template,subject,container,recipient,attachment=None):
        self.check_connection()
        with open(template,"r") as file:
            template = file.read()
        self.message["To"] = recipient
        self.message["Subject"] = subject
        patterns = list(container.keys())
        for pattern in patterns:
            value = container[pattern]
            search_pattern = fr"{pattern}"
            template = re.sub(search_pattern,value,template)
        self.message.attach(MIMEText(template,"html"))

        if attachment == None:
            try:
                self.server.sendmail(self.email,recipient,self.message.as_string())
                return {"Status":"Email Sent"}
            except smtplib.SMTPServerDisconnected:
                print("Server Disconnected. Attempting reconnection....")
                self.check_connection()
                self.server.sendmail(self.email,recipient,self.message.as_string())
                return {"Status":"Email Sent"}
            except:
                print("Failed to send email...")
                return {"Status":"Email sending failed"}
            finally:
                self.close_connection()
        else:
            with open(attachment,"rb") as file:
                part = MIMEBase("application","octet-stream")
                part.set_payload(file.read())
            encoders.encode_base64(part)
            part.add_header("Content-Disposition",f"attachment; filename=Attachment",)
            self.message.attach(part)
            try:
                self.server.sendmail(self.email,recipient,self.message.as_string())
                return {"Status":"Email Sent"}
            except smtplib.SMTPServerDisconnected:
                print("Server Disconnected. Attempting reconnection....")
                self.check_connection()
                self.server.sendmail(self.email,recipient,self.message.as_string())
                return {"Status":"Email Sent"}
            except:
                print("Failed to send email...")
                return {"Status":"Email sending failed"}
            finally:
                self.close_connection()






