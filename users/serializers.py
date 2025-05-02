#from django.forms import fields
#from requests import request
#from requests.models import LocationParseError
#from typing_extensions import Required
from django.utils.timezone import make_aware
from django.contrib.auth import get_user_model
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

#from rest_framework.serializers import ModelSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import serializers
from . import models


from .generator.referral_code_generator import *
from .Hasher import hasher
#from .mmail import Agent
from .tasks import send_email
from datetime import datetime
import os
import uuid
import boto3

ref_agent = generator()
hasher = hasher()

#Defining Templates
c_directory = os.path.dirname(os.path.abspath(__file__))
resources_directory = os.path.join(c_directory,"resources")
otp_template = os.path.join(resources_directory,"mail_otp.html")




user_options = (("learner","learner"),("mentor","mentor"),("employer","employer"))

industry_options = (
    ("agriculture","agriculture"),
    ("banking","banking"),
    ("business","business"),
    ("commerce","commerce"),
    ("construction","construction"),
    ("education","education"),
    ("entertainment","entertainment"),
    ("government","government"),
    ("health","health"),
    ("manufacturing","manufacturing"),
    ("media","media"),
    ("others","others"),
    ("sports","sports"),
    ("technology","technology"),
    ("transportation","transportation")
)

employment_type_options = (
            ("Onsite","Onsite"),
            ("Remote","Remote"),
            ("Hybrid","Hybrid")
        )



Users = get_user_model()






#REGISTRATION AND AUTHENTICATION SERIALIZERS --------------------------
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


class RegisterSerializer(serializers.Serializer):
    #user_option = serializers.ChoiceField(choices=user_options)
    name = serializers.CharField(max_length=300)
    email = serializers.CharField(max_length=300)
    #username = serializers.CharField(max_length=150)
    password1 = serializers.CharField(max_length=200)
    password2 = serializers.CharField(max_length=200)
    otp = serializers.CharField(max_length=20,required=False)

    def validate_email(self,value):
        if models.Users.objects.filter(email=value.lower()).exists():
            raise serializers.ValidationError("Existing Email!")
        else:
            return value


    def validate(self,data):
        password1 = data.get("password1",None)
        password2 = data.get("password2",None)
        if password1 != None:
            validity = hasher.password_validity(password1)
        if password1 == None or password2 == None:
            raise serializers.ValidationError({"password error":"Password field cannot be empty"})
        elif validity != True:
            raise serializers.ValidationError(validity)
        elif password1 != password2:
            raise serializers.ValidationError({"Password Mismatch":"Passwords must be the same"})
        else:
            return data

    def create(self,validated_data):
        #user_type = validated_data.get("user_option")
        name = validated_data.get("name")
        email = validated_data.get("email")
        username = uuid.uuid4()
        password1 = validated_data.get("password1")
        otp = validated_data.get("otp",None)

        if otp == None:
            ref_code_generated = ref_agent.generate_otp()
            container = {"{OTP}":ref_code_generated}
            print(ref_code_generated)
            send_email.delay(template=otp_template,subject="Verify your Email",container=container,recipient=email)
            models.Otp.objects.create(otp=ref_code_generated)
            output = {"status":"Otp sent"}
            return output
        else:
            if models.Otp.objects.filter(otp=otp).exists():
                otp_obj = models.Otp.objects.get(otp=otp)
                otp_time = otp_obj.time_stamp
                current_time = make_aware(datetime.now())
                time_diff = (current_time - otp_time).total_seconds()/60
                if time_diff > 5:
                    otp_obj.delete()
                    raise serializers.ValidationError({"OTP Error":"Expired OTP"})
                else:
                    otp_obj.delete()
                    user_obj = models.Users.objects.create_user(
                            #user_type = user_type,
                            name = name,
                            email= email.lower(),
                            username = username,
                            password = password1
                            )
                    models.PersonalProfile.objects.create(user=user_obj,name=name)
                    output = {
                            "email":user_obj.email,
                            "status":"Success"
                            }
                    return output
            else:
                raise serializers.ValidationError({"OTP Error":"Invalid OTP"})

class PostRegistrationSerializer(serializers.ModelSerializer):
    user_type = serializers.ChoiceField(choices=user_options)
    industry = serializers.ChoiceField(choices=industry_options)

    class Meta:
        model = models.Users
        fields=["user_type","industry"]


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=250)
    password = serializers.CharField(max_length=200)

    def validate(self,data):
        email = data.get("email")
        password = data.get("password")
        user = Users.objects.filter(email=email.lower()).first()
        if user and user.check_password(password):
            return user
        else:
            raise serializers.ValidationError("Invalid Credentials")


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField(max_length=1000)

    def validate(self,data):
        refresh_token = data.get("refresh")
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            return refresh
        except:
            raise serializers.ValidationError("Invalid Token")

class DeleteWaitListSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self,value):
        if models.WaitList.objects.filter(email=value).exists():
            return value
        else:
            raise serializers.ValidationError("Unregistered User")

