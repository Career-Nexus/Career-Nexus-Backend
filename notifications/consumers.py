import json
from channels.db import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from django.contrib.auth import get_user_model



class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        user = self.scope["user"]
        #self.group_name = f"notification_{user.email}"
        self.group_name = f"notification_for_{user.id}"
        await self.channel_layer.group_add(self.group_name,self.channel_name)
        await self.accept()
        #logging
        print(f"User with id {user.id} is connected to {self.group_name}")

    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.group_name,self.channel_name)

    async def send_notification(self,event):
        await self.send(
            text_data=json.dumps({"message":event["message"]})
        )



class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        #Late imports to ensure apps are loaded at runtime
        from django.db.models import Q
        from . import models


        self.user = self.scope["user"]
        self.other_id = self.scope["url_route"]["kwargs"]["other_user"]
        User = get_user_model()
        try:
            self.other_user = await sync_to_async(User.objects.get)(id=self.other_id)
            try:
                self.room_obj = await sync_to_async(models.Chatroom.objects.get)(Q(initiator=self.user,contributor=self.other_user) | Q(initiator=self.other_user,contributor=self.user))
            except models.Chatroom.DoesNotExist:
                self.room_obj = await sync_to_async(models.Chatroom.objects.create)(initiator=self.user,contributor=self.other_user)
        except User.DoesNotExist:
            #print("Inexistent user")
            await self.close()
            return
        if self.user == self.other_user:
            await self.close()
            return
        self.room_suffix = f"{max(self.user.id,int(self.other_id))}{min(self.user.id,int(self.other_id))}"
        self.room_group_name = f"chatroom_{self.room_suffix}"
        print(self.room_group_name)
        await self.channel_layer.group_add(self.room_group_name,self.channel_name)
        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.room_group_name,self.channel_name)

    async def receive(self, text_data):
        #Late imports to ensure apps are loaded at runtime
        from django.db.models import Q
        from . import models


        data = json.loads(text_data)
        message = data.get("message")
        await sync_to_async(models.Message.objects.create)(room=self.room_obj,person=self.user,message=message)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type":"send_message",
                "user_id":self.user.id,
                "email":self.user.email,
                "message":message
            }
        )


    async def send_message(self,event):
        await self.send(text_data=json.dumps({
            "user_id":event["user_id"],
            "email":event["email"],
            "message":event["message"]
        }))
