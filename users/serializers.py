from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from . import models
from .generator.referral_code_generator import *

ref_agent = generator()


class WaitListSerializer(serializers.Serializer):
	name = serializers.CharField(max_length=200)
	email = serializers.EmailField()
	industry = serializers.CharField(max_length=240,required=False)
	ref_code = serializers.CharField(max_length=30,required=False)

	def validate_email(self,value):
		if models.WaitList.objects.filter(email=value).exists():
			user = models.WaitList.objects.get(email=value)
			if user.referral_code != "NA" and user.name != "NA":
				raise serializers.ValidationError("Existing Email")
		return value

	def validate_name(self,value):
		if value == "NA":
			raise serializers.ValidationError("NA is not recognized")
		else:
			return value

	def create(self,validated_data):
		name = self.validated_data.get("name")
		email = self.validated_data.get("email")
		industry = self.validated_data.get("industry","NA")
		ref_code = self.validated_data.get("ref_code","NA")
		ref_code_generated = ref_agent.generate()
		if ref_code != "NA":
			try:
				referee = models.WaitList.objects.get(referral_code=ref_code)
				referee.invites +=1
				referee.save()
			except:
				raise serializers.ValidationError("Invalid Referral Code")
		if models.WaitList.objects.filter(email=email).exists():
			user = models.WaitList.objects.get(email=email)
			user.name = name
			user.industry = industry
			user.referral_code = ref_code_generated
			user.save()
			return {
				"name":user.name,
				"email":user.email,
				"industry":user.industry,
				"ref_code":ref_code_generated,
				"status":"CREATED"
			}
		else:
			user = models.WaitList.objects.create(
			                                      name=name,
			                                      email=email,
			                                      industry=industry,
			                                      referral_code=ref_code_generated,
			                                      )
			return {
				"name":user.name,
				"email":user.email,
				"industry":user.industry,
				"ref_code":ref_code_generated,
				"status":"CREATED"
			}

class NewsLetterSubscribeSerializer(serializers.Serializer):
	email = serializers.EmailField()

	def validate_email(self,value):
		if models.WaitList.objects.filter(email=value).exists():
			user = models.WaitList.objects.get(email=value)
			if user.sub_status == True:
				raise serializers.ValidationError("Already Subscribed")
		return value

	def create(self,validated_data):
		email = validated_data.get("email")
		if models.WaitList.objects.filter(email=email).exists():
			user = models.WaitList.objects.get(email=email)
			user.sub_status = True
			user.save()
		else:
			models.WaitList.objects.create(
			                        name="NA",
			                        email=email,
			                        industry="NA",
			                        referral_code="NA",
			                        )
		return {"Status":"Subscribed Successfully"}

class NewsLetterUnsubscribeSerializer(serializers.Serializer):
	email = serializers.EmailField()

	def validate_email(self,value):
		if models.WaitList.objects.filter(email=value).exists():
			user = models.WaitList.objects.get(email=value)
			if user.sub_status == False:
				raise serializers.ValidationError("Already Unsubscribed")
			else:
				return value
		else:
			raise serializers.ValidationError("Unregistered Email")

	def update(self,instance,validated_data):
		instance.sub_status = False
		instance.save()

		return instance


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


class DeleteWaitListSerializer(serializers.Serializer):
	email = serializers.EmailField()

	def validate_email(self,value):
		if models.WaitList.objects.filter(email=value).exists():
			return value
		else:
			raise serializers.ValidationError("Unregistered User")