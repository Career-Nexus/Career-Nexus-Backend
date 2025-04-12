from django.db import models
from users.models import Users


class Project(models.Model):
    user = models.ForeignKey(Users,on_delete=models.CASCADE)
    title = models.CharField(max_length=500)
    description = models.CharField(max_length=2500)
    image = models.CharField(max_length=1000)
