from drf_yasg.utils import swagger_auto_schema

from . import serializers
from . import models

from follows.models import UserFollow

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination

from django.http import Http404
from django.db.models import Q
from django.db.models import Count
from django.db.models import Prefetch
from django.core.cache import cache

from users.views import delete_cache

class PostPagination(PageNumberPagination):
    page_size = 3


# Create your views here.

class PostView(APIView):
    permission_classes= [
                IsAuthenticated,
            ]
    serializer_class = serializers.PostSerializer

    @swagger_auto_schema(request_body=serializer_class, operation_description="Allows the user to create a new feed post. N.B:This endpoint returns paginated responses.")
    def post(self,request):
        serializer = self.serializer_class(data=request.data,context={"request":request})
        if serializer.is_valid(raise_exception=True):
            output = serializer.save()
            return Response(output,status=status.HTTP_201_CREATED)

    @swagger_auto_schema(operation_description="Retrieves Post data and related data count for comments and likes")
    def get(self,request):
        param = request.query_params.get("post_id",None)
        user_type = request.user.industry
        if user_type == "":
            user_type = "others"

        if not param:
            base_url = request.build_absolute_uri()
            base_url = base_url.split("?")[0]
            page_request = request.query_params.get("page","1")
            cache_key = f"{user_type}_post_{page_request}"
            cached_data = cache.get(cache_key)
            if not cached_data:
                posts = models.Posts.objects.filter(Q(industries__icontains=user_type.lower()) | Q(profile__user__user_type="mentor")).order_by("-time_stamp")
                paginator = PostPagination()
                paginated_items = paginator.paginate_queryset(posts,request)

                serializer = serializers.RetrievePostSerializer(paginated_items,many=True)

                item_counts = posts.count()
                floor = item_counts//paginator.page_size
                if item_counts % paginator.page_size == 0:
                    last_page = floor
                else:
                    last_page = floor + 1

                response = paginator.get_paginated_response(serializer.data).data
                response["last_page"] = f"{base_url}?page={last_page}"
                cache.set(cache_key,response,timeout=300)
                return Response(response,status=status.HTTP_200_OK)
            else:
                return Response(cached_data,status=status.HTTP_200_OK)
        else:
            try:
                post = models.Posts.objects.get(id=param)
                #print(post.media)
                #output = serializers.ParentPostSerializer(post,many=False).data
                output = serializers.RetrievePostSerializer(post,many=False).data
                return Response(output,status=status.HTTP_200_OK)
            except:
                return Response({"error":"Inexistent Post"},status=status.HTTP_404_NOT_FOUND)


class FollowingPostView(APIView):
    permission_classes = [
        IsAuthenticated,
    ]
    serializer_class = serializers.RetrievePostSerializer
    def get(self,request):
        user = request.user
        followings = user.follower.select_related("user_following__profile").all()
        profiles = [following.user_following.profile.id for following in followings]
        #profiles = [profile.id for profile in user_followings]
        following_posts = models.Posts.objects.filter(profile__in=profiles).order_by("-time_stamp")

        paginator = PostPagination()
        paginated_items = paginator.paginate_queryset(following_posts,request)

        serializer = self.serializer_class(paginated_items,many=True).data
        response = paginator.get_paginated_response(serializer).data

        return Response(response,status=status.HTTP_200_OK)









class CreateCommentView(APIView):
    permission_classes = [
                IsAuthenticated,
            ]
    serializer_class = serializers.CreateCommentSerializer

    @swagger_auto_schema(request_body=serializer_class,operation_description="Allows user to create a comment to a Post.")
    def post(self,request):
        serializer = self.serializer_class(data=request.data,context={"request":request})
        if serializer.is_valid(raise_exception=True):
            output = serializer.save()
            return Response(output,status=status.HTTP_201_CREATED)
    
    @swagger_auto_schema(operation_description="Retrieves all comments for a particular post using the query parameter *post_id")
    def get(self,request):
        post_id = request.query_params.get("post_id")
        if post_id:
            try:
                post = models.Posts.objects.get(id=post_id)
                comments = models.Comment.objects.filter(post=post)
                serializer = serializers.CommentSerializer(comments,many=True).data
                output = [comment for comment in serializer if not comment["parent"]]
                return Response(output,status=status.HTTP_200_OK)

            except:
                return Response({"error":"Inexistent post"},status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error":"No query parameter"},status=status.HTTP_400_BAD_REQUEST)



class CreateReplyView(APIView):
    permission_classes = [
                IsAuthenticated,
            ]
    serializer_class = serializers.CreateReplySerializer

    @swagger_auto_schema(request_body=serializer_class,operation_description="Allows user to create a reply to a Post comment.")
    def post(self,request):
        serializer = self.serializer_class(data=request.data,context={"request":request})
        if serializer.is_valid(raise_exception=True):
            output = serializer.save()
            return Response(output,status=status.HTTP_201_CREATED)



class CreateLikeView(APIView):
    permission_classes = [
                IsAuthenticated,
            ]
    serializer_class = serializers.CreateLikeSerializer


    @swagger_auto_schema(request_body=serializer_class,operation_description="Allows user to like a Post once.")
    def post(self,request):
        serializer = self.serializer_class(data=request.data,context={"user":request.user})
        if serializer.is_valid(raise_exception=True):
            output = serializer.save()
            return Response(output,status=status.HTTP_201_CREATED)


class RepostView(APIView):
    permission_classes= [
                IsAuthenticated,
            ]
    serializer_class = serializers.RepostSerializer

    @swagger_auto_schema(request_body=serializer_class,operation_description="Allows a user to repost a feed.")
    def post(self,request):
        serializer = self.serializer_class(data=request.data,context={"user":request.user})
        if serializer.is_valid(raise_exception=True):
            output = serializer.save()
            return Response(output,status=status.HTTP_201_CREATED)



class SavePostView(APIView):
    permission_classes = [
                IsAuthenticated,
            ]
    serializer_class = serializers.SavePostSerializer

    @swagger_auto_schema(request_body=serializer_class, operation_description="Allows user to save a post.")
    def post(self,request):
        serializer = self.serializer_class(data=request.data,context={"user":request.user})
        if serializer.is_valid(raise_exception=True):
            output = serializer.save()
            return Response(output,status=status.HTTP_201_CREATED)

    @swagger_auto_schema(operation_description="Gets all the saved posts for the logged in user.")
    def get(self,request):
        user = request.user
        saved_posts = models.PostSave.objects.filter(user=user)
        #print(saved_posts.values())
        saved_posts = serializers.RetrieveSavePostSerializer(saved_posts,many=True).data
        return Response(saved_posts,status=status.HTTP_200_OK)


class ShareView(APIView):
    permission_classes = [
                IsAuthenticated,
            ]
    serializer_class = serializers.ShareSerializer

    @swagger_auto_schema(request_body=serializer_class,operation_description="Allows recording of the number of shares of a post.")
    def post(self,request):
        serializer = self.serializer_class(data=request.data,context={"user":request.user})
        if serializer.is_valid(raise_exception=True):
            output = serializer.save()
            return Response(output,status=status.HTTP_201_CREATED)

