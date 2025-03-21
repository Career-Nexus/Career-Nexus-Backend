from django.db import models
from users.models import PersonalProfile


# Create your models here.
class Posts(models.Model):
    profile = models.ForeignKey(PersonalProfile,on_delete=models.CASCADE)
    body = models.CharField(max_length=10000)
    media = models.CharField(max_length=500,default="N/A")
    article = models.CharField(max_length=500,default="N/A")
    time_stamp = models.DateTimeField(auto_now_add=True)
