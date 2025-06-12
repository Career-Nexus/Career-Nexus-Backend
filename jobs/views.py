#from django.shortcuts import render
from django.core import paginator
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from notifications.utils import jobnotify

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

                title = output.get("title").lower()
                title = title.replace(" ","_")
                employment_type = output.get("employment_type").lower()
                work_type = output.get("work_type").lower()
                industries = output.get("industry").split(",")

                for industry in industries:
                    suffix = f"{title}_{employment_type}_{work_type}_{industry}"
                    text = f"A new job matching your preference. {output['title']} at {output['organization']}. Apply now!"

                    jobnotify(suffix=suffix,text=text)

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



class JobPreferenceView(APIView):
    permission_classes = [
        IsAuthenticated,
    ]
    serializer_class = serializers.JobPreferenceSerializer

    def put(self,request):
        user = request.user
        preference_obj, created = models.JobPreference.objects.get_or_create(user=user)
        serializer = self.serializer_class(data=request.data,instance=preference_obj)
        if serializer.is_valid(raise_exception=True):
            instance = serializer.save()
            output = {
                "title":instance.title,
                "employment_type":instance.employment_type,
                "work_type":instance.work_type,
                "industry":instance.industry,
                "experience_level":instance.experience_level
            }
            return Response(output,status=status.HTTP_200_OK)

    def get(self,request):
        user = request.user
        try:
            preference = models.JobPreference.objects.get(user=user)
            output = {
                "title":preference.title,
                "employment_type":preference.employment_type,
                "work_type":preference.work_type,
                "industry":preference.industry,
                "experience_level":preference.experience_level
            }
            return Response(output,status=status.HTTP_200_OK)
        except models.JobPreference.DoesNotExist:
            output = {
                "title":"N/A",
                "employment_type":"N/A",
                "work_type":"N/A",
                "industry":"N/A",
                "experience_level":"N/A"
            }
            return Response(output,status=status.HTTP_200_OK)
