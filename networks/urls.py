from django.urls import path
from . import views

urlpatterns = [
    path("",views.ConnectionView.as_view(),name="Connection"),
    path("status/",views.ConnectionStatusView.as_view(),name="Connection-status"),
    path("pending/",views.ConnectionPendingView.as_view(),name="Pending-connections"),
    path("requests/",views.ConnectionRequestSentView.as_view(),name="Sent-Requests"),
    path("recommendation/",views.ConnectionRecommendationView.as_view(),name="Connection-recommendation"),
    path("count/",views.ConnectionsCountView.as_view(),name="Connection_count")
]
