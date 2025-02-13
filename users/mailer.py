import yagmail
import os
import re


class Mailer():
	def __init__(self):
		self.yag = yagmail.SMTP(user="saliuoazeez@gmail.com", password="ycgx aqeq moyu umgi ")
		c_directory = os.path.dirname(os.path.abspath(__file__))
		self.logo = os.path.join(c_directory,"logo.jpg")
		self.template = os.path.join(c_directory,"mail.html")

		self.name_pattern = r"{NAME}"
		self.r_patterns = r"{REFERRAL LINK}"

		# self.subject = "Congratulations on Joining Career-Nexus – Your Career Journey Starts Here!"

		with open(self.template,"r",encoding="utf-8") as file:
			self.template = file.read()
	
	def send_waitlist_mail(self,recepient,name,ref_code,head="Congratulations on Joining Career-Nexus – Your Career Journey Starts Here!"):
		body = self.template
		body = re.sub(self.name_pattern,name,body)
		body = re.sub(self.r_patterns,ref_code,body)

		try:
			self.yag.send(to=recepient,contents=body,subject=head,attachments=self.logo)
		except:
			pass
