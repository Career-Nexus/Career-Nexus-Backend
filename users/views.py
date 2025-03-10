#from django.shortcuts import render
import email
import os

from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken


from . import serializers
from . import models
from .mmail import Agent

from django.contrib.auth import get_user_model

User = get_user_model()

agent = Agent()


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
