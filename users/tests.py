from mmail import Agent

agent = Agent("smtp.zoho.com","info@career-nexus.com","ExcWFp4JeJKd")

output =agent.send_email("mail.html","Testing New Config",{"{NAME}":"Opeyemi","{REFERRAL LINK}":"12345","{EMAIL}":"info@career-nexus.com"},recipient="saliuoazeez@gmail.com",attachment="career-nexus_logo.png")

print(output)
