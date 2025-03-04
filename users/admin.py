from django.contrib import admin
from .models import *

admin.site.site_title = "Career Nexus Admin Panel"  # Change the title shown in the browser tab
admin.site.site_header = "Career Nexus"  # Change the header of the admin interface
admin.site.index_title = "Welcome to the Admin Dashboard"
# Register your models here.
models = [WaitList,Users,Otp]
for model in models:
    admin.site.register(model)
