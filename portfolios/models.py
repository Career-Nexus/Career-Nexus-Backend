from django.db import models
from users.models import Users



class ProjectCatalogue(models.Model):
    owner = models.ForeignKey(Users,on_delete=models.CASCADE,related_name="catalogue_owner")
    title = models.CharField(max_length=150)
    description = models.TextField()
    image = models.CharField(default="https://careernexus-storage1.s3.amazonaws.com/portfolio/image/6229255a-7c60-4f15-b932-39c525350c86default_portfolio.png")
    download_material = models.CharField(null=True,blank=True)

