from django.shortcuts import render
#import email
import os
import requests

from django.utils.ipv6 import is_valid_ipv6_address
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.pagination import PageNumberPagination
from rest_framework.exceptions import ValidationError


from . import serializers
from . import models
from .mmail import Agent

from django.contrib.auth import get_user_model

User = get_user_model()

agent = Agent()

class ItemPagination(PageNumberPagination):
    page_size = 10
    def get_next_link(self):
        if self.page.has_next():
            return f"?page={self.page.next_page_number()}"
        else:
            return None

    def get_previous_link(self):
        if self.page.has_previous():
            return f"?page={self.page.previous_page_number()}"
        else:
            return None


#Defining Templates
c_directory = os.path.dirname(os.path.abspath(__file__))
resources_directory = os.path.join(c_directory,"resources")
welcome_template = os.path.join(resources_directory,"welcome.html")
logo = os.path.join(resources_directory,"career-nexus_logo.png")



#Functions


class WaitListView(APIView):
    serializer_class = serializers.WaitListSerializer
    permission_classes = [
            AllowAny,
            ]
    def post(self,request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            data = serializer.save()
            first_name = data["name"].split()[0]
            email = data["email"]
            ref_code = data["ref_code"]
            subject = "Congratulations on Joining Career-Nexus – Your Career Journey Starts Here!"
            #agent.send_waitlist_mail(recepient=email,name=first_name,ref_code=ref_code)
            container = {"{NAME}":first_name,"{REFERRAL LINK}":ref_code,"{EMAIL}":"info@career-nexus.com"}
            agent.send_email(welcome_template,subject,container,recipient=email,attachment=logo)
            return Response(data,status=status.HTTP_201_CREATED)

class NewsLetterSubscribeView(APIView):
    serializer_class = serializers.NewsLetterSubscribeSerializer
    permission_classes=[
            AllowAny,
            ]

    def post(self,request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            output = serializer.save()
            return Response(output,status=status.HTTP_200_OK)

class NewsLetterUnsubscribeView(APIView):
    serializer_class = serializers.NewsLetterUnsubscribeSerializer
    permission_classes = [
            AllowAny,
            ]
    def get_object(self,request):
        email = request.data.get("email")
        if models.WaitList.objects.filter(email=email).exists():
            user = models.WaitList.objects.get(email=email)
            return user
        else:
            return Response({"Error":"Unregistered Email"},status=status.HTTP_400_BAD_REQUEST)

    def put(self,request):
        user = self.get_object(request)
        serializer = self.serializer_class(data=request.data, instance=user)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"Status":"Unsubscribed Successfully"},status=status.HTTP_200_OK)



class RegisterView(APIView):
    serializer_class=serializers.RegisterSerializer
    permission_classes=[
            AllowAny,
            ]

    def post(self,request):
        serializer =self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            data = serializer.save()	
            return Response(data,status=status.HTTP_201_CREATED)


