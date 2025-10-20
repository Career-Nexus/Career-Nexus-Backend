from random import choice
from django.utils.timezone import make_aware
from django.contrib.auth import get_user_model
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.db.models import Q

from django.db import transaction


from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import serializers
from . import models
from follows.models import UserFollow
from info.models import ExchangeRate


from .generator.referral_code_generator import *
from .Hasher import hasher

from .tasks import send_email
from .options import get_choices
from datetime import datetime
import os
import uuid
import boto3


ref_agent = generator()
hasher = hasher()


#Defining Email Templates
c_directory = os.path.dirname(os.path.abspath(__file__))
resources_directory = os.path.join(c_directory,"resources")

otp_template = os.path.join(resources_directory,"mail_otp.html")
password_reset_template = os.path.join(resources_directory,"forgetpassword_otp.html")

CHOICES = get_choices()

#Defining Choice Fields

user_options = CHOICES["user"]

industry_options = CHOICES["industry"]

employment_type_options = CHOICES["employment_type"]

availability_options = CHOICES["availability"]

timezones_choices = CHOICES["timezones"]

company_type_options = CHOICES["company_type"]

company_size = CHOICES["company_size"]



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


class CorporateLeadsSerializer(serializers.Serializer):
    full_name = serializers.CharField()
    email_address = serializers.EmailField()
    phone_number = serializers.CharField()
    interested_services = serializers.JSONField()
    package = serializers.ChoiceField(choices=models.packages_options,required=False)

    def validate_email_address(self,value):
        if models.CorporateLeads.objects.filter(email_address=value).exists():
            raise serializers.ValidationError("This email already exists")
        return value

    def validate_interested_services(self,value):
        if not isinstance(value,list):
            raise serializers.ValidationError("Interested services must be a list")
        return value

    def create(self,validated_data):
        output_instance = models.CorporateLeads.objects.create(**validated_data)
        return output_instance






#Main App Serializers begins here
class RegisterSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=300)
    industry = serializers.ChoiceField(choices=industry_options,required=False)
    password1 = serializers.CharField(max_length=200)
    password2 = serializers.CharField(max_length=200)
    otp = serializers.CharField(max_length=20,required=False)

    def validate_email(self,value):
        if models.Users.objects.filter(email=value.strip().lower()).exists():
            raise serializers.ValidationError("Existing Email!")
            #return value
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
        email = validated_data.get("email").strip().lower()
        username = uuid.uuid4()
        password1 = validated_data.get("password1")
        otp = validated_data.get("otp",None)
        industry = validated_data.get("industry")

        if otp == None:
            ref_code_generated = ref_agent.generate_otp()
            ref_code_hash = str(uuid.uuid4())
            container = {"{OTP}":ref_code_generated,"{HASH}":ref_code_hash}
            #print(ref_code_generated)
            send_email.delay(template=otp_template,subject="Verify your Email",container=container,recipient=email)
            models.Otp.objects.create(otp=ref_code_generated,hash=ref_code_hash,username=username,email=email,password=password1)
            output = {"status":"Otp sent"}
            return output
        else:
            if models.Otp.objects.filter(otp=otp).exists():
                otp_obj = models.Otp.objects.get(otp=otp)
                otp_time = otp_obj.time_stamp
                current_time = make_aware(datetime.now())
                time_diff = (current_time - otp_time).total_seconds()/60
                if time_diff > 5:
                    models.Otp.objects.filter(email=email).delete()
                    raise serializers.ValidationError({"OTP Error":"Expired OTP"})
                else:
                    models.Otp.objects.filter(email=email).delete()
                    #If industry is not specified at registeration, default user_type to learner
                    with transaction.atomic():
                        if not industry:
                            user_obj = models.Users.objects.create_user(
                                    email= email.lower(),
                                    username = str(username),
                                    password = password1
                                    )
                        else:
                            #If industry is specified at registeration, create user as a mentor.
                            user_obj = models.Users.objects.create_user(
                                email=email.lower(),
                                username = str(username),
                                password = password1,
                                user_type = "mentor",
                                industry = industry
                            )
                        models.PersonalProfile.objects.create(user=user_obj)
                    output = user_obj
                    return output
            else:
                raise serializers.ValidationError({"OTP Error":"Invalid OTP"})



