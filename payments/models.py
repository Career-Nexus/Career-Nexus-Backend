from django.db import models

from users.models import Users
from mentors.models import Sessions


transaction_statuses = (
    ("pending","pending"),
    ("successful","successful")
)



class SessionTransactions(models.Model):
    transaction_id = models.CharField()
    session = models.ForeignKey(Sessions,on_delete=models.CASCADE)
    initiator = models.ForeignKey(Users,on_delete=models.CASCADE,related_name="transaction_initiator")
    mentor = models.ForeignKey(Users,on_delete=models.CASCADE,related_name="concerned_mentor")
    amount = models.IntegerField()
    currency = models.CharField()
    status = models.CharField(choices=transaction_statuses)
    initiated_at = models.DateTimeField(auto_now=True)



class TransactionCallbacks(models.Model):
    tx_ref = models.CharField()
    transaction_id = models.CharField()


class StripeTransactions(models.Model):
    transaction_id = models.CharField()
    session = models.ForeignKey(Sessions,on_delete=models.CASCADE)
    initiator = models.ForeignKey(Users,on_delete=models.CASCADE)
    amount = models.IntegerField()
    status = models.CharField(choices=transaction_statuses,default="pending")
    initiated_at = models.DateTimeField(auto_now=True)
