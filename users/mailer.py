import yagmail


class Mailer():
	def __init__(self):
		self.yag = yagmail.SMTP(user="saliuoazeez@gmail.com", password="ycgx aqeq moyu umgi ")
	
	def waitlist_mail(self,recepient,message,head="Congratulations on Joining CareerNexus"):
		try:
			self.yag.send(to=recepient,contents=message,subject=head)
		except:
			pass