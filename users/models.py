from django.db import models
from django.contrib.auth.models import AbstractUser

class WaitList(models.Model):
    name = models.CharField(max_length=5000)
    email = models.EmailField(unique=True)
    industry = models.CharField(max_length=5000)
    referral_code = models.CharField(max_length=100)
    invites = models.IntegerField(default=0)
    sub_status = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} with email {self.email} interested in {self.industry}"

class Users(AbstractUser):
    name = models.CharField(max_length=300)
    password2 = models.CharField(max_length=100)
    def __str__(self):
        return f"user with username:{self.username}and email:{self.email}"

class Otp(models.Model):
    otp = models.CharField(max_length=100)
    time_stamp = models.DateTimeField(auto_now_add=True)

