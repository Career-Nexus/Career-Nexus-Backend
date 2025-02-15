from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework import status


from . import serializers
from . import models
from .mailer import Mailer

from django.contrib.auth import get_user_model

User = get_user_model()
agent = Mailer()

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
			agent.send_waitlist_mail(recepient=email,name=first_name,ref_code=ref_code)
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
			output = {
				"username":data.username,
				"email":data.email,
				"status":"Created"
			}
			return Response(output,status=status.HTTP_201_CREATED)


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