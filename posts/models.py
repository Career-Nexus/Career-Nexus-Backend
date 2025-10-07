from django.db import models
from users.models import PersonalProfile,Users


# Create your models here.
class Posts(models.Model):
    profile = models.ForeignKey(PersonalProfile,on_delete=models.CASCADE)
    body = models.CharField(max_length=10000,blank=True)
    pic1 = models.CharField(max_length=500,default="N/A")
    pic2 = models.CharField(max_length=500,default="N/A")
    pic3 = models.CharField(max_length=500,default="N/A")
    video = models.CharField(max_length=500,default="N/A")
    #media = models.CharField(max_length=500,default="N/A")
    article = models.CharField(max_length=500,default="N/A")
    time_stamp = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey("self",null=True,blank=True,on_delete=models.CASCADE,related_name="mainpost")
    industries = models.TextField(null=True,blank=True)

class Comment(models.Model):
    post = models.ForeignKey(Posts,on_delete=models.CASCADE)
    user = models.ForeignKey(Users,on_delete=models.CASCADE)
    body = models.CharField(max_length=5000)
    media = models.CharField(max_length=500,default="N/A")
    parent = models.ForeignKey("self",null=True,blank=True,on_delete=models.CASCADE,related_name="replies")
    time_stamp = models.DateTimeField(auto_now_add=True)

#POST LIKE TABLE
class Like(models.Model):
    post = models.ForeignKey(Posts,on_delete=models.CASCADE)
    user = models.ForeignKey(Users,on_delete=models.CASCADE)

#COMMENT/REPLY LIKE TABLE
class CommentLike(models.Model):
    user = models.ForeignKey(Users,on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment,on_delete=models.CASCADE)

class Share(models.Model):
    post = models.ForeignKey(Posts,on_delete=models.CASCADE)
    user = models.ForeignKey(Users,on_delete=models.CASCADE)
    hash = models.CharField()

class PostSave(models.Model):
    user = models.ForeignKey(Users,on_delete=models.CASCADE)
    post = models.ForeignKey(Posts,on_delete=models.CASCADE)
