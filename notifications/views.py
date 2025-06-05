from django.shortcuts import render
from django.db.models import Q
from django.http import Http404

import rest_framework
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated


from . import models
from . import serializers



class ChatView(APIView):
    permission_classes = [
        IsAuthenticated,
    ]
    serializer_class = serializers.ChatSerializer

    def get(self,request):
        chatrooms = models.Chatroom.objects.filter(Q(initiator=request.user) | Q(contributor=request.user)).order_by("-created")
        serialized_data = serializers.ChatSerializer(chatrooms,many=True).data
        return Response(serialized_data,status=status.HTTP_200_OK)



class ChatMessageView(APIView):
    permission_classes=[
        IsAuthenticated,
    ]
    serializer_class = serializers.ChatMessageSerializer

    def get_chatroom(self,chat_id,user):
        try:
            chatroom = models.Chatroom.objects.get(Q(id=chat_id,initiator=user) | Q(id=chat_id,contributor=user))
            return chatroom
        except models.Chatroom.DoesNotExist:
            raise Http404("Invalid Chatroom_id")



    def get(self,request):
        params = int(request.query_params.get("chat_id"))
        if not params:
            return Response({"error":"No chat_id provided"})
        else:
            chatroom = self.get_chatroom(chat_id=params,user=request.user)
            messages = models.Message.objects.filter(room=chatroom).order_by("-timestamp")
            serialized_data = self.serializer_class(messages,many=True).data
            return Response(serialized_data,status=status.HTTP_200_OK)

