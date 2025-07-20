from django.db import models
from users.models import Users



class Sessions(models.Model):
    mentor = models.ForeignKey(Users,on_delete=models.CASCADE,related_name="mentor")
    mentee = models.ForeignKey(Users,on_delete=models.CASCADE,related_name="mentee")
    session_type = models.CharField(max_length=20)
    session_at = models.DateTimeField()
    discourse = models.TextField()
    status = models.CharField(max_length=20,default="PENDING")
