from django.urls import path,re_path
from . import views

urlpatterns = [
    path("chats/",views.ChatView.as_view(),name="Chats"),
    path("chat/messages/",views.ChatMessageView.as_view(),name="Chat-Messages"),
    path("notifications/",views.NotificationView.as_view(),name="Notifications"),

    path("test/",views.TestNotificationView.as_view(),name="Test-Notifications"),
]
