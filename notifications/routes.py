from django.urls import path,re_path
from . import consumers

urlpatterns = [
    path("ws/notification/",consumers.NotificationConsumer.as_asgi()),
    re_path("ws/chat/(?P<other_user>\d+)/$",consumers.ChatConsumer.as_asgi()),
    path("ws/notification/jobs/",consumers.JobNotificationConsumer.as_asgi()),
]
