from datetime import time
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.pagination import PageNumberPagination

from django.core.cache import cache

from users.serializers import NewsLetterSubscribeSerializer


from . import serializers,models


def invalidate_newsletter_cache():
    for item in range(1,9):
        cache_key = f"Newsletter_Page_{item}"
        cache.delete(cache_key)





class NewletterPaginator(PageNumberPagination):
    page_size = 5




class SubscribeView(APIView):
    permission_classes = [
        IsAuthenticated,
    ]

    def post(self,request):
        serializer = serializers.SubscribeSerializer(data=request.data,context={"user":request.user})
        if serializer.is_valid(raise_exception=True):
            output_instance = serializer.save()
            output = serializers.NewsletterSubscriberSerializer(output_instance,many=False).data
            return Response(output,status=status.HTTP_200_OK)


class UnsubscribeView(APIView):
    permission_classes = [
        IsAuthenticated,
    ]
    def post(self,request):
        serializer = serializers.UnsubscribeSerializer(data=request.data,context={"user":request.user})
        if serializer.is_valid(raise_exception=True):
            output = serializer.save()
            return Response(output,status=status.HTTP_200_OK)



class CreateNewsLetterView(APIView):
    permission_classes = [
        #TODO Write Admin permissions for creating NewsLetters.
        IsAuthenticated,
    ]

    def post(self,request):
        serializer = serializers.CreateNewsLetterSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            output_instance = serializer.save()
            invalidate_newsletter_cache()
            output = serializers.NewsLetterSerializer(output_instance,many=False).data
            return Response(output,status=status.HTTP_200_OK)


class RetrieveNewsLetterView(APIView):
    permission_classes = [
        IsAuthenticated,
    ]

    def get(self,request):
        user = request.user
        param = request.query_params.get("page",1)
        cache_key = f"Newsletter_Page_{param}"
        if not models.NewsletterSubscribers.objects.filter(subscriber=user).exists():
            output = {
                "subscribed":False
            }
            return Response(output,status=status.HTTP_404_NOT_FOUND)
        cached = cache.get(cache_key)
        if not cached:
            newsletters = models.NewsLetter.objects.all().order_by("-timestamp")
            recent = serializers.NewsLetterSerializer(newsletters.first(),many=False).data
            paginator = NewletterPaginator()
            paginated_items = paginator.paginate_queryset(newsletters[1:],request)
            serialized_items = serializers.NewsLetterSerializer(paginated_items,many=True).data
            archive = paginator.get_paginated_response(serialized_items).data
            output = {
                "recent":recent,
                "archive":archive
            }
            cache.set(cache_key,output,timeout=60*60*24*6)
        else:
            output = cached
        return Response(output,status=status.HTTP_200_OK)






class TestView(APIView):
    permission_classes = [
        AllowAny,
    ]
    def get(self,request):
        return Response({"INSTALLED"},status=status.HTTP_200_OK)