class LoginView(APIView):
    permission_classes = [
                AllowAny,
            ]
    serializer_class = serializers.LoginSerializer

    def post(self,request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        refresh = RefreshToken.for_user(user)
        return Response(
                {
                    "refresh":str(refresh),
                    "access":str(refresh.access_token),
                    "user":user.email
                    },
                status=status.HTTP_200_OK
                )

class LogoutView(APIView):
    permission_classes = [
                IsAuthenticated,
            ]
    serializer_class = serializers.LogoutSerializer

    def post(self,request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({"status":"Logged Out"}, status=status.HTTP_202_ACCEPTED)




class DeleteWaitListView(APIView):
    serializer_class = serializers.DeleteWaitListSerializer
    permission_classes= [
            AllowAny,
            ]

    def delete(self,request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.validated_data.get("email")
            models.WaitList.objects.get(email=email).delete()
            return Response({"Deleted Successfully"},status=status.HTTP_204_NO_CONTENT)

#PROFILE VIEWS ------------------------------

class PersonalProfileView(APIView):
    permission_classes = [
                IsAuthenticated,
            ]
    serializer_class = serializers.PersonalProfileSerializer

    def get_object(self,request):
        user = request.user 
        user_object = models.PersonalProfile.objects.get(user=user)
        return user_object

    #View method serving as update and retrieving user profile data.
    def put(self,request):
        user = self.get_object(request)
        serializer = self.serializer_class(instance=user,data=request.data)
        if serializer.is_valid(raise_exception=True):
            output = serializer.save()
            return Response(output,status=status.HTTP_201_CREATED)

    def patch(self,request):
        user = models.Users.objects.filter(email=request.user.email).first()
        serializer = serializers.PostRegistrationSerializer(data=request.data,instance=user,partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            user_type = serializer.data.get("user_type")
            industry = serializer.data.get("industry")
            output = {
                        "user_type":user_type,
                        "industry":industry,
                        "email":user.email
                    }
            return Response(output,status=status.HTTP_206_PARTIAL_CONTENT)


class RetreiveProfileView(APIView):
    permission_classes = [
                IsAuthenticated,
            ]
    serializer_class = serializers.RetrieveProfileSerializer

    def post(self,request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            profile_id = serializer.data["profile_id"]
            profile = models.PersonalProfile.objects.get(id=profile_id)
            profile_owner = profile.user
            owner_experience = models.experience.objects.filter(user=profile_owner).values("title","organization","start_date","end_date","location","employment_type","detail").order_by("-end_date")
            owner_education = models.education.objects.filter(user=profile_owner).values("course","school","start_date","end_date","location","detail").order_by("-end_date")
            owner_certification = models.certification.objects.filter(user=profile_owner).values("title","school","issue_date","cert_id","skills").order_by("-issue_date")
            output = {
                    "name":profile.name,
                    "profile_photo":profile.profile_photo,
                    "qualification":profile.qualification,
                    "intro_video":profile.intro_video,
                    "summary":profile.summary,
                    "experience":owner_experience,
                    "education":owner_education,
                    "certification":owner_certification
                }
            return Response(output,status=status.HTTP_200_OK)







class ExperienceView(APIView):
    permission_classes= [
                IsAuthenticated,
            ]
    serializer_class= serializers.ExperienceSerializer

    def get(self,request):
        user_id = request.user.id
        data = models.experience.objects.filter(user_id=user_id).values("id","title","organization","start_date","end_date","location","employment_type","detail").order_by("-start_date")
        return Response(data,status=status.HTTP_200_OK)


    def post(self,request):
        serializer = self.serializer_class(data=request.data, context={"request":request})
        if serializer.is_valid(raise_exception=True):
            output = serializer.save()
            output = {
                        "title":output.title,
                        "organization":output.organization,
                        "start_date":output.start_date,
                        "end_date":output.end_date,
                        "location":output.location,
                        "employment_type":output.employment_type,
                        "detail":output.detail
                    }
            return Response(output,status=status.HTTP_201_CREATED)


class UpdateExperienceView(APIView):
    permission_classes= [
                IsAuthenticated,
            ]
    serializer_class = serializers.UpdateExperienceSerializer

    def put(self,request):
        serializer = self.serializer_class(data=request.data,instance=request.user,context={"request":request})
        if serializer.is_valid(raise_exception=True):
            output = serializer.save()
            return Response(output,status=status.HTTP_201_CREATED)



class EducationView(APIView):
    permission_classes= [
                IsAuthenticated,
            ]
    serializer_class = serializers.EducationSerializer

    def post(self,request):
        serializer = self.serializer_class(data=request.data,context={"request":request.user})
        if serializer.is_valid(raise_exception=True):
            output = serializer.save()
            return Response(output,status=status.HTTP_201_CREATED)

    def get(self,request):
        detail = models.education.objects.filter(user_id=request.user.id).values("id","course","school","start_date","end_date","location","detail").order_by("-start_date")
        return Response(detail,status=status.HTTP_200_OK)

    def put(self,request):
        serializer = serializers.UpdateEducationSerializer(data=request.data,instance=request.user,context={"request":request})
        if serializer.is_valid(raise_exception=True):
            output = serializer.save()
            return Response(output,status=status.HTTP_201_CREATED)

    def delete(self,request):
        serializer = serializers.UpdateEducationSerializer(data=request.data,context={"request":request})
        if serializer.is_valid(raise_exception=True):
            id = serializer.validated_data["id"]
            models.education.objects.get(id=id).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)


class CertificationView(APIView):
    permission_classes = [
                IsAuthenticated,
            ]
    serializer_class = serializers.CertificationSerializer

    def post(self,request):
        serializer = self.serializer_class(data=request.data,context={"request":request})
        if serializer.is_valid(raise_exception=True):
            output = serializer.save()
            return Response(output,status=status.HTTP_201_CREATED)

    def get(self,request):
        certifications = models.certification.objects.filter(user=request.user).values("id","title","school","issue_date","cert_id","skills").order_by("-issue_date")
        return Response(certifications,status=status.HTTP_200_OK)

    def delete(self,request):
        serializer = serializers.DeleteCertificationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            id = serializer.validated_data["id"]
            if models.certification.objects.filter(user=request.user,id=id).exists():
                models.certification.objects.get(user=request.user,id=id).delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                raise ValidationError({"Error":"Certificate does not exist!"})
        










class TestView(APIView):
    permission_classes=[
                AllowAny,
            ]
    serializer_class = serializers.TestSerializer

    def get(self,request):
        items = models.Test.objects.all().values("id","file").order_by("id")
        paginator = ItemPagination()
        paginated_items = paginator.paginate_queryset(items,request)
        serializer = self.serializer_class(paginated_items,many=True)

        total_items = items.count()
        floor = total_items//paginator.page_size
        if total_items % paginator.page_size == 0:
            total_pages = floor
        else:
            total_pages = floor + 1

        response_data = paginator.get_paginated_response(serializer.data).data
        response_data["last_page"] = f"?page={total_pages}"
        return Response(response_data,status=status.HTTP_200_OK)


def CallTestView(request):
    url = "http://127.0.0.1:8000/user/test/"
    #own_url = "http://127.0.0.1:8000/user/calltest/"
    page = request.GET.get('page',1)

    response = requests.get(f"{url}?page={page}")

    if response.status_code == 200:
        response_data = response.json()
        items = response_data.get('results',[])
        next_page = response_data.get('next',None)
        previous_page = response_data.get('previous',None)
        first_page = f"?page=1"
        last_page = response_data.get("last_page")
    else:
        items = []
        first_page = 1
        next_page=None
        previous_page=None
        last_page=1

    context = {
                "items":items,
                "next_page":next_page,
                "previous_page":previous_page,
                "first_page":first_page,
                "last_page":last_page,
                "current_page":page
            }

    return render(request,"data.html",context=context)
