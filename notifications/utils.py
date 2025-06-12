from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

def notify(user_id,text="default"):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"notification_for_{user_id}",
        {
            "type":"send_notification",
            "message":text
        }
    )

def jobnotify(suffix,text):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"job_{suffix}",
        {
            "type":"notify",
            "message":text
        }
    )
