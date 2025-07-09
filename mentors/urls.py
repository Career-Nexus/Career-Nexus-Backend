from django.urls import path
from . import views

urlpatterns = [
    path("recommendation/",views.MentorRecommendationView.as_view(),name="Mentor-Recommendation"),

    path("test/",views.TestView.as_view(),name="Test-View"),
]
