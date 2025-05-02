from django.db import models
from users.models import Users


class Connection(models.Model):
    user = models.ForeignKey(Users,on_delete=models.CASCADE,related_name="connection_user")
    connection = models.ForeignKey(Users,on_delete=models.CASCADE,related_name="connect")
    status = models.CharField(max_length=20)

