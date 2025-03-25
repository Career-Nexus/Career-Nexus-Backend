#from django.shortcuts import render
from rest_framework.response import Response

from . import serializers
from . import models

from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.pagination import PageNumberPagination

class PostPagination(PageNumberPagination):
    page_size = 3


# Create your views here.

class PostView(APIView):
    permission_classes= [
                IsAuthenticated,
            ]
    serializer_class = serializers.PostSerializer

    def post(self,request):
        serializer = self.serializer_class(data=request.data,context={"request":request})
        if serializer.is_valid(raise_exception=True):
            output = serializer.save()
            return Response(output,status=status.HTTP_201_CREATED)

    def get(self,request):
        base_url = request.build_absolute_uri()
        base_url = base_url.split("?")[0]

        posts = models.Posts.objects.all().order_by("-time_stamp")
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

        return Response(response,status=status.HTTP_200_OK)
