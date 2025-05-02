from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

def notify():
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "notification",
        {
            "type":"send_notification",
            "message":"Notification worked just fine!! Well done"
        }
    )
