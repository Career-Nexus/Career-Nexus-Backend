from django.template import context
from drf_yasg.utils import swagger_auto_schema

from . import serializers
from . import models

from follows.models import UserFollow

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.pagination import PageNumberPagination

from django.http import Http404
from django.db.models import Q
from django.db.models import Count
from django.db.models import Prefetch
from django.core.cache import cache

from users.views import delete_cache
from users.models import Users


def invalidate_post_cache(user_industry,user_id=None):
    if user_industry == "":
        user_industry = "others"
    for item in range(1,6):
        cache_key = f"{user_industry}_post_{item}"
        delete_cache(cache_key)
    if user_id:
        for item in range(1,6):
            cache_key = f"{user_id}_ownposts_{item}"
            delete_cache(cache_key)



class PostPagination(PageNumberPagination):
    page_size = 5




class PostView(APIView):
    permission_classes= [
                IsAuthenticated,
            ]
    serializer_class = serializers.PostSerializer

    @swagger_auto_schema(request_body=serializer_class, operation_description="Allows the user to create a new feed post. N.B:This endpoint returns paginated responses.")
    def post(self,request):
        user = request.user
        serializer = self.serializer_class(data=request.data,context={"request":request})
        if serializer.is_valid(raise_exception=True):
            output = serializer.save()
            invalidate_post_cache(user_industry=user.industry,user_id=user.id)
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
                posts = models.Posts.objects.select_related("profile","profile__user").filter(Q(industries__icontains=user_type.lower()) | Q(profile__user__user_type="mentor")).order_by("-time_stamp")
                paginator = PostPagination()
                paginated_items = paginator.paginate_queryset(posts,request)

                serializer = serializers.RetrievePostSerializer(paginated_items,many=True,context={"user":request.user})

                item_counts = posts.count()
                floor = item_counts//paginator.page_size
                if item_counts % paginator.page_size == 0:
                    last_page = floor
                else:
                    last_page = floor + 1

                response = paginator.get_paginated_response(serializer.data).data
                response["last_page"] = f"{base_url}?page={last_page}"
                cache.set(cache_key,response,timeout=60)
                return Response(response,status=status.HTTP_200_OK)
            else:
                return Response(cached_data,status=status.HTTP_200_OK)
        else:
            try:
                post = models.Posts.objects.get(id=param)

                output = serializers.RetrievePostSerializer(post,many=False,context={"user":request.user}).data
                return Response(output,status=status.HTTP_200_OK)
            except models.Posts.DoesNotExist:
                return Response({"error":"Inexistent Post"},status=status.HTTP_404_NOT_FOUND)


class DeletePostView(APIView):
    permission_classes = [
        IsAuthenticated,
    ]
    def delete(self,request):
        user = request.user
        param = request.query_params.get("post_id")
        if not param:
            return Response({"error":"A post_id query parameter is required for this request"},status=status.HTTP_400_BAD_REQUEST)
        else:
            post = models.Posts.objects.filter(id=param).first()
            if not post:
                return Response({"error":"Invalid Post ID"},status=status.HTTP_400_BAD_REQUEST)
            else:
                if post.profile != user.profile:
                    return Response({"error":"Can't delete another users post"},status=status.HTTP_401_UNAUTHORIZED)
                else:
                    post.delete()
                    #Avoid returning stale post data
                    invalidate_post_cache(user_industry=user.industry,user_id=user.id)
                    return Response(status=status.HTTP_204_NO_CONTENT)



class OtherUserPosts(APIView):
    permission_classes =[
        IsAuthenticated,
    ]
    def get(self,request):
        user = request.user
        param = request.query_params.get("user_id")
        page_number = request.query_params.get("page",'1')
        if not param:
            return Response({"error":"No user_id query parameter was provided."},status=status.HTTP_400_BAD_REQUEST)
        else:
            other_user = Users.objects.filter(id=param).first()
            if not other_user:
                return Response({"error":"Invalid user_id"},status=status.HTTP_400_BAD_REQUEST)
            else:
                cache_key = f"{other_user.id}_ownposts_{page_number}"
                cached_data = cache.get(cache_key)
                if not cached_data:
                    other_users_posts = models.Posts.objects.filter(profile=other_user.profile).order_by("-time_stamp")
                    paginator = PostPagination()
                    paginated_items = paginator.paginate_queryset(other_users_posts,request)
                    serialized_data = serializers.RetrievePostSerializer(paginated_items,many=True,context={"user":user}).data
                    output = paginator.get_paginated_response(serialized_data).data
                    cache.set(cache_key,output,timeout=60)
                    return Response(output,status=status.HTTP_200_OK)
                else:
                    return Response(cached_data,status=status.HTTP_200_OK)




