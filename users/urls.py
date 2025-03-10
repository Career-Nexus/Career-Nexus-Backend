from django.urls import path
from . import views


urlpatterns = [
	# path("",views.TestView.as_view(),name="Test-view"),
	path("join/",views.WaitListView.as_view(),name="Add-waitlist"),
	path("signup/",views.RegisterView.as_view(),name="User_Register"),
    path("signin/",views.LoginView.as_view(),name="User Login"),
    path("signout/",views.LogoutView.as_view(), name="User Logout"),
	path("subscribe/",views.NewsLetterSubscribeView.as_view(), name="News-Letter-Subscribe"),
	path("unsubscribe/",views.NewsLetterUnsubscribeView.as_view(), name="News-Letter-Unsubscribe"),
	path("delete/",views.DeleteWaitListView.as_view(),name="Delete-Waitlist"),
]
