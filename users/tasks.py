from celery import shared_task
from .mmail import Agent
from datetime import datetime

@shared_task
def send_email(template,subject,container,recipient,attachment=None):
    agent = Agent()
    if not attachment:
        agent.send_email(template=template,subject=subject,container=container,recipient=recipient)
        print(f"Email sent to {recipient} at time {datetime.now()}")
    else:
        agent.send_email(template=template,subject=subject,container=container,recipient=recipient,attachment=attachment)
        print(f"Email sent to {recipient} at time:{datetime.now()}")
