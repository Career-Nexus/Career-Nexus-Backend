from rest_framework.permissions import AllowAny
from . import views
from django.urls import path
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
   openapi.Info(
      title="CAREER NEXUS POST APIS",
      default_version='v1',
      description="APIs for managing content suggestions.",
      terms_of_service="",
      contact=openapi.Contact(email="saliuoazeez@gmail.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(AllowAny,)
)
urlpatterns= [
            #path("doc/",schema_view.with_ui("swagger",cache_timeout=0), name="Post-App-Documentation"),
            path("",views.PostView.as_view(),name="Add-View-Posts"),
            path("delete/",views.DeletePostView.as_view(),name="Delete-Post"),
            path("by-user/",views.OtherUserPosts.as_view(),name="Other-Users-Posts"),
            path("by-mentors/",views.MentorPostsView.as_view(),name="Mentors-Posts"),
            path("comment/",views.CreateCommentView.as_view(),name="Create-comment"),
            path("reply/",views.CreateReplyView.as_view(),name="Create-reply"),
            path("like/",views.CreateLikeView.as_view(),name="Create-Post-like"),
            path("like/comment/",views.CommentLikeView.as_view(),name="Create-Comment-Reply-Like"),
            path("unlike/",views.UnlikePostView.as_view(),name="Unlike-post"),
            path("unlike/comment/",views.CommentUnlikeView.as_view(),name="Unlike-comment"),
            path("repost/",views.RepostView.as_view(),name="Repost"),
            path("save/",views.SavePostView.as_view(),name="Save-post"),
            path("share/",views.ShareView.as_view(),name="Share-post"),
            path("following/",views.FollowingPostView.as_view(), name="Following-posts"),
            path("posted/",views.OwnPosts.as_view(),name="Own-Posts"),
        ]
