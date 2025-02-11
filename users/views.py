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






class TestView(APIView):
	def get(self,request):
		return Response("Hello World",status=status.HTTP_200_OK)


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
			waitlist_success_message = f'''
			<html>
				<body>
					<h2 style="color: Green;">
						<b>
							Dear {first_name},
						</b>
					</h2>
					<h3>
						Congratulations on joining our waitlist.
						CareerNexus gives you an opportunity to grow your skill and better your qualification standings.
						Through our state of the act methodology in mentoring and upskilling individuals, you can be sure of developing valuable skills that you would surely find very useful to your professional journey.

						Our platform would be launching on the 31st of March, 2025. Don't forget to keep tabs on <a href="https://career-nexus-lp-ogqq.vercel.app/">our platform</a>

						See you then.

						<h3 style="color:Red">The CareerNexus Team</h3>
					</h3>
				</body>
			</html>
			'''

			output = {
				"name":data.name,
				"email":data.email,
				"industry":data.industry,
				"status":"Created"
			}
			agent.waitlist_mail(recepient=data.email,message=waitlist_success_message)
			return Response(output,status=status.HTTP_201_CREATED)


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