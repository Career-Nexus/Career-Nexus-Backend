#from django.shortcuts import render
from rest_framework.response import Response

from . import serializers
from . import models

from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.pagination import PageNumberPagination

class PostPagination(PageNumberPagination):
    page_size = 5


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
        posts = models.Posts.objects.all().order_by("-time_stamp")
        serializer = serializers.RetrievePostSerializer(posts,many=True)

        return Response(serializer.data,status=status.HTTP_200_OK)
