from django.db import models
from users.models import Users



class Sessions(models.Model):
    mentor = models.ForeignKey(Users,on_delete=models.CASCADE,related_name="mentor")
    mentee = models.ForeignKey(Users,on_delete=models.CASCADE,related_name="mentee")
    session_type = models.CharField(max_length=20)
    room_name = models.CharField()
    session_at = models.DateTimeField()
    discourse = models.TextField()
    status = models.CharField(max_length=20,default="PENDING")
    is_paid = models.BooleanField(default=False)


class SavedMentors(models.Model):
    saver = models.ForeignKey(Users,on_delete=models.CASCADE,related_name="mentor_saver")
    saved = models.ForeignKey(Users,on_delete=models.CASCADE,related_name="mentor_saved")

class MentorRating(models.Model):
    mentor = models.OneToOneField(Users,on_delete=models.CASCADE,related_name="rating")
    ratings = models.JSONField(default=list)
