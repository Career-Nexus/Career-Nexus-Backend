#from django.shortcuts import render
from django.core import paginator
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination

from . import serializers
from . import models


class JobPagination(PageNumberPagination):
    page_size = 5



class JobsView(APIView):
    permission_classes = [
        IsAuthenticated,
    ]
    serializer_class =serializers.JobsSerializer

    def post(self,request):
        user_type = request.user.user_type
        if user_type == "employer":
            serializer = self.serializer_class(data=request.data,context={"user":request.user})
            if serializer.is_valid(raise_exception=True):
                output = serializer.save()
                return Response(output,status=status.HTTP_200_OK)
        else:
            return Response({"Unauthorized":f"User of type {user_type} cannot post jobs"},status=status.HTTP_401_UNAUTHORIZED)

    def get(self,request):
        user = request.user
        base_url = request.build_absolute_uri()
        base_url = base_url.split("?")[0]
        print(base_url)
        job_posts = user.poster.all().order_by("-time_stamp")

        paginator = JobPagination()
        paginated_items = paginator.paginate_queryset(job_posts,request)



        serialized_data = self.serializer_class(paginated_items,many=True).data
        response = paginator.get_paginated_response(serialized_data).data
        return Response(response,status=status.HTTP_200_OK)


class RecommendJobView(APIView):
    permission_classes = [
        IsAuthenticated,
    ]
    serializer_class = serializers.JobsSerializer

    def get(self,request):
        user = request.user
        user_industry = user.industry

        recommended_jobs = models.Jobs.objects.filter(industry__icontains = user_industry)

        paginator = JobPagination()
        paginated_items = paginator.paginate_queryset(recommended_jobs,request)


        serialized_data = self.serializer_class(paginated_items,many=True).data
        output = paginator.get_paginated_response(serialized_data).data
        return Response(output,status=status.HTTP_200_OK)
