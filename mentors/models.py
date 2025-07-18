from django.db import models
from users.models import Users



class Sessions(models.Model):
    mentor = models.ForeignKey(Users,on_delete=models.CASCADE,related_name="mentor")
    mentee = models.ForeignKey(Users,on_delete=models.CASCADE,related_name="mentee")
    session_type = models.CharField(max_length=20)
    mentee_date = models.DateField()
    mentee_time = models.TimeField()
    mentor_date = models.DateField()
    mentor_time = models.TimeField()
    discourse = models.TextField()
