from django.db import models
from users.models import Users


class Jobs(models.Model):
    poster = models.ForeignKey(Users,on_delete=models.CASCADE,related_name="poster")
    title = models.CharField(max_length=250)
    organization = models.CharField(max_length=250)
    employment_type = models.CharField(max_length=100)
    work_type = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    salary = models.CharField(max_length=100)
    overview = models.TextField()
    description = models.TextField()
    industry = models.TextField()
    time_stamp = models.DateField(auto_now_add=True)
