from django.core.paginator import Page
from django.shortcuts import render
from django.db.models import Q
from django.http import Http404

import rest_framework
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.pagination import PageNumberPagination


from . import models
from . import serializers


class NotificationPaginator(PageNumberPagination):
    page_size = 5


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
        params = request.query_params.get("chat_id")
        if not params:
            return Response({"error":"No chat_id provided"})
        else:
            chatroom = self.get_chatroom(chat_id=params,user=request.user)
            messages = models.Message.objects.filter(room=chatroom).order_by("-timestamp")
            serialized_data = self.serializer_class(messages,many=True).data
            return Response(serialized_data,status=status.HTTP_200_OK)


class NotificationView(APIView):
    permission_classes = [
        IsAuthenticated,
    ]

    def get(self,request):
        user = request.user
        all_notifications = models.Notification.objects.filter(user=user).order_by("-timestamp")

        paginator = NotificationPaginator()
        paginated_items = paginator.paginate_queryset(all_notifications,request)
        serialized_items = serializers.NotificationSerializer(paginated_items,many=True).data
        output = paginator.get_paginated_response(serialized_items).data
        return Response(output,status=status.HTTP_200_OK)

    def delete(self,request):
        user = request.user
        all_notifications = models.Notification.objects.filter(user=user)
        all_notifications.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TestNotificationView(APIView):
    permission_classes = [
        IsAuthenticated,
    ]

    def post(self,request):
        user = request.user
        serializer = serializers.TestNotificationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"status":"Sent push notification"},status=status.HTTP_200_OK)
        
