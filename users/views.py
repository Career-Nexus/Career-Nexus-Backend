from django.http import Http404
from django.shortcuts import render
from django.core.cache import cache
#import email
import os
from django.utils.html import strip_tags
import requests

from django.utils.ipv6 import is_valid_ipv6_address
from requests.api import delete
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.pagination import PageNumberPagination
from rest_framework.exceptions import ValidationError
from drf_yasg.utils import swagger_auto_schema


from . import serializers
from . import models
from .mmail import Agent
from notifications.utils import notify

from django.contrib.auth import get_user_model

User = get_user_model()

agent = Agent()

default_profile_photo = "https://careernexus-storage1.s3.amazonaws.com/profile_pictures/ad7b2bc0-98b2-4d29-bc90-3d784ce22cc9career_nexus_default_dp.png"
default_cover_photo = "https://careernexus-storage1.s3.amazonaws.com/profile_pictures/ad7b2bc0-98b2-4d29-bc90-3d784ce22cc9career_nexus_default_dp.png"
default_intro_video = ''


def delete_cache(key):
    #print("Tried")
    if cache.get(key):
        cache.delete(key)
        #print(f"LOG:DELETED CACHE FOR {key}")




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








class WaitListView(APIView):
    serializer_class = serializers.WaitListSerializer
    permission_classes = [
            AllowAny,
            ]
    @swagger_auto_schema(request_body=serializer_class,operation_description="Allows users to be added to the WaitList.")
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

    @swagger_auto_schema(request_body=serializer_class,operation_description="Allows users to subscribe to NewsLetter.")

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
    @swagger_auto_schema(request_body=serializer_class,operation_description="Allows users to Unsubscribe from the NewsLetter.")
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

    @swagger_auto_schema(request_body=serializer_class,operation_description="Allows users to register into the main platform with a valid email.")
    def post(self,request):
        serializer =self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            data = serializer.save()
            if data != {"status":"Otp sent"}:
                refresh = RefreshToken.for_user(data)
                response = {
                    "refresh":str(refresh),
                    "access":str(refresh.access_token),
                    "user":data.email,
                    "status":"Success"
                }

                return Response(response,status=status.HTTP_201_CREATED)
            else:
                return Response(data,status=status.HTTP_201_CREATED)

    #TODO REMOVE THIS IN PRODUCTION-------------------------
    def delete(self,request):
        email = request.query_params.get("email",None)
        try:
            models.Users.objects.get(email=email).delete()
            return Response({"Deleted":email},status=status.HTTP_204_NO_CONTENT)
        except:
            return Response({"error":f"{email} not registered"},status=status.HTTP_404_NOT_FOUND)


