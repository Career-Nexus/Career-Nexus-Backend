from django.urls import path
from . import views

urlpatterns = [
    path("",views.JobsView.as_view(),name="Jobs"),
    path("recommend/",views.RecommendJobView.as_view(),name="Recommend-Jobs"),
]
