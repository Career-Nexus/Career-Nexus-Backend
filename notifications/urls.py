from django.urls import path
from . import consumers

urlpatterns = [
    path("ws/notification/",consumers.NotificationConsumer.as_asgi()),
]
