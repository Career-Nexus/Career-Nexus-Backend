from django.urls import path
from . import views

urlpatterns = [
    path("recommendation/",views.MentorRecommendationView.as_view(),name="Mentor-Recommendation"),
    path("search/",views.MentorSearchAndFilterView.as_view(),name="Mentor-Search_and_filter"),


    path("test/",views.TestView.as_view(),name="Test-View"),
]
