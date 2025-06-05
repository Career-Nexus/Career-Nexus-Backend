from django.urls import path,re_path
from . import views

urlpatterns = [
    path("",views.ChatView.as_view(),name="Chats"),
    path("messages/",views.ChatMessageView.as_view(),name="Chat-Messages"),
]
