from . import views
from django.urls import path


urlpatterns= [
            path("",views.PostView.as_view(),name="Add-View-Posts"),
            path("comment/",views.CreateCommentView.as_view(),name="Create-comment"),
            path("reply/",views.CreateReplyView.as_view(),name="Create-reply"),
        ]
