from django.urls import path
from . import views


urlpatterns = [
	path("",views.TestView.as_view(),name="Test-view"),
	path("join/",views.WaitListView.as_view(),name="Add-waitlist"),
	path("register/",views.RegisterView.as_view(),name="User_Register")
]