class VerifyHashView(APIView):
    permission_classes = [
        AllowAny,
    ]
    serializer_class = serializers.VerifyHashSerializer

    def post(self,request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            output = {
                "refresh":str(refresh),
                "access":str(refresh.access_token),
                "email":str(user.email),
                "status":"Success"
            }
            return Response(output,status=status.HTTP_201_CREATED)


class ForgetPasswordView(APIView):
    permission_classes = [
        AllowAny,
    ]
    serializer_class = serializers.ForgetPasswordSerializer

    def post(self,request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            output = serializer.save()
            return Response(output,status=status.HTTP_200_OK)



class LoginView(APIView):
    permission_classes = [
                AllowAny,
            ]
    serializer_class = serializers.LoginSerializer

    @swagger_auto_schema(request_body=serializer_class,operation_description="Authenticates registered users within the platform and returns a Bearer token for subsequent requests. N.B:Token expires in 6 hours.")
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

    @swagger_auto_schema(request_body=serializer_class,operation_description="Logs out signed in users and blacklists the Bearer Token.")
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
    @swagger_auto_schema(request_body=serializers.PersonalProfileSerializer, operation_description="Allows user to update the profile parameters qualification, summary, profile_photo and intro_video.")
    def put(self,request):
        user = self.get_object(request)
        serializer = self.serializer_class(instance=user,data=request.data)
        if serializer.is_valid(raise_exception=True):
            output = serializer.save()
            cache_key = f"{request.user.id}_profile"
            delete_cache(cache_key)
            return Response(output,status=status.HTTP_201_CREATED)

    @swagger_auto_schema(request_body=serializers.PostRegistrationSerializer,operation_description="Allows users to update profile parameters User_type and Industry.")
    def patch(self,request):
        user = models.Users.objects.filter(email=request.user.email).first()
        serializer = serializers.PostRegistrationSerializer(data=request.data,instance=user,partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            industry = serializer.data.get("industry")
            output = {
                        "industry":industry,
                        "email":user.email
                    }
            cache_key = f"{request.user.id}_profile"
            delete_cache(cache_key)
            return Response(output,status=status.HTTP_206_PARTIAL_CONTENT)





class RetreiveProfileView(APIView):
    permission_classes = [
                IsAuthenticated,
            ]
    def get_user(self,request):
        try:
            user =models.Users.objects.get(email=request.user.email)
            return user
        except:
            raise Http404({"error":"Inexistent User"})

    @swagger_auto_schema(operation_description="Retrieves User complete profile including their work experience, education and certification.")
    def get(self,request):
        param = request.query_params.get("user_id")
        if not param:
            cache_key = f"{request.user.id}_profile"
            cached_data = cache.get(cache_key)
            if not cached_data:
                user = self.get_user(request)
                profile = models.PersonalProfile.objects.get(user=user)
                output = serializers.RetrieveAnotherProfileSerializer(profile).data
                cache.set(cache_key,output,timeout=7200)
                #notify(user.id,f"profile for {user.email} was successfully retrieved")
                return Response(output,status=status.HTTP_200_OK)
            else:
                #print(cache_key)
                return Response(cached_data,status=status.HTTP_200_OK)
        else:
            try:
                user = models.Users.objects.get(id=param)
            except:
                raise Http404({"error":"Invalid User Id"})

            cache_key = f"{user.id}_profile"
            cached_data = cache.get(cache_key)
            if not cached_data:
                profile = models.PersonalProfile.objects.get(user=user)

                #Implementation profile viewing counter 
                models.ProfileView.objects.create(viewer=request.user,viewed=user)
                profile_data = serializers.RetrieveAnotherProfileSerializer(profile,many=False).data
                cache.set(cache_key,profile_data,timeout=7200)
                return Response(profile_data,status=status.HTTP_200_OK)
            else:
                return Response(cached_data,status=status.HTTP_200_OK)







class ExperienceView(APIView):
    permission_classes= [
                IsAuthenticated,
            ]
    serializer_class= serializers.ExperienceSerializer
    
    @swagger_auto_schema(operation_description="Gets all the Experience data for the logged in user.")
    def get(self,request):
        user_id = request.user.id
        data = models.experience.objects.filter(user_id=user_id).values("id","title","organization","start_date","end_date","location","employment_type","detail").order_by("-start_date")
        return Response(data,status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=serializer_class,operation_description="Allows creation of new work experience.")
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
            cache_key = f"{request.user.id}_profile"
            delete_cache(cache_key)
            return Response(output,status=status.HTTP_201_CREATED)
    def delete(self,request):
        param = request.query_params.get("experience_id")
        if not param:
            return Response({"error":"No query parameter"},status=status.HTTP_400_BAD_REQUEST)
        else:
            try:
                experience_instance = models.experience.objects.get(user=request.user,id=param)
                experience_instance.delete()
                cache_key = f"{request.user.id}_profile"
                delete_cache(cache_key)
                return Response(status=status.HTTP_204_NO_CONTENT)
            except:
                raise Http404("Inexistent experience")






class UpdateExperienceView(APIView):
    permission_classes= [
                IsAuthenticated,
            ]
    serializer_class = serializers.UpdateExperienceSerializer

    @swagger_auto_schema(request_body=serializer_class,operation_description="Updates data in a user work experience.")
    def put(self,request):
        serializer = self.serializer_class(data=request.data,instance=request.user,context={"request":request})
        if serializer.is_valid(raise_exception=True):
            output = serializer.save()
            cache_key = f"{request.user.id}_profile"
            delete_cache(cache_key)
            return Response(output,status=status.HTTP_201_CREATED)






class EducationView(APIView):
    permission_classes= [
                IsAuthenticated,
            ]
    serializer_class = serializers.EducationSerializer

    @swagger_auto_schema(request_body=serializer_class,operation_description="Creates a new Education data for the user.")
    def post(self,request):
        serializer = self.serializer_class(data=request.data,context={"request":request.user})
        if serializer.is_valid(raise_exception=True):
            output = serializer.save()
            cache_key = f"{request.user.id}_profile"
            delete_cache(cache_key)
            return Response(output,status=status.HTTP_201_CREATED)

    @swagger_auto_schema(operation_description="Retrieves all Education data for the logged in user.")
    def get(self,request):
        detail = models.education.objects.filter(user_id=request.user.id).values("id","course","school","start_date","end_date","location","detail").order_by("-start_date")
        return Response(detail,status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=serializer_class,operation_description="Updates Education data of the user.")
    def put(self,request):
        serializer = serializers.UpdateEducationSerializer(data=request.data,instance=request.user,context={"request":request})
        if serializer.is_valid(raise_exception=True):
            output = serializer.save()
            cache_key = f"{request.user.id}_profile"
            delete_cache(cache_key)
            return Response(output,status=status.HTTP_201_CREATED)

    @swagger_auto_schema(request_body=serializers.UpdateEducationSerializer,operation_description="Deletes an education entry of the user.")

    def delete(self,request):
        user = request.user
        param = request.query_params.get("education_id",None)
        if not param:
            return Response({"error":"No query parameter specified"},status=status.HTTP_400_BAD_REQUEST)
        else:
            try:
                education_instance = models.education.objects.get(user=user,id=param)
                education_instance.delete()
                cache_key = f"{request.user.id}_profile"
                delete_cache(cache_key)

                return Response(status=status.HTTP_204_NO_CONTENT)
            except:
                raise Http404("Inexistent education")



class CertificationView(APIView):
    permission_classes = [
                IsAuthenticated,
            ]
    serializer_class = serializers.CertificationSerializer

    @swagger_auto_schema(request_body=serializer_class,operation_description="Creates a new certification data for the user.")
    def post(self,request):
        serializer = self.serializer_class(data=request.data,context={"request":request})
        if serializer.is_valid(raise_exception=True):
            output = serializer.save()
            cache_key = f"{request.user.id}_profile"
            delete_cache(cache_key)
            return Response(output,status=status.HTTP_201_CREATED)

    @swagger_auto_schema(operation_description="Retrieves all certificates of the logged in user.")
    def get(self,request):
        certifications = models.certification.objects.filter(user=request.user).values("id","title","school","issue_date","cert_id","skills").order_by("-issue_date")
        return Response(certifications,status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=serializers.DeleteCertificationSerializer, operation_description="Allows for user to delete a certification data through certification id.")
    #TODO Resolve delete to use query parameter rather than sending the request in body.
    def delete(self,request):
        param = request.query_params.get("certification_id")
        user = request.user
        if not param:
            return Response({"error":"No query parameter specified"},status=status.HTTP_400_BAD_REQUEST)
        else:
            try:
                certification_instance = models.certification.objects.get(user=user,id=param)
                certification_instance.delete()
                cache_key = f"{request.user.id}_profile"
                delete_cache(cache_key)
                return Response(status=status.HTTP_204_NO_CONTENT)
            except:
                raise Http404("Inexistent certification")


class AnalyticsView(APIView):
    permission_classes = [
        IsAuthenticated,
    ]
    serializer_class = serializers.AnalyticsSerializer
    def get(self,request):
        profile = request.user.profile
        serializer = self.serializer_class(profile).data
        return Response(serializer,status=status.HTTP_200_OK)






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

class WizardView(APIView):
    permission_classes = [
        IsAuthenticated,
    ]
    def get(self,request):
        user = request.user
        user_profile = user.profile
        completion = 0
        complete = []
        incomplete = []
        if user_profile.profile_photo == default_profile_photo:
            incomplete.append("profile_photo")
        else:
            completion += 15
            complete.append("profile_photo")

        if user_profile.intro_video == default_intro_video:
            incomplete.append("intro_video")
        else:
            completion += 15
            complete.append("intro_video")

        work_experience_count = user.experience_set.count()
        if work_experience_count == 0:
            incomplete.append("experience")
        else:
            completion += 20
            complete.append("experience")

        certification_count = user.certification_set.count()
        if certification_count == 0:
            incomplete.append("certification")
        else:
            completion += 15
            complete.append("certification")
        if user.profile.bio == '':
            incomplete.append("bio")
        else:
            completion += 15
            complete.append("bio")
        if user.education_set.count() == 0:
            incomplete.append("education")
        else:
            completion += 20 
            complete.append("education")

        output = {
            "completion":completion,
            "incomplete_items":incomplete,
            "complete_items":complete
        }

        return Response(output,status=status.HTTP_200_OK)

        
