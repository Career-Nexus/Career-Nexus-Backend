from django.db import models
from users.models import Users


class UserFollow(models.Model):
    user_follower = models.ForeignKey(Users,on_delete=models.CASCADE,related_name="follower")
    user_following = models.ForeignKey(Users,on_delete=models.CASCADE,related_name="following")
