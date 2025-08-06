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
    user_type = models.CharField(max_length=20,default="learner")
    industry = models.CharField(max_length=100,default="others")
    change_password = models.BooleanField(default=False)
    request_time = models.DateTimeField(auto_now_add=True)

    #Settings Specific Fields
    email_notify = models.BooleanField(default=False)
    push_notify = models.BooleanField(default=True)
    message_notify = models.BooleanField(default=False)
    weekly_summary = models.BooleanField(default=False)
    job_alerts = models.BooleanField(default=True)
    marketing = models.BooleanField(default=False)
    show_email = models.BooleanField(default=True)
    show_activity = models.BooleanField(default=False)
    show_location = models.BooleanField(default=False)



    def __str__(self):
        return f"{self.email}|{self.profile.profile_photo}"
        
class Otp(models.Model):
    otp = models.CharField(max_length=100)
    hash = models.CharField(max_length=300)
    email = models.CharField(max_length=150,null=True)
    username = models.CharField(max_length=200,null=True)
    password = models.CharField(max_length=150,null=True)
    time_stamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.otp} created at {self.time_stamp}"


# USER PROFILE MODELS --------------------------------------------

class PersonalProfile(models.Model):
    #General profile properties
    user = models.OneToOneField(Users,on_delete=models.CASCADE,related_name="profile",primary_key=True)
    first_name = models.CharField(max_length=200,default="N/A")
    last_name = models.CharField(max_length=200,default="N/A")
    middle_name = models.CharField(max_length=200,default="N/A")
    profile_photo = models.CharField(max_length=3000,default='https://careernexus-storage1.s3.amazonaws.com/profile_pictures/4aaed37c-eb8b-400d-a73a-82574dccfb88default_pp.jpeg')
    cover_photo = models.CharField(max_length=300,default='https://careernexus-storage1.s3.amazonaws.com/cover_photos/70114098-5014-4eda-a725-5421792972dadefault_cp.jpeg')
    qualification = models.CharField(max_length=3000,default='')
    position = models.CharField(max_length=1000,default='')
    country_code = models.CharField(max_length=20,default="+000")
    phone_number = models.CharField(max_length=30,default="00000000000")
    location = models.CharField(max_length=1000,default='')
    bio = models.CharField(max_length=4000,default='')
    intro_video = models.CharField(max_length=300,default='')
    summary = models.CharField(max_length=5000,default='')
    resume = models.CharField(max_length=5000,default='')
    #Extra properties for mentors
    years_of_experience = models.IntegerField(null=True,blank=True)
    availability = models.CharField(null=True,blank=True)
    current_job = models.CharField(null=True,blank=True)
    areas_of_expertise = models.JSONField(default=list)
    technical_skills = models.JSONField(default=list)
    mentorship_styles = models.JSONField(default=list)
    timezone = models.CharField(default="UTC")
    linkedin_url = models.CharField(null=True,blank=True)
    
    #Ensuring that the user id is always the same as profile id
    @property
    def id(self):
        return self.user_id



class ProfileView(models.Model):
    viewer = models.ForeignKey(Users,on_delete=models.CASCADE,related_name="viewer")
    viewed = models.ForeignKey(Users,on_delete=models.CASCADE,related_name="viewed")
    date = models.DateField(auto_now_add=True)

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
