from django.urls import path
from . import views


urlpatterns = [
    path("",views.ProjectCatalogueView.as_view(),name="Project-Catalogue"),
]
