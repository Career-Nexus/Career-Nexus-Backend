from django.urls import path
from . import views

urlpatterns = [
    path("",views.JobsView.as_view(),name="Jobs"),
    path("recommend/",views.RecommendJobView.as_view(),name="Recommend-Jobs"),
    path("preference/",views.JobPreferenceView.as_view(),name="Job-Preference"),
    path("save/",views.SaveJobView.as_view(),name="Save-Job"),
    path("unsave/",views.UnsaveJobView.as_view(),name="Unsave-Job"),
]
