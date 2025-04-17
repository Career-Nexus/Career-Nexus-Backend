from django.db import models
from users.models import Users


class Project(models.Model):
    user = models.ForeignKey(Users,on_delete=models.CASCADE)
    cover_image = models.CharField(max_length=1000)
    title = models.CharField(max_length=500)
    description = models.CharField(max_length=2500)
    role = models.CharField(max_length=500)
    tools = models.CharField(max_length=1000)
    image = models.CharField(max_length=1000)
