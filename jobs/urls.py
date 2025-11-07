from django.conf.urls import handler400
from django.urls import path
from . import views

urlpatterns = [
    path("",views.JobsView.as_view(),name="Jobs"),
    path("recommend/",views.RecommendJobView.as_view(),name="Recommend-Jobs"),
    path("preference/",views.JobPreferenceView.as_view(),name="Job-Preference"),
    path("save/",views.SaveJobView.as_view(),name="Save-Job"),
    path("unsave/",views.UnsaveJobView.as_view(),name="Unsave-Job"),
    path("status/update/",views.JobStatusUpdateView.as_view(),name="Update-Job-Status"),
    path("apply/",views.JobApplicationView.as_view(),name="Apply-For-Job"),
    path("application/",views.RetrieveJobApplicationView.as_view(),name="View-Job_applications"),
    path("application/recent/",views.RetrieveRecentJobApplicationsView.as_view(),name="Retrieve-Recent-Job-Applications"),
]

