#from django.shortcuts import render
from functools import partial

from django.db.models.query import InstanceCheckMeta
from django.http import Http404,HttpResponseBadRequest
from django.core.exceptions import BadRequest

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from notifications.utils import jobnotify


from . import serializers
from . import models
from .permissions import IsEmployer
from utilities.helpers import retrieve_object,retrieve_query_parameter


import uuid



def no_object_fails(message):
    raise Http404(message)

def no_parameter_fails(message):
    raise Http404(message)







class JobPagination(PageNumberPagination):
    page_size = 5

class JobApplicationPagination(PageNumberPagination):
    page_size=10


class JobsView(APIView):
    permission_classes = [
        IsAuthenticated,
        IsEmployer,
    ]
    serializer_class =serializers.JobsSerializer

    def post(self,request):
        user_type = request.user.user_type
        serializer = self.serializer_class(data=request.data,context={"user":request.user})
        if serializer.is_valid(raise_exception=True):
            output = serializer.save()

            title = output.get("title").lower().replace(" ","_")
            employment_type = output.get("employment_type").lower()
            work_type = output.get("work_type").lower()
            industries = output.get("industry").lower().split(",")
            experience_level = output.get("experience_level").lower()

            for industry in industries:
                combination = f"{title}_{employment_type}_{work_type}_{industry}_{experience_level}"
                #Retrieving or creating a ref no associated with the job post combination which is to be used in the construction of group name for JobNotificationConsumer
                try:
                    suffix_obj = models.JobPreferenceSuffix.objects.get(preference_combination=combination)
                except:
                    suffix_obj = models.JobPreferenceSuffix.objects.create(ref_no=str(uuid.uuid4()),preference_combination=combination)

                suffix = suffix_obj.ref_no

                text = f"A new job matching your preference. {output['title']} at {output['organization']}. Apply now!"

                jobnotify(suffix=suffix,text=text)

            return Response(output,status=status.HTTP_200_OK)

    def get(self,request):
        user = request.user
        status_param = request.query_params.get("status")
        if not status_param:
            job_posts = user.poster.all().order_by("-time_stamp")
        else:
            allowed_status = ["active","draft","closed"]
            if status_param not in allowed_status:
                return Response({"error":"Invalid status parameter"},status=status.HTTP_400_BAD_REQUEST)
            job_posts = user.poster.filter(status=status_param).order_by("-time_stamp")

        paginator = JobPagination()
        paginated_items = paginator.paginate_queryset(job_posts,request)

        serialized_data = serializers.RetrieveJobSerializer(paginated_items,context={"user":user},many=True).data
        response = paginator.get_paginated_response(serialized_data).data
        return Response(response,status=status.HTTP_200_OK)

    def put(self,request):
        user = request.user
        job_id = retrieve_query_parameter(request,"job_id",no_parameter_fails,"A job_id query parameter is required.")
        job = retrieve_object(job_id,models.Jobs,no_object_fails,"Invalid job id")

        if job.status != "draft":
            return Response({"error":"Only Draft jobs can be edited"},status=status.HTTP_403_FORBIDDEN)

        serializer = serializers.JobsSerializer(data=request.data,instance=job,context={"user":user},partial=True)
        if serializer.is_valid(raise_exception=True):
            job_instance = serializer.save()
            output = serializers.RetrieveJobSerializer(job_instance,many=False,context={"user":user}).data
            return Response(output,status=status.HTTP_206_PARTIAL_CONTENT)




class JobApplicationView(APIView):
    permission_classes = [
        IsAuthenticated,
    ]

    def post(self,request):
        user = request.user
        serializer = serializers.JobApplicationSerializer(data=request.data,context={"user":user})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            output = {
                "application_status":"Success"
            }
            return Response(output,status=status.HTTP_200_OK)

    def get(self,request):
        user = request.user
        all_applied_jobs = user.jobapplication_set.all()
        output = serializers.RetrieveAppliedJobs(all_applied_jobs,many=True).data
        return Response(output,status=status.HTTP_200_OK)


