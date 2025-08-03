from django.urls import path
from . import views


urlpatterns = [
    path("subscribe/",views.SubscribeView.as_view(),name="Subscribe-to-Newsletter"),
    path("unsubscribe/",views.UnsubscribeView.as_view(),name="Unsubscribe-from-Newsletter"),
    path("create/",views.CreateNewsLetterView.as_view(),name="Create-Newsletter"),
    path("",views.RetrieveNewsLetterView.as_view(),name="Retrieve-NewsLetter"),


    path("test/",views.TestView.as_view(),name="Test"),
]
