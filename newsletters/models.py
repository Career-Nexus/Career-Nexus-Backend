from django.db import models

from users.models import Users


class NewsletterSubscribers(models.Model):
    subscriber = models.ForeignKey(Users,on_delete=models.CASCADE)
    subscribed_at = models.DateTimeField(auto_now_add=True)

class NewsLetter(models.Model):
    title = models.CharField(max_length=500)
    content = models.TextField()
    image = models.CharField(max_length=500)
    timestamp = models.DateTimeField(auto_now=True)