class RetrieveRecentJobApplicationsView(APIView):
    permission_classes = [
        IsAuthenticated,
        IsEmployer
    ]

    def get(self,request):
        user = request.user
        recently_applied = models.JobApplication.objects.filter(job__poster=user).order_by("-applied_on")[:5]
        output = serializers.RetrieveRecentJobApplicantsSerializer(recently_applied,many=True).data
        return Response(output,status=status.HTTP_200_OK)




class RetrieveJobApplicationView(APIView):
    permission_classes = [
        IsAuthenticated,
        IsEmployer,
    ]

    def get(self,request):
        user = request.user
        job = request.query_params.get("job_id")
        if not job:
            return Response({"error":"A job_id query parameter is required for this request"},status=status.HTTP_400_BAD_REQUEST)
        job_instance = models.Jobs.objects.filter(id=job).first()
        if not job_instance:
            return Response({"error":"Invalid Job ID"},status=status.HTTP_400_BAD_REQUEST)
        if job_instance.poster == user:
            return Response({"error":"This job was posted by another user."},status=status.HTTP_401_UNAUTHORIZED)
        all_applicants = job_instance.application.all().order_by("-applied_on")
        paginator = JobApplicationPagination()
        paginated_items = paginator.paginate_queryset(all_applicants,request)
        serialized_items = serializers.RetrieveJobApplicationSerializer(paginated_items,many=True).data
        output = paginator.get_paginated_response(serialized_items).data
        return Response(output,status=status.HTTP_200_OK)



class RecommendJobView(APIView):
    permission_classes = [
        IsAuthenticated,
    ]
    serializer_class = serializers.RetrieveJobSerializer

    def get(self,request):
        user = request.user
        user_industry = user.industry

        recommended_jobs = models.Jobs.objects.filter(industry__icontains = user_industry,status="active")

        paginator = JobPagination()
        paginated_items = paginator.paginate_queryset(recommended_jobs,request)


        serialized_data = self.serializer_class(paginated_items,context={"user":user},many=True).data
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
                "experience_level":preference.experience_level,
                "preference_set":True
            }
            return Response(output,status=status.HTTP_200_OK)
        except models.JobPreference.DoesNotExist:
            output = {
                "title":"N/A",
                "employment_type":"N/A",
                "work_type":"N/A",
                "industry":"N/A",
                "experience_level":"N/A",
                "preference_set":False
            }
            return Response(output,status=status.HTTP_200_OK)


class SaveJobView(APIView):
    permission_classes = [
        IsAuthenticated,
    ]

    def post(self,request):
        user = request.user
        serializer = serializers.SaveJobSerializer(data=request.data,context={"user":user})
        if serializer.is_valid(raise_exception=True):
            output_instance = serializer.save()
            output = serializers.RetrieveSavedJobSerializer(output_instance,many=False).data
            return Response(output,status=status.HTTP_201_CREATED)

    def get(self,request):
        user = request.user
        saved_jobs = user.job_saver.all()
        output = serializers.RetrieveSavedJobSerializer(saved_jobs,many=True).data
        return Response(output,status=status.HTTP_200_OK)

class UnsaveJobView(APIView):
    permission_classes = [
        IsAuthenticated,
    ]

    def delete(self,request):
        user = request.user
        param = request.query_params.get("job")
        if not param:
            return Response({"error":"A job query parameter is required for this request"},status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer = serializers.UnsaveJobSerializer(data=request.query_params,context={"user":user})
            if serializer.is_valid(raise_exception=True):
                saved_instance = serializer.validated_data
                saved_instance.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)



class JobStatusUpdateView(APIView):
    permission_classes = [
        IsAuthenticated,
        IsEmployer,
    ]

    def put(self,request):
        user = request.user
        serializer = serializers.JobStatusUpdateSerializer(data=request.data,instance=user,context={"user":user},partial=False)
        if serializer.is_valid(raise_exception=True):
            output_instance = serializer.save()
            output = serializers.RetrieveJobSerializer(output_instance,many=False,context={"user":user}).data
            return Response(output,status=status.HTTP_200_OK)
