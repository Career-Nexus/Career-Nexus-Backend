from django.db import models
from users.models import Users

class Chatroom(models.Model):
    initiator = models.ForeignKey(Users,on_delete=models.CASCADE,related_name="user1")
    contributor = models.ForeignKey(Users,on_delete=models.CASCADE,related_name="user2")
    created = models.DateTimeField(auto_now=True)

class Message(models.Model):
    room = models.ForeignKey(Chatroom,on_delete=models.CASCADE)
    person = models.ForeignKey(Users,on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

class Notification(models.Model):
    user = models.ForeignKey(Users,on_delete=models.CASCADE)
    text = models.CharField(max_length=1500)
    page = models.CharField(max_length=100,null=True)
    route = models.CharField(max_length=200,null=True)
    obj_id = models.CharField(null=True)
    timestamp = models.DateTimeField(auto_now=True)
