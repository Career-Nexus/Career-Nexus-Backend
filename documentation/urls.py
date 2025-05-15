from django.urls import path
from . import views

urlpatterns=[
    path("",views.ShowDocumentation,name="Show-Documentation"),
]
