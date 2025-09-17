from django.urls import path
from . import views
from rest_framework.permissions import AllowAny

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
        openapi.Info(
            title="Career Nexus Documentation",
            description="Documentation for Career Nexus APIs. This documentation covers all the API systems supporting the frontend architecture.",
            default_version="v1",
            terms_of_service="",
            contact=openapi.Contact(email="saliuoazeez@gmail.com"),
            #license=openapi.License(name="BSD License"),
            ),
        public=True,
        permission_classes=(AllowAny,)
        )

urlpatterns = [
    path("docs/",schema_view.with_ui("swagger", cache_timeout=0), name="User API Documentation"),

	# path("",views.TestView.as_view(),name="Test-view"),
	path("join/",views.WaitListView.as_view(),name="Add-waitlist"),
	path("signup/",views.RegisterView.as_view(),name="User_Register"),
    path("corporate/signup/",views.CreateCorporateAccountView.as_view(),name="Corporate-User-Register"),
    path("linked-accounts/",views.LinkedAccountsView.as_view(),name="Linked-Accounts"),

    path("hash/verify/",views.VerifyHashView.as_view(),name="Verify-hash"),
    path("signin/",views.LoginView.as_view(),name="User Login"),
    path("signout/",views.LogoutView.as_view(), name="User Logout"),
    path("forget-password/",views.ForgetPasswordView.as_view(),name="Forget Password"),

	path("subscribe/",views.NewsLetterSubscribeView.as_view(), name="News-Letter-Subscribe"),
	path("unsubscribe/",views.NewsLetterUnsubscribeView.as_view(), name="News-Letter-Unsubscribe"),
	path("delete/",views.DeleteUserView.as_view(),name="Delete-Waitlist"),
    #path('upload/',views.TestView.as_view(),name="Test-view"),
    path('profile-update/',views.PersonalProfileView.as_view(),name="Update-Personal-profile"),
    path('experience/',views.ExperienceView.as_view(),name="Add-and-view-experience"),
    path('update-experience/',views.UpdateExperienceView.as_view(),name="update-experience"),
    path('education/', views.EducationView.as_view(), name="Add-view-update-delete-education"),
    path("certification/", views.CertificationView.as_view(), name="Add-View-Delete-Certification"),
    path("retrieve-profile/",views.RetreiveProfileView.as_view(), name="Retrieve-Profile"),
    path("analytics/",views.AnalyticsView.as_view(),name="User-Analytics"),
    path("completion/",views.WizardView.as_view(),name="wizard-view"),
    path("settings/",views.SettingsView.as_view(),name="Settings-View"),
    path("search/",views.UserSearchView.as_view(),name="User-Search-View"),
    path("google/signup/",views.GoogleSignupView.as_view(),name="Google-Signup"),
    path("google/signin/",views.GoogleSignInView.as_view(),name="Google-signin"),
    path("disputes/", views.DisputeTicketsView.as_view(),name="Dispute-View"),
    path("admin/disputes/",views.AdminDisputeTicketView.as_view(),name="Admin-Dispute-View"),
    path("admin/disputes/summary/",views.DisputeRetrieveSummaryView.as_view(),name="Dispute-Summary"),







    path('callback/',views.TestCallbackView.as_view(), name="call-test-view"),
    #path('test/',views.TestView.as_view(), name="test-view")
]
