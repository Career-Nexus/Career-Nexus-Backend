from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from . import models
from .generator.referral_code_generator import *

ref_agent = generator()


class WaitListSerializer(ModelSerializer):
	class Meta:
		model = models.WaitList
		fields = ["name","email","industry"]

	def create(self,validated_data):
		name = self.validated_data.get("name")
		email = self.validated_data.get("email")
		industry = self.validated_data.get("industry","NA")
		ref_code = ref_agent.generate()
		user = models.WaitList.objects.create(
		                                      name=name,
		                                      email=email,
		                                      industry=industry,
		                                      referral_code=ref_code,
		                                      )
		return user


class RegisterSerializer(ModelSerializer):
	class Meta:
		model = models.Users
		fields = ["first_name","last_name","username","email","password","password2"]

	def validate(self,data):
		password1 = data.get("password",None)
		password2 = data.get("password2",None)
		if password1 == None or password2 == None:
			raise serializers.ValidationError({"password error":"Password field cannot be empty"})
		elif len(password1) < 7 or len(password2) < 7:
			raise serializers.ValidationError({"Weak Password":"password must exceed 7 characters"})
		elif password1 != password2:
			raise serializers.ValidationError({"Password Mismatch":"Passwords must be the same"})
		else:
			return data