class PostRegistrationSerializer(serializers.ModelSerializer):
    #user_type = serializers.ChoiceField(choices=user_options)
    industry = serializers.ChoiceField(choices=industry_options)

    class Meta:
        model = models.Users
        fields=["industry"]

class VerifyHashSerializer(serializers.Serializer):
    hash = serializers.CharField(max_length=300)

    def validate(self,data):
        hash_str = data.get("hash")
        hash = models.Otp.objects.filter(hash=hash_str)
        if hash.exists():
            current_time = make_aware(datetime.now())
            hash_created_at = hash.first().time_stamp
            time_diff = (current_time - hash_created_at).total_seconds()/60
            if time_diff < 5:
                data["email"] = hash.first().email
                data["password"] = hash.first().password
                data["username"] = hash.first().username
                models.Otp.objects.filter(email=hash.first().email).delete()
                return data
            else:
                models.Otp.objects.filter(email=hash.first().email).delete()
                raise serializers.ValidationError("Link Expired")
        else:
            raise serializers.ValidationError("Invalid Link")
    
    def create(self,validated_data):
        email = validated_data.get("email")
        password = validated_data.get("password")
        username = validated_data.get("username")
        with transaction.atomic():
            user = models.Users.objects.create_user(email=email.lower(),password=password,username=username)
            models.PersonalProfile.objects.create(user=user)
        return user


class CreateCorporateAccountSerializer(serializers.Serializer):
    company_name = serializers.CharField(max_length=500)
    company_email = serializers.EmailField()
    company_type = serializers.ChoiceField(choices=company_type_options)
    company_size = serializers.ChoiceField(choices=company_size)
    industry = serializers.ChoiceField(choices=industry_options)
    website = serializers.CharField()
    location = serializers.CharField()
    logo = serializers.ImageField(required=False)
    tagline = serializers.CharField()

    def validate_company_email(self,value):
        if models.Users.objects.filter(email=value).exists():
            raise serializers.ValidationError("An account with this email already exists.")
        return value

    def validate_logo(self,file):
        if not file.name.endswith((".png",".jpeg",".jpg")):
            raise serializers.ValidationError("Invalid File format")
        if file.size/1000000 > 2:
            raise serializers.ValidationError("File too large")
        return file

    def create(self,validated_data):
        user = self.context["user"]
        email = validated_data.pop("company_email")
        industry = validated_data.pop("industry")

        logo = validated_data.get("logo")
        if logo:
            file_name = f"profile_photo/company_logo/{uuid.uuid4()}{logo.name}"
            file_path = default_storage.save(file_name,ContentFile(logo.read()))
            validated_data["logo"] = default_storage.url(file_path)

        with transaction.atomic():
            account = models.Users.objects.create_user(username=str(uuid.uuid4()),email=email,industry=industry,user_type="employer")
            validated_data["user"] = account
            models.PersonalProfile.objects.create(**validated_data)
            models.LinkedAccounts.objects.create(main_account=user,child=account)
        return account


class SwitchAccountSerializer(serializers.Serializer):
    account = serializers.PrimaryKeyRelatedField(queryset=models.Users.objects.all())

    def validate_account(self,value):
        user = self.context["user"]
        if user == value:
            raise serializers.ValidationError("You are currently logged in as this user.")
        if not models.LinkedAccounts.objects.filter(
            Q(main_account=user,child=value)|
            Q(main_account=value,child=user)
        ).exists():
            raise serializers.ValidationError("This account is not linked to your profile.")
        return value



    #email only --> sends otp
    #otp/hash only --> verifies request validity and sets database parameters accordingly.
#email and password1 and password2 --> Attempts to change password while carrying out time and status verification

class ForgetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=False)
    hash = serializers.CharField(max_length=200,required=False)
    otp = serializers.CharField(max_length=20,required=False)
    password1 = serializers.CharField(max_length=200,required=False)
    password2 = serializers.CharField(max_length=200,required=False)

    def validate(self,data):
        if data.get("email") and not data.get("password1") and not data.get("password2"):
            #Ensuring the email has been registered.
            if Users.objects.filter(email=data["email"]).exists():
                data["email"] = data["email"].strip().lower()
                return data
            else:
                raise serializers.ValidationError("Unregistered Email")
        elif data.get("otp"):
            otp = data.get("otp")
            otp_obj = models.Otp.objects.filter(otp=otp)
            if not otp_obj.exists():
                raise serializers.ValidationError("Invalid OTP")
            else:
                current_time = make_aware(datetime.now())
                otp_created = otp_obj.first().time_stamp
                if (current_time - otp_created).total_seconds()/60 > 5:
                    #Ensure cleanup
                    otp_obj.delete()
                    raise serializers.ValidationError("Expired OTP")
                else:
                    data["validated_email"] = otp_obj.first().email
                    otp_obj.delete()
                    return data
        elif data.get("hash"):
            hash = data.get("hash")
            hash_obj = models.Otp.objects.filter(hash=hash)
            if not hash_obj.exists():
                raise serializers.ValidationError("Invalid OTP")
            else:
                current_time = make_aware(datetime.now())
                hash_created = hash_obj.first().time_stamp
                if (current_time - hash_created).total_seconds()/60 >5:
                    #Ensure cleanup
                    hash_obj.delete()
                    raise serializers.ValidationError("Expired OTP")
                else:
                    data["validated_email"] = hash_obj.first().email
                    hash_obj.delete()
                    return data
            
        elif data.get("password1") and data.get("password2") and data.get("email"):
            password1 = data.get("password1")
            password2 = data.get("password2")
            email = data.get("email")
            user = Users.objects.filter(email=email).first()
            if user.change_password == False:
                raise serializers.ValidationError("Cannot change password. Request new otp.")
            current_time = make_aware(datetime.now())
            if (current_time-user.request_time).total_seconds()/60 > 5:
                user.change_password = False
                user.save()
                raise serializers.ValidationError("Expired Request")
            else:
                if password1 != password2:
                    raise serializers.ValidationError("Unmatched passwords")
                else:
                    validity = hasher.password_validity(password1)
                    if validity != True:
                        raise serializers.ValidationError(validity)
                    else:
                        return data
        else:
            raise serializers.ValidationError("Invalid Request!")


    def create(self,validated_data):
        email = validated_data.get("email")
        otp = validated_data.get("otp")
        hash = validated_data.get("hash")
        password1 = validated_data.get("password1")
        password2 = validated_data.get("password2")

        if email and not password1 and not password2:
            #Ensure email instance cleanup 
            models.Otp.objects.filter(email=email.lower()).delete()

            otp = ref_agent.generate_otp()
            hash = str(uuid.uuid4())
            otp_obj = models.Otp.objects.create(otp=otp,hash=hash,email=email)
            container = {"{OTP}":otp,"{HASH}":hash}
            send_email.delay(template=password_reset_template,subject="Password Reset Request",container=container,recipient=email)
            output = {
                "status":"Reset Password OTP sent.",
                "email":email
            }
            return output
        elif otp or hash:
            user = Users.objects.get(email=validated_data["validated_email"])
            user.change_password = True
            user.request_time = make_aware(datetime.now())
            user.save()
            output = {
                "status":"Verified",
                "email":validated_data["validated_email"]
            }
            return output
        elif email and password1 and password2:
            user = Users.objects.filter(email=email).first()
            user.set_password(password1)
            user.change_password = False
            user.save()
            output = {
                "status":"Password Changed",
                "email":email
            }
            return output






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
            return refresh_token
        except:
            raise serializers.ValidationError("Invalid Token")

class DeleteUserSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self,value):
        if models.Users.objects.filter(email=value).exists():
            return value
        else:
            raise serializers.ValidationError("Unregistered User")

#PROFILE SERIALIZERS ------------------------------------

class PersonalProfileSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=200,required=False)
    last_name = serializers.CharField(max_length=200,required=False)
    middle_name = serializers.CharField(max_length=200,required=False)
    country_code = serializers.CharField(max_length=20,required=False)
    phone_number = serializers.CharField(max_length=30,required=False)
    profile_photo = serializers.FileField(required=False)
    cover_photo = serializers.FileField(required=False)
    qualification = serializers.CharField(max_length=3000,required=False)
    intro_video = serializers.FileField(max_length=300,required=False)
    summary = serializers.CharField(max_length=5000,required=False)
    position = serializers.CharField(max_length=1000,required=False)
    location = serializers.CharField(max_length=1000,required=False)
    bio = serializers.CharField(max_length=4000,required=False)
    resume = serializers.FileField(required=False)
    timezone = serializers.ChoiceField(choices=timezones_choices,required=False)
    industry = serializers.ChoiceField(choices=industry_options,required=False)
    #Field options for mentors.
    years_of_experience = serializers.IntegerField(required=False)
    availability = serializers.ChoiceField(choices=availability_options,required=False)
    current_job = serializers.CharField(max_length=250,required=False)
    areas_of_expertise = serializers.JSONField(required=False)
    technical_skills = serializers.JSONField(required=False)
    mentorship_styles = serializers.JSONField(required=False)
    session_rate = serializers.IntegerField(required=False)
    linkedin_url = serializers.CharField(max_length=500,required=False)

    def validate_profile_photo(self,file):
        if not file.name.endswith((".png",".jpg",".jpeg")):
            raise serializers.ValidationError("Invalid file format")
        if (file.size/1000000) > 2:
            raise serializers.ValidationError("File too large.")
        return file


    def validate(self,data):
        areas_of_expertise = data.get("areas_of_expertise")
        technical_skills = data.get("technical_skills")
        mentorship_styles = data.get("mentorship_styles")
        container = [areas_of_expertise,technical_skills,mentorship_styles]
        for item in container:
            if item and not isinstance(item,list):
                raise serializers.ValidationError(f"{item} must be a list of values.")
        return data

    def validate_resume(self,file):
        size = file.size
        if size/1000000 > 5:
            raise serializers.ValidationError("File size too large.")
        return file

    def update(self,instance,validated_data):
        profile_photo = validated_data.get('profile_photo','')
        cover_photo = validated_data.get("cover_photo",'')
        qualification = validated_data.get('qualification',instance.qualification)
        intro_video = validated_data.get('intro_video','')
        summary = validated_data.get('summary',instance.summary)
        resume = validated_data.get("resume",'')


        instance.position = validated_data.get("position",instance.position)
        instance.location = validated_data.get("location",instance.location)
        instance.bio = validated_data.get("bio",instance.bio)
        instance.first_name = validated_data.get("first_name",instance.first_name)
        instance.last_name = validated_data.get("last_name",instance.last_name)
        instance.middle_name = validated_data.get("middle_name",instance.middle_name)
        instance.country_code = validated_data.get("country_code",instance.country_code)
        instance.phone_number = validated_data.get("phone_number",instance.phone_number)
        instance.timezone = validated_data.get("timezone",instance.timezone)
        
        #Make user industry updateable via PUT while also avoiding always calling save when other data are updated
        selected_industry = validated_data.get("industry")
        if selected_industry:
            instance.user.industry = selected_industry
            instance.user.save()

        #Extra updates if instance is a mentor.
        if instance.user.user_type == "mentor":
            #Inferring the session rate currency from the user's phone country code
            session_rate = validated_data.get("session_rate",instance.session_rate)
            country_code = instance.country_code
            rate_instance = ExchangeRate.objects.filter(country__code=country_code).first()
            if not rate_instance:
                pass
            else:
                #Convert session rate to central value (dollars)
                session_rate = session_rate // rate_instance.exchange_rate


            years_of_experience = validated_data.get("years_of_experience",instance.years_of_experience)
            availability = validated_data.get("availability",instance.availability)
            current_job = validated_data.get("current_job",instance.current_job)
            areas_of_expertise = validated_data.get("areas_of_expertise",instance.areas_of_expertise)
            technical_skills = validated_data.get("technical_skills",instance.technical_skills)
            mentorship_styles = validated_data.get("mentorship_styles",instance.mentorship_styles)
            linkedin_url = validated_data.get("linkedin_url",instance.linkedin_url)


            instance.years_of_experience = years_of_experience
            instance.availability = availability
            instance.current_job = current_job
            instance.areas_of_expertise = areas_of_expertise
            instance.technical_skills = technical_skills
            instance.mentorship_styles = mentorship_styles
            instance.session_rate = session_rate

            instance.linkedin_url = linkedin_url
        

        if resume != '':
            file_name = f"resumes/{uuid.uuid4()}{resume.name}"
            file_path = default_storage.save(file_name,ContentFile(resume.read()))
            url = default_storage.url(file_path)
            resume = url
        else:
            resume = instance.resume


        if profile_photo != '':
            #TODO create auto-cleaning logic for profile photo that has been changed

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
            #TODO Create auto-cleaning logic for intro-videos that has been changed

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
        instance.resume = resume
        instance.save()
        if instance.user.user_type == "learner":
            output = LearnerUpdateOutputSerializer(instance,many=False).data
        else:
            output = MentorUpdateOutputSerializer(instance,many=False).data
        return output


class MentorUpdateOutputSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.PersonalProfile
        fields = ["first_name","last_name","middle_name","country_code","phone_number","profile_photo","cover_photo","qualification","intro_video","location","bio","position","summary","years_of_experience","availability","current_job","areas_of_expertise","technical_skills","resume","mentorship_styles","timezone","linkedin_url","session_rate"]




class LearnerUpdateOutputSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.PersonalProfile
        fields = ["first_name","last_name","middle_name","country_code","phone_number","profile_photo","cover_photo","qualification","intro_video","location","bio","position","summary","availability"]



class RetrieveAnotherProfileSerializer(serializers.ModelSerializer):
    experience = serializers.SerializerMethodField()
    education = serializers.SerializerMethodField()
    certification = serializers.SerializerMethodField()
    followers = serializers.SerializerMethodField()
    followings = serializers.SerializerMethodField()
    user_type = serializers.SerializerMethodField()
    industry = serializers.SerializerMethodField()

    class Meta:
        model = models.PersonalProfile
        fields = ["first_name","last_name","middle_name","country_code","phone_number","cover_photo","profile_photo","location","position","bio","qualification","intro_video","summary","experience","education","certification","followers","followings","resume","timezone","user_type","industry"]

    def get_industry(self,obj):
        return obj.user.industry

    def get_user_type(self,obj):
        return obj.user.user_type

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

class RetrieveMentorProfileSerializer(serializers.ModelSerializer):
    experience = serializers.SerializerMethodField()
    education = serializers.SerializerMethodField()
    certification = serializers.SerializerMethodField()
    followers = serializers.SerializerMethodField()
    followings = serializers.SerializerMethodField()
    user_type = serializers.SerializerMethodField()
    session_rate = serializers.SerializerMethodField()
    industry = serializers.SerializerMethodField()
    rating = serializers.SerializerMethodField()

    class Meta:
        model = models.PersonalProfile
        fields = ["first_name","last_name","middle_name","country_code","phone_number","cover_photo","profile_photo","location","position","bio","qualification","intro_video","summary","experience","education","certification","years_of_experience","availability","current_job","areas_of_expertise","technical_skills","mentorship_styles","resume","timezone","linkedin_url","followers","followings","session_rate","rating","user_type","industry"]

    def get_rating(self,obj):
        user = obj.user
        try:
            mentor_rating = user.rating
            ratings = mentor_rating.ratings
            average_rating = sum(ratings)//len(ratings)
            return average_rating
        except:
            return 0

    def get_industry(self,obj):
        return obj.user.industry

    def get_session_rate(self,obj):
        user = self.context.get("user")
        if not user:
            return f"{obj.session_rate}USD"
        else:
            country_code = obj.country_code
            rate_instance = ExchangeRate.objects.filter(country__code=country_code).first()
            if not rate_instance:
                return f"{obj.session_rate}USD"
            else:
                amount = int(rate_instance.exchange_rate*obj.session_rate)
                currency = rate_instance.currency_initials
                return f"{amount}{currency}"

    def get_user_type(self,obj):
        return obj.user.user_type

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


class RetrieveCorporateUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.PersonalProfile
        fields = ["id","company_name","company_type","company_size","country_code","phone_number","location","website","tagline","logo","cover_photo"]


class MiniUserSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    profile_photo = serializers.SerializerMethodField()
    extras = serializers.SerializerMethodField()

    class Meta:
        model = models.Users
        fields = ["id","name","profile_photo","extras"]

    def get_name(self,obj):
        if obj.user_type == "employer":
            return obj.profile.company_name
        return f"{obj.profile.first_name} {obj.profile.middle_name} {obj.profile.last_name}"

    def get_profile_photo(self,obj):
        if obj.user_type == "employer":
            return obj.profile.logo
        return obj.profile.profile_photo

    def get_extras(self,obj):
        if obj.user_type == "employer":
            return obj.profile.tagline
        return obj.profile.qualification


