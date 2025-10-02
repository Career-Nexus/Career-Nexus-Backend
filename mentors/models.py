from django.db import models
from users.models import Users


VAULT_TRANSACTION_CHOICES = (
    ("EARN","EARN"),
    ("WITHDRAW","WITHDRAW")
)


class Sessions(models.Model):
    mentor = models.ForeignKey(Users,on_delete=models.CASCADE,related_name="mentor")
    mentee = models.ForeignKey(Users,on_delete=models.CASCADE,related_name="mentee")
    session_type = models.CharField(max_length=20)
    room_name = models.CharField()
    session_at = models.DateTimeField()
    discourse = models.TextField()
    rating = models.IntegerField(default=0)
    status = models.CharField(max_length=20,default="PENDING")
    is_paid = models.BooleanField(default=False)


class SavedMentors(models.Model):
    saver = models.ForeignKey(Users,on_delete=models.CASCADE,related_name="mentor_saver")
    saved = models.ForeignKey(Users,on_delete=models.CASCADE,related_name="mentor_saved")

class MentorRating(models.Model):
    mentor = models.OneToOneField(Users,on_delete=models.CASCADE,related_name="rating")
    ratings = models.JSONField(default=list)

class MentorVault(models.Model):
    mentor = models.OneToOneField(Users,on_delete=models.CASCADE,related_name="vault")
    amount = models.DecimalField(default=0.00,decimal_places=2,max_digits=10)
    last_updated = models.DateTimeField(auto_now_add=True)

class VaultTransactions(models.Model):
    mentor = models.ForeignKey(Users,on_delete=models.CASCADE,related_name="vault_transactions")
    action = models.CharField(max_length=20,choices=VAULT_TRANSACTION_CHOICES)
    amount = models.DecimalField(decimal_places=2,max_digits=10)
    extra_data = models.JSONField(default=dict)
    timestamp = models.DateTimeField(auto_now=True)
