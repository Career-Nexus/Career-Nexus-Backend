#from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import AllowAny,IsAuthenticated

from django.http import Http404

from . import models, serializers


from users.models import *
from posts.models import *
from users.serializers import PersonalProfileSerializer


class FollowView(APIView):
    permission_classes = [
                IsAuthenticated,
            ]
    serializer_class = serializers.FollowSerializer

    def post(self,request):
        serializer = self.serializer_class(data=request.data,context={"user":request.user})
        if serializer.is_valid(raise_exception=True):
            output = serializer.save()
            return Response(output,status=status.HTTP_201_CREATED)

class FollowingView(APIView):
    permission_classes = [
                IsAuthenticated,
            ]
    def get(self,request):
        user = request.user
        followings = user.follower.select_related("user_follower__profile").all()
        data = [following.user_following.profile for following in followings]
        serializer = serializers.RetrieveFollowingSerializer(data,many=True).data
        return Response(serializer,status=status.HTTP_200_OK)

class FollowerView(APIView):
    permission_classes = [
                IsAuthenticated,
            ]
    def get(self,request):
        user = request.user
        followers = user.following.select_related("user_following__profile").all()
        data = [follower.user_follower.profile for follower in followers]
        serializer = serializers.RetrieveFollowingSerializer(data,many=True).data
        return Response(serializer,status=status.HTTP_200_OK)

class FollowingCountView(APIView):
    permission_classes = [
        IsAuthenticated,
    ]
    def get(self,request):
        user = request.user
        followings = user.follower.all()
        followings_count = len(followings)
        return Response({"following_count":followings_count},status=status.HTTP_200_OK)

class FollowerCountView(APIView):
    permission_classes = [
        IsAuthenticated,
    ]
    def get(self,request):
        user = request.user
        followers = user.following.all()
        followers_count = len(followers)
        return Response({"followers count":followers_count},status=status.HTTP_200_OK)











class Test(APIView):
    permission_classes = [
                AllowAny,
            ]

    def get(self,request):
        return Response("Installed",status=status.HTTP_200_OK)
