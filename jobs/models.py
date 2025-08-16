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
    experience_level = models.CharField(max_length=20)
    time_stamp = models.DateField(auto_now_add=True)

class JobPreference(models.Model):
    user = models.OneToOneField(Users,on_delete=models.CASCADE)
    title = models.CharField(max_length=250,null=True)
    employment_type = models.CharField(max_length=20,null=True)
    work_type = models.CharField(max_length=10,null=True)
    industry = models.CharField(max_length=150,null=True)
    experience_level = models.CharField(max_length=15,null=True)



class JobPreferenceSuffix(models.Model):
    ref_no = models.CharField(max_length=99)
    preference_combination = models.CharField(max_length=500)



class SavedJobs(models.Model):
    saver = models.ForeignKey(Users,on_delete=models.CASCADE,related_name="job_saver")
    job = models.ForeignKey(Jobs,on_delete=models.CASCADE)
    saved_at = models.DateTimeField(auto_now=True)
