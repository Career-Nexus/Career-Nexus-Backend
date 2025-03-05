import smtplib
import re
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

class Agent():
    def __init__(self,client="smtp.mail.us-east-1.awsapps.com",email="no-reply@career-nexus.com",password="Hhlbbcnofns1$"):
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
            #self.server.starttls()
            self.server.login(self.email,self.password)
            #return self.server
        except smtplib.SMTPAuthenticationError:
            pass
        except Exception:
            pass

    def close_connection(self):
        if self.server:
            self.server.quit()


    def send_email(self,template,subject,container,recipient,attachment=None):
        if not self.server:
            self.warmup()
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
            except:
                print("Email sending Failed")
            finally:
                self.close_connection()
                #print("Connection closed")
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
            except:
                print("Email sending failed")
            finally:
                self.close_connection()






