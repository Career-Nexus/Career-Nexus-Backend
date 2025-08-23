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


class Library(models.Model):
    title = models.CharField(max_length=250)
    description = models.TextField()
    tags = models.JSONField()
    file = models.CharField()

class ExchangeRate(models.Model):
    country = models.ForeignKey(Countrycodes,on_delete=models.CASCADE)
    currency_name = models.CharField()
    currency_initials = models.CharField()
    exchange_rate = models.DecimalField(max_digits=10,decimal_places=2)
