from django.db import models
from users.models import PersonalProfile,Users


# Create your models here.
class Posts(models.Model):
    profile = models.ForeignKey(PersonalProfile,on_delete=models.CASCADE)
    body = models.CharField(max_length=10000,blank=True)
    media = models.CharField(max_length=500,default="N/A")
    article = models.CharField(max_length=500,default="N/A")
    time_stamp = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey("self",null=True,blank=True,on_delete=models.CASCADE,related_name="mainpost")
    industries = models.TextField(null=True,blank=True)

class Comment(models.Model):
    post = models.ForeignKey(Posts,on_delete=models.CASCADE)
    user = models.ForeignKey(Users,on_delete=models.CASCADE)
    body = models.CharField(max_length=5000)
    parent = models.ForeignKey("self",null=True,blank=True,on_delete=models.CASCADE,related_name="replies")
    time_stamp = models.DateTimeField(auto_now_add=True)

class Like(models.Model):
    post = models.ForeignKey(Posts,on_delete=models.CASCADE)
    user = models.ForeignKey(Users,on_delete=models.CASCADE)

class Share(models.Model):
    post = models.ForeignKey(Posts,on_delete=models.CASCADE)
    user = models.ForeignKey(Users,on_delete=models.CASCADE)

class PostSave(models.Model):
    user = models.ForeignKey(Users,on_delete=models.CASCADE)
    post = models.ForeignKey(Posts,on_delete=models.CASCADE)
