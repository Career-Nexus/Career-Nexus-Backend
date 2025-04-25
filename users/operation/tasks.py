from mmail import Agent
#from openpyxl import load_workbook
import json
import time

with open("waitlist.json","r") as file:
    lists = json.load(file)


sent = []
for unit in lists:
    agent = Agent()

    names = unit["name"].split(" ")
    container = {"{NAME}":names[0]}
    email = unit["email"]
    
    agent.send_email("body.html",container=container,subject="Small Delay, Big Promise – Career-Nexus Is Almost Here",recipient=email)

    #logging
    sent.append(unit)
    with open("logs.json","w") as file:
        json.dump(sent,file)
    print(f"SENT TO:{email}")
    time.sleep(2)


#print("Done")