class OwnPosts(APIView):
    permission_classes = [
        IsAuthenticated,
    ]
    
    def get(self,request):
        base_url = request.build_absolute_uri()
        base_url = base_url.split()[0]
        user = request.user
        page_number = request.query_params.get("page","1")
        cache_key = f"{request.user.id}_ownposts_{page_number}"
        cached_data = cache.get(cache_key)
        if not cached_data:
            posts = user.profile.posts_set.all().order_by("-time_stamp")
            paginator = PostPagination()
            paginated_items = paginator.paginate_queryset(posts,request)
            serialized_items = serializers.RetrievePostSerializer(paginated_items,many=True,context={"user":request.user}).data

            item_count = posts.count()
            floor = item_count//paginator.page_size
            if item_count % paginator.page_size == 0:
                last_page = floor
            else:
                last_page = floor + 1

            output = paginator.get_paginated_response(serialized_items).data
            output["last_page"] = f"{base_url}?page={last_page}"
            cache.set(cache_key,output,timeout=60)
            return Response(output,status=status.HTTP_200_OK)
        else:
            return Response(cached_data,status=status.HTTP_200_OK)


class MentorPostsView(APIView):
    permission_classes = [
        IsAuthenticated,
    ]

    def get(self,request):
        mentors_posts = models.Posts.objects.filter(profile__user__user_type="mentor").order_by("-time_stamp")
        paginator = PostPagination()
        paginated_items = paginator.paginate_queryset(mentors_posts,request)
        serialized_items = serializers.RetrievePostSerializer(paginated_items,many=True,context={"user":request.user}).data
        output = paginator.get_paginated_response(serialized_items).data
        return Response(output,status=status.HTTP_200_OK)





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

        serializer = self.serializer_class(paginated_items,many=True,context={"user":request.user}).data
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
                serializer = serializers.CommentSerializer(comments,context={"user":request.user},many=True).data
                output = [comment for comment in serializer if not comment["parent"]]
                return Response(output,status=status.HTTP_200_OK)

            except models.Posts.DoesNotExist:
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
            user_industry = request.user.industry
            #Deleting cache to prevent returning stale data
            invalidate_post_cache(user_industry,user_id=request.user.id)
            return Response(output,status=status.HTTP_201_CREATED)



class UnlikePostView(APIView):
    permission_classes = [
        IsAuthenticated,
    ]

    def post(self,request):
        serializer = serializers.UnlikePostSerializer(data=request.data,context={"user":request.user})
        if serializer.is_valid(raise_exception=True):
            output = serializer.save()
            user_industry = request.user.industry
            #Avoiding returning stale data due to caching
            invalidate_post_cache(user_industry,user_id=request.user.id)
            return Response(output,status.HTTP_200_OK)


class CommentLikeView(APIView):
    permission_classes = [
        IsAuthenticated,
    ]

    def post(self,request):
        serializer = serializers.CommentLikeSerializer(data=request.data,context={"user":request.user})
        if serializer.is_valid(raise_exception=True):
            output_instance = serializer.save()
            output = {
                "comment_id":output_instance.comment.id,
                "user_id":output_instance.user.id,
                "status":"Liked Comment"
            }
            return Response(output,status=status.HTTP_201_CREATED)


class CommentUnlikeView(APIView):
    permission_classes = [
        IsAuthenticated,
    ]

    def post(self,request):
        serializer = serializers.CommentUnlikeSerializer(data=request.data,context={"user":request.user})
        if serializer.is_valid(raise_exception=True):
            comment = serializer.validated_data.get("comment")
            models.CommentLike.objects.filter(user=request.user,comment=comment).delete()
            return Response({"status":"Unliked Comment"},status=status.HTTP_200_OK)







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
        saved_posts = serializers.RetrieveSavePostSerializer(saved_posts,many=True,context={"user":request.user}).data
        return Response(saved_posts,status=status.HTTP_200_OK)


class ShareView(APIView):
    def get_permissions(self):
        if self.request.method == "POST":
            return [
                IsAuthenticated(),
            ]
        elif self.request.method == "GET":
            return [
                AllowAny(),
            ]

    serializer_class = serializers.ShareSerializer

    @swagger_auto_schema(request_body=serializer_class,operation_description="Allows recording of the number of shares of a post.")
    def post(self,request):
        serializer = self.serializer_class(data=request.data,context={"user":request.user})
        if serializer.is_valid(raise_exception=True):
            output = serializer.save()
            return Response(output,status=status.HTTP_200_OK)

    def get(self,request):
        param = request.query_params.get("hash")
        if not param:
            return Response({"error":"A hash query parameter is required for this request."},status=status.HTTP_400_BAD_REQUEST)
        else:
            cache_key = f"post_hash_{param}"
            cached_data = cache.get(cache_key)
            if not cached_data:
                shared_content = models.Share.objects.filter(hash=param).first()
                if not shared_content:
                    return Response({"error":"Invalid Share Hash"},status=status.HTTP_400_BAD_REQUEST)
                else:
                    output = serializers.RetrieveSharedPostSerializer(shared_content,many=False).data
                    cache.set(cache_key,output,timeout=60*60*24)
            else:
                output = cached_data
            return Response(output,status=status.HTTP_200_OK)

