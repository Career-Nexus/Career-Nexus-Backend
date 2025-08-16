from django.urls import path
from . import views

urlpatterns = [
    path("",views.InformationView.as_view(),name="Information"),
    path("country-permit/",views.CountryPermitView.as_view(),name="Permitted-Country"),
    path("choice-data/",views.ChoiceFieldView.as_view(),name="Choice-Data"),
    path("library/",views.LibraryView.as_view(),name="Library"),
]
