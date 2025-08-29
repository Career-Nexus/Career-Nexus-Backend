from django.urls import path
from . import views

urlpatterns = [
    path("recommendation/",views.MentorRecommendationView.as_view(),name="Mentor-Recommendation"),
    path("search/",views.MentorSearchAndFilterView.as_view(),name="Mentor-Search_and_filter"),
    path("sessions/book/",views.CreateMentorshipSessionView.as_view(),name="Book-Mentorship-Session"),
    path("sessions/",views.RetrieveMentorshipSessionsView.as_view(),name="Retrieve-Requested-Accepted-mentorship-sessions"),
    path("sessions/accept-reject/",views.AcceptRejectMentorshipSessionsView.as_view(),name="Accept-Reject-Sessions"),
    path("save/",views.SaveMentorView.as_view(),name="Save-Mentor"),
    path("annotate/",views.AnnotateMentorshipSessionView.as_view(),name="Annotate-Sessions"),
    path("session/cancel/",views.CancelSessionView.as_view(),name="Cancel-Session"),
    path("session/join/",views.JoinSessionView.as_view(),name="Join-Session"),


    path("test/",views.TestView.as_view(),name="Test-View"),
]
