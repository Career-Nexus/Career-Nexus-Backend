from django.db import models


class Information(models.Model):
    title = models.CharField(max_length=200,unique=True)
    content = models.TextField(null=True)
    items = models.TextField(null=True)
    updated_at = models.DateField(auto_now=True)


class Countrycodes(models.Model):
    country = models.CharField(max_length=1000)
    code = models.CharField(max_length=20)
    permitted = models.BooleanField(default=True)

