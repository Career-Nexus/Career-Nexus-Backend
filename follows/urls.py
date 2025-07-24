from django.urls import path
from . import views


urlpatterns = [
    path("test/",views.Test.as_view(),name="Test-view"),

    path("follow/",views.FollowView.as_view(),name="follow"),
    path("unfollow/",views.UnfollowView.as_view(),name="unfollow"),
    path("followings/",views.FollowingView.as_view(), name="followings"),
    path("followers/",views.FollowerView.as_view(),name="followers"),
    path("followers/count/",views.FollowerCountView.as_view(), name="followers-count"),
    path("followings/count/", views.FollowingCountView.as_view(), name="followings-count"),
    path("follow/recommendation/",views.FollowingRecommendationView.as_view(),name="Recommend-Following-View"),
        ]
