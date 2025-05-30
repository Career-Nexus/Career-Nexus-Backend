from django.urls import path
from . import views

urlpatterns = [
    path("",views.InformationView.as_view(),name="Information"),
    path("country-permit/",views.CountryPermitView.as_view(),name="Permitted-Country"),
]
