#from django.shortcuts import render
from django.db.models import Q
from django.core.cache import cache
from django.http import Http404

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import AllowAny,IsAuthenticated


from . import models, serializers


from users.models import *
from users.views import delete_cache
from posts.models import *
from users.serializers import PersonalProfileSerializer
from posts.views import invalidate_post_cache
from networks.views import RecommendationPaginator
from networks.serializers import RetrieveRecommendationDetailSerializer


def invalidate_following_cache(user_email):
    for item in range(1,11):
        cache_key = f"{user_email}_following_recommendation_{item}"
        delete_cache(cache_key)



class FollowView(APIView):
    permission_classes = [
                IsAuthenticated,
            ]
    serializer_class = serializers.FollowSerializer

    def post(self,request):
        serializer = self.serializer_class(data=request.data,context={"user":request.user})
        if serializer.is_valid(raise_exception=True):
            output = serializer.save()
            user_industry = request.user.industry 
            #Avoid returning stale can_follow data if a user is followed from their posts page on the frontend.
            invalidate_post_cache(user_industry)
            invalidate_following_cache(request.user.email)

            return Response(output,status=status.HTTP_201_CREATED)



class UnfollowView(APIView):
    permission_classes = [
        IsAuthenticated,
    ]

    def post(self,request):
        serializer = serializers.UnfollowSerializer(data=request.data,context={"user":request.user})
        if serializer.is_valid(raise_exception=True):
            output = serializer.save()
            user_industry = request.user.industry
            #Avoid returning stale can_follow data if a user is unfollowed from their posts page in the frontend.
            invalidate_post_cache(user_industry)
            invalidate_following_cache(request.user.email)


            return Response(output,status=status.HTTP_200_OK)



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


class FollowingRecommendationView(APIView):
    permission_classes = [
        IsAuthenticated,
    ]
    def get(self,request):
        user = request.user
        user_industry = user.industry
        user_location = user.profile.location
        page = request.query_params.get("page",1)
        cache_key = f"{user.email}_following_recommendation_{page}"
        cached_data = cache.get(cache_key)
        if not cached_data:
            follows_recommendation = Users.objects.filter(
                Q(industry=user_industry) |
                Q(profile__location__icontains=user_location)
            ).exclude(id=user.id)
            #Exclude those that have been previously followed and shuffle them
            recommendation = follows_recommendation.exclude(
                Q(follower__user_following=user) |
                Q(following__user_follower=user)
            ).order_by("?")
            paginator = RecommendationPaginator()
            paginated_items = paginator.paginate_queryset(recommendation,request)
            serialized_items = RetrieveRecommendationDetailSerializer(paginated_items,many=True).data
            output = paginator.get_paginated_response(serialized_items).data
            cache.set(cache_key,output,timeout=3600)
            return Response(output,status=status.HTTP_200_OK)
        else:
            output= cached_data
            return Response(output,status=status.HTTP_200_OK)





class Test(APIView):
    permission_classes = [
                AllowAny,
            ]

    def get(self,request):
        return Response("Installed",status=status.HTTP_200_OK)