#PROFILE SERIALIZERS ------------------------------------

class PersonalProfileSerializer(serializers.Serializer):
    profile_photo = serializers.FileField(required=False)
    cover_photo = serializers.FileField(required=False)
    qualification = serializers.CharField(max_length=3000,required=False)
    intro_video = serializers.FileField(max_length=300,required=False)
    summary = serializers.CharField(max_length=5000,required=False)
    position = serializers.CharField(max_length=1000,required=False)
    location = serializers.CharField(max_length=1000,required=False)
    bio = serializers.CharField(max_length=4000,required=False)

    def update(self,instance,validated_data):
        profile_photo = validated_data.get('profile_photo','')
        cover_photo = validated_data.get("cover_photo",'')
        qualification = validated_data.get('qualification',instance.qualification)
        intro_video = validated_data.get('intro_video','')
        summary = validated_data.get('summary',instance.summary)

        instance.position = validated_data.get("position",instance.position)
        instance.location = validated_data.get("location",instance.location)
        instance.bio = validated_data.get("bio",instance.bio)

        if profile_photo != '':
            #create auto-cleaning logic for profile photo

            file_name = f"profile_pictures/{uuid.uuid4()}{profile_photo.name}"
            file_path = default_storage.save(file_name,ContentFile(profile_photo.read()))
            url = default_storage.url(file_path)
            profile_photo = url
            
        else:
            profile_photo = instance.profile_photo


        if cover_photo != '':
            file_name = f"cover_photos/{uuid.uuid4()}{cover_photo.name}"
            file_path = default_storage.save(file_name,ContentFile(cover_photo.read()))
            url = default_storage.url(file_path)
            cover_photo = url
        else:
            cover_photo = instance.cover_photo


        if intro_video != '':
            #Create auto-cleaning logic for intro-videos

            file_name = f"intro_videos/{uuid.uuid4()}{intro_video.name}"
            file_path = default_storage.save(file_name,ContentFile(intro_video.read()))
            url = default_storage.url(file_path)
            intro_video = url 
        else:
            intro_video = instance.intro_video

        instance.profile_photo = profile_photo
        instance.cover_photo = cover_photo
        instance.qualification = qualification
        instance.intro_video = intro_video
        instance.summary = summary
        instance.save()
        return {
                "profile_photo":instance.profile_photo,
                "cover_photo":instance.cover_photo,
                "qualification":instance.qualification,
                "intro_video":instance.intro_video,
                "location":instance.location,
                "bio":instance.bio,
                "position":instance.position,
                "summary":instance.summary
                }


class RetrieveAnotherProfileSerializer(serializers.ModelSerializer):
    experience = serializers.SerializerMethodField()
    education = serializers.SerializerMethodField()
    certification = serializers.SerializerMethodField()
    followers = serializers.SerializerMethodField()
    followings = serializers.SerializerMethodField()
    class Meta:
        model = models.PersonalProfile
        fields = ["name","cover_photo","profile_photo","location","position","bio","qualification","intro_video","summary","experience","education","certification","followers","followings"]

    def get_followings(self,obj):
        followings = len(obj.user.follower.all())
        return followings

    def get_followers(self,obj):
        followers = len(obj.user.following.all())
        return followers

    def get_experience(self,obj):
        experience = obj.user.experience_set.all().order_by("-start_date")
        data = ExperienceSerializer(experience,many=True).data
        return data

    def get_education(self,obj):
        education = obj.user.education_set.all().order_by("-start_date")
        data = EducationSerializer(education,many=True).data
        return data

    def get_certification(self,obj):
        certifications = obj.user.certification_set.all().order_by("-issue_date")
        data = CertificationSerializer(certifications,many=True).data
        return data




class RetrieveProfileSerializer(serializers.Serializer):
    profile_id = serializers.IntegerField()

    def validate(self,data):
        profile_id = data.get("profile_id")
        if models.PersonalProfile.objects.filter(id=profile_id).exists():
            return data
        else:
            raise serializers.ValidationError({"Error":"Profile does not exist"})


class ExperienceSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)


    title = serializers.CharField(max_length=150)
    organization = serializers.CharField(max_length=500)
    start_date = serializers.DateField()
    end_date = serializers.DateField(required=False)
    location = serializers.CharField(max_length=256)
    employment_type = serializers.ChoiceField(choices=employment_type_options)
    detail = serializers.CharField(max_length=2000)

    def validate(self,data):
        request = self.context["request"]
        data["user"] = request.user 
        return data

    def create(self,validated_data):
        user = validated_data.get("user")
        title = validated_data.get("title")
        organization = validated_data.get("organization")
        start_date = validated_data.get("start_date")
        end_date = validated_data.get("end_date","Present")
        location = validated_data.get("location")
        employment_type = validated_data.get("employment_type")
        detail = validated_data.get("detail")
        output = models.experience.objects.create(
                    user=user,
                    title=title,
                    organization=organization,
                    start_date=start_date,
                    end_date=end_date,
                    location=location,
                    employment_type=employment_type,
                    detail=detail,
                )
        return output

class UpdateExperienceSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=150,required=False)
    organization = serializers.CharField(max_length=500,required=False)
    start_date = serializers.DateField(required=False)
    end_date = serializers.DateField(required=False)
    location = serializers.CharField(max_length=256,required=False)
    employment_type = serializers.ChoiceField(choices=employment_type_options,required=False)
    detail = serializers.CharField(max_length=2000,required=False)

    def validate(self,data):
        request = self.context["request"]
        user = request.user
        id = data.get("id")
        if models.experience.objects.filter(user=user,id=id):
            return data
        else:
            raise serializers.ValidationError({"Error":"Experience does not exist"})

    def update(self,instance,validated_data):
        id = validated_data.get("id")
        instance = models.experience.objects.filter(user=instance,id=id).first()
        instance.title = validated_data.get("title",instance.title)
        instance.organization = validated_data.get("organization",instance.organization)
        instance.start_date = validated_data.get("start_date",instance.start_date)
        instance.end_date = validated_data.get("end_date",instance.end_date)
        instance.location = validated_data.get("location",instance.location)
        instance.employment_type = validated_data.get("employment_type",instance.employment_type)
        instance.detail = validated_data.get("detail",instance.detail)
        instance.save()
        return {
                    "id":instance.id,
                    "title":instance.title,
                    "organization":instance.organization,
                    "start_date":instance.start_date,
                    "end_date":instance.end_date,
                    "location":instance.location,
                    "employment_type":instance.employment_type,
                    "detail":instance.detail
                }
        

class EducationSerializer(serializers.ModelSerializer):
    end_date = serializers.DateField(required=False)
    class Meta:
        model = models.education
        fields = ["id","course", "school", "start_date","end_date","location","detail"]
        read_only_fields = ["id"]

    def validate(self,data):
        user = self.context["request"]
        data["user"] = user
        return data

    def create(self,validated_data):
        end_date = validated_data.get("end_date",None)
        if not end_date:
            validated_data["end_date"] = "Present"
        education = models.education.objects.create(**validated_data)
        output = {
                    "course":education.course,
                    "school":education.school,
                    "start_date":education.start_date,
                    "end_date": education.end_date,
                    "location": education.location,
                    "detail":education.detail
                }
        return output


class UpdateEducationSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    course = serializers.CharField(max_length=200,required=False)
    school = serializers.CharField(max_length=250,required=False)
    start_date = serializers.CharField(max_length=20,required=False)
    end_date = serializers.CharField(max_length=20,required=False)
    location = serializers.CharField(max_length=200,required=False)
    detail = serializers.CharField(max_length=2000,required=False)

    def validate(self,data):
        request = self.context["request"]
        id = data["id"]
        user = request.user
        if models.education.objects.filter(user=user,id=id).exists():
            return data
        else:
            raise serializers.ValidationError({"Error":"Education does not exist!"})


    def update(self,instance,validated_data):
        id = validated_data.get("id")
        instance = models.education.objects.get(id=id)
        instance.course = validated_data.get("course",instance.course)
        instance.school = validated_data.get("school",instance.school)
        instance.start_date = validated_data.get("start_date",instance.start_date)
        instance.end_date = validated_data.get("end_date",instance.end_date)
        instance.location = validated_data.get("location",instance.location)
        instance.detail = validated_data.get("detail",instance.detail)

        output= {
                    "id":instance.id,
                    "course":instance.course,
                    "school":instance.school,
                    "start_date":instance.start_date,
                    "end_date":instance.end_date,
                    "location":instance.location,
                    "detail":instance.detail
                }
        return output


class CertificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.certification
        fields = ["id","title","school","issue_date","cert_id","skills"]

        read_only_fields = ["id"]

    def validate(self,data):
        request = self.context["request"]
        data["user"] = request.user
        return data

    def create(self,validated_data):
        certification = models.certification.objects.create(**validated_data)
        output = {
                    "title":certification.title,
                    "school":certification.school,
                    "issue_date":certification.issue_date,
                    "cert_id":certification.cert_id,
                    "skills":certification.skills
                }
        return output

class DeleteCertificationSerializer(serializers.Serializer):
    id = serializers.IntegerField()

class AnalyticsSerializer(serializers.ModelSerializer):
    total_posts = serializers.SerializerMethodField()
    total_views = serializers.SerializerMethodField()
    class Meta:
        model = models.PersonalProfile
        fields = ["total_posts","total_views"]

    def get_total_posts(self,obj):
        total_posts = obj.posts_set.all().count()
        return total_posts
    def get_total_views(self,obj):
        user_viewed = obj.user.viewed.all().count()
        return user_viewed



class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Test
        fields = "__all__"
