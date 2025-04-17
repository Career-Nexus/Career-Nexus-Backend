from django.db import models
from django.contrib.auth.models import AbstractUser

from django.contrib.auth import get_user_model

#UserModel = get_user_model()


# User Registration and authentication models ----------------------------

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
    user_type = models.CharField(max_length=20,default="")
    name = models.CharField(max_length=300)
    #password2 = models.CharField(max_length=100)
    industry = models.CharField(max_length=100,default="")

    def __str__(self):
        return f"{self.name}|{self.profile.profile_photo}"
        
class Otp(models.Model):
    otp = models.CharField(max_length=100)
    time_stamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.otp} created at {self.time_stamp}"


# USER PROFILE MODELS --------------------------------------------

class PersonalProfile(models.Model):
    user = models.OneToOneField(Users,on_delete=models.CASCADE,related_name="profile")
    name = models.CharField(max_length=250)
    profile_photo = models.CharField(max_length=300,default='')
    qualification = models.CharField(max_length=3000,default='')
    position = models.CharField(max_length=1000,default='')
    location = models.CharField(max_length=1000,default='')
    bio = models.CharField(max_length=4000,default='')
    intro_video = models.CharField(max_length=300,default='')
    summary = models.CharField(max_length=5000,default='')

class experience(models.Model):
    user = models.ForeignKey(Users,on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    organization = models.CharField(max_length=500)
    start_date = models.CharField(max_length=20)
    end_date = models.CharField(max_length=20)
    location = models.CharField(max_length=256)
    employment_type = models.CharField(max_length=50)
    detail = models.CharField(max_length=2000)

class education(models.Model):
    user = models.ForeignKey(Users,on_delete=models.CASCADE)
    course = models.CharField(max_length=200)
    school = models.CharField(max_length=250)
    start_date = models.CharField(max_length=20)
    end_date = models.CharField(max_length=20)
    location = models.CharField(max_length=200)
    detail = models.CharField(max_length=2000)

class certification(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    title = models.CharField(max_length=256)
    school = models.CharField(max_length=200)
    issue_date = models.CharField(max_length=20)
    cert_id = models.CharField(max_length=1000)
    skills = models.CharField(max_length=1000)










class Test(models.Model):
    file = models.CharField(max_length=256)