class LinkedAccountsSerializer(serializers.Serializer):
    account = serializers.SerializerMethodField()

    class Meta:
        model = models.LinkedAccounts
        fields = ["account"]

    def get_account(self,obj):
        user = self.context["user"]
        if obj.main_account == user:
            output = MiniUserSerializer(obj.child,many=False).data
        else:
            output = MiniUserSerializer(obj.main_account,many=False).data
        return output



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
        instance.save()

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
    total_connections = serializers.SerializerMethodField()
    class Meta:
        model = models.PersonalProfile
        fields = ["total_posts","total_views","total_connections"]

    def get_total_posts(self,obj):
        total_posts = obj.posts_set.all().count()
        return total_posts
    def get_total_views(self,obj):
        user_viewed = obj.user.viewed.all().count()
        return user_viewed
    def get_total_connections(self,obj):
        connections_by_user = obj.user.connection_user.filter(status="CONFIRMED").count()
        connections_toward_user = obj.user.connect.filter(status="CONFIRMED").count()
        connections_total = connections_by_user + connections_toward_user
        return connections_total



class SettingsSerializer(serializers.Serializer):
    email_notify = serializers.BooleanField(required=False)
    push_notify = serializers.BooleanField(required=False)
    message_notify = serializers.BooleanField(required=False)
    weekly_summary = serializers.BooleanField(required=False)
    job_alerts = serializers.BooleanField(required=False)
    marketing = serializers.BooleanField(required=False)
    show_email = serializers.BooleanField(required=False)
    show_activity = serializers.BooleanField(required=False)
    show_location = serializers.BooleanField(required=False)
    timezone = serializers.ChoiceField(choices=timezones_choices,required=False)

    def update(self,instance,validated_data):
        instance.email_notify = validated_data.get("email_notify",instance.email_notify)
        instance.push_notify = validated_data.get("push_notify",instance.push_notify)
        instance.message_notify = validated_data.get("message_notify",instance.message_notify)
        instance.weekly_summary = validated_data.get("weekly_summary",instance.weekly_summary)
        instance.job_alerts = validated_data.get("job_alerts",instance.job_alerts)
        instance.marketing = validated_data.get("marketing",instance.marketing)
        instance.show_email = validated_data.get("show_email",instance.show_email)
        instance.show_activity = validated_data.get("show_activity",instance.show_activity)
        instance.show_location = validated_data.get("show_location",instance.show_location)

        instance.profile.timezone = validated_data.get("timezone",instance.profile.timezone)

        instance.save()
        instance.profile.save()
        return instance


class RetrieveSettingsSerializer(serializers.ModelSerializer):
    timezone = serializers.SerializerMethodField()

    class Meta:
        model = models.Users
        fields = ["email_notify","push_notify","message_notify","weekly_summary","job_alerts","marketing","show_email","show_activity","show_location","timezone"]

    def get_timezone(self,obj):
        return obj.profile.timezone


class CreateDisputeTicketSerializer(serializers.Serializer):
    category = serializers.ChoiceField(choices=models.dispute_categories_options)
    priority = serializers.ChoiceField(choices=models.dispute_priority_options)
    message = serializers.CharField()

    def create(self,validated_data):
        validated_data["user"] = self.context["user"]
        output_instance = models.DisputeTickets.objects.create(**validated_data)
        return output_instance

class DisputeTicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.DisputeTickets
        fields = ["id","category","priority","message","status","admin_response","timestamp"]

class AnnotateDisputeTicketSerializer(serializers.Serializer):
    dispute = serializers.PrimaryKeyRelatedField(queryset=models.DisputeTickets.objects.all())
    status = serializers.ChoiceField(choices=models.dispute_status_options,required=False)
    response = serializers.CharField(required=False)

    def update(self,instance,validated_data):
        status = validated_data.get("status")
        response = validated_data.get('response')
        dispute = validated_data.get("dispute")
        if status:
            dispute.status = status
        if response:
            dispute.admin_response = response
        dispute.save()
        return dispute







class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Test
        fields = "__all__"


