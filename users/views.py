from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework import status


from . import serializers
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
			first_name = data.name.split()[0]
			email = data.email
			ref_code = data.referral_code
			agent.send_waitlist_mail(recepient=email,name=first_name,ref_code=ref_code)
			return Response({
			                "name":data.name,
			                "email":data.email,
			                "industry":data.industry,
			                "status":"CREATED"
			                },status=status.HTTP_201_CREATED)


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