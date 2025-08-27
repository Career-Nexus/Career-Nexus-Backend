from shutil import register_unpack_format
from django.utils.timezone import make_aware
from rest_framework import serializers
from rest_framework.response import Serializer


from users.options import get_choices
from users.models import PersonalProfile,Users
from posts.serializers import PersonalProfileSerializer
from info.models import ExchangeRate
from notifications.utils import send_notification

from . import models

from datetime import datetime,timedelta,date,time
import pytz
import uuid

CHOICES = get_choices()


def split_datetime_into_components(datetime):
    return [datetime.date(),datetime.time()]



experience_level_choices= CHOICES["experience_level"]
availability_options = CHOICES["availability"]
session_categories = CHOICES["session_categories"]

session_actions = (
    ("Accept","Accept"),
    ("Reject","Reject")
)



class RetrieveMentorsSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    qualification = serializers.SerializerMethodField()
    position = serializers.SerializerMethodField()
    years_of_experience = serializers.SerializerMethodField()
    technical_skills = serializers.SerializerMethodField()

    class Meta:
        model = Users
        fields = ["id","name","qualification","position","years_of_experience","technical_skills"]

    def get_name(self,obj):
        return f"{obj.profile.first_name} {obj.profile.middle_name} {obj.profile.last_name}"

    def get_qualification(self,obj):
        return obj.profile.qualification

    def get_position(self,obj):
        return obj.profile.position

    def get_years_of_experience(self,obj):
        return obj.profile.years_of_experience

    def get_technical_skills(self,obj):
        return obj.profile.technical_skills





class MentorRecommendationSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    is_saved = serializers.SerializerMethodField()
    session_rate = serializers.SerializerMethodField()

    class Meta:
        model = PersonalProfile
        fields = ["id","first_name","last_name","middle_name","profile_photo","current_job","years_of_experience","technical_skills","session_rate","is_saved"]

    def get_session_rate(self,obj):
        session_rate = obj.session_rate
        user = self.context["user"]
        rate_instance = ExchangeRate.objects.filter(country__code=user.profile.country_code).first()
        if not rate_instance:
            return f"{session_rate}USD"
        else:
            amount = int(rate_instance.exchange_rate*session_rate)
            currency = rate_instance.currency_initials
            return f"{amount}{currency}"

    def get_id(self,obj):
        return obj.user.id

    def get_is_saved(self,obj):
        user = self.context.get("user")
        if models.SavedMentors.objects.filter(saver=user,saved=obj.user).exists():
            return True
        else:
            return False




class MentorSearchAndFilterSerializer(serializers.Serializer):
    text = serializers.CharField(max_length=1000,required=False)
    experience_level = serializers.ChoiceField(choices=experience_level_choices,required=False)
    skills = serializers.CharField(max_length=500,required=False)
    availability = serializers.ChoiceField(choices=availability_options,required=False)



class CreateMentorshipSessionSerializer(serializers.Serializer):
    mentor = serializers.PrimaryKeyRelatedField(queryset=Users.objects.all())
    session_type = serializers.ChoiceField(choices=session_categories)
    date = serializers.DateField()
    time = serializers.TimeField()
    discourse = serializers.CharField()

    def validate_mentor(self,value):
        if Users.objects.filter(id=value.id).first().user_type != "mentor":
            raise serializers.ValidationError("This User is not a mentor.")
        return value

    def validate(self,data):
        user = self.context["user"]
        if user == data["mentor"]:
            raise serializers.ValidationError("Cannot schedule a mentorship session with yourself.")

        user_timezone = user.profile.timezone
        date = data.get("date")
        time = data.get("time")
        if not data or not time:
            raise serializers.ValidationError("A Date and time must be set when booking sessions.")
        if date.today() > date:
            raise serializers.ValidationError("Cannot set a mentorship date in the past.")

        #Combine the User set date and time to a datetime object
        naive_datetime = datetime.combine(date=date,time=time)
        #Set the user datetime object to the user timezone aware object.
        try:
            timezone = pytz.timezone(user_timezone)
        except:
            raise serializers.ValidationError("User Profile has an Invalid timezone.")
        aware_time = timezone.localize(naive_datetime)
        #Convert the User timezone aware datetime to a central timezone for storage."UTC"
        central_time = aware_time.astimezone(pytz.UTC)

        #Remove unncessary data
        data.pop("date")
        data.pop("time")

        data["session_at"] = central_time
        data["mentee"] = user
        return data

    def create(self,validated_data):
        mentee = validated_data.get("mentee")
        mentor = validated_data.get("mentor")
        validated_data["room_name"] = f"Room_{mentee.id}_{mentor.id}_{uuid.uuid4()}"

        session_instance = models.Sessions.objects.create(**validated_data)

        send_notification(session_instance.mentor, f"{session_instance.mentee.profile.first_name} {session_instance.mentee.profile.last_name} requested a mentorship session from you.")

        return session_instance


class AcceptRejectMentorshipSessionSerializer(serializers.Serializer):
    session = serializers.PrimaryKeyRelatedField(queryset=models.Sessions.objects.all())
    action = serializers.ChoiceField(choices=session_actions)

    def validate(self,data):
        user = self.context["user"]
        session = data.get("session")
        if user.user_type != "mentor":
            raise serializers.ValidationError("Only a mentor can Acept/Reject sessions")
        if session.mentor != user:
            raise serializers.ValidationError("This session was not initiated for you.")
        if session.status == "ACCEPTED":
            raise serializers.ValidationError("This session has already been accepted")
        return data

    def create(self,validated_data):
        action = validated_data.get("action")
        session = validated_data.get("session")
        session_id = session.id
        if action == "Reject":
            send_notification(session.mentee,f"Mentor {session.mentor.profile.first_name} {session.mentor.profile.last_name} rejected your mentorship request.")
            session.delete()
        else:
            send_notification(session.mentee,f"Mentor {session.mentor.profile.first_name} {session.mentor.profile.last_name} accepted your mentorship request.")
            session.status = "ACCEPTED"
            session.save()
        return {
            "session_id":session_id,
            "action":f"{action}ed"
        }



class SessionRetrieveSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    mentor = serializers.SerializerMethodField()
    mentee = serializers.SerializerMethodField()
    join = serializers.SerializerMethodField()
    session_type = serializers.CharField()
    session_at = serializers.SerializerMethodField()
    discourse = serializers.CharField()
    amount = serializers.SerializerMethodField()
    status = serializers.CharField()
    is_paid = serializers.BooleanField()

    def get_amount(self,obj):
        mentor_rate = obj.mentor.profile.session_rate
        user = self.context["user"]
        rate_instance = ExchangeRate.objects.filter(country__code=user.profile.country_code).first()
        if rate_instance:
            amount = int(rate_instance.exchange_rate * mentor_rate)
            currency = rate_instance.currency_initials
            return f"{amount}{currency}"
        else:
            return f"{mentor_rate}USD"

    def get_join(self,obj):
        if obj.status != "PENDING" and obj.is_paid:
            utc = pytz.timezone("UTC")
            present = utc.localize(datetime.now())
            session_at = obj.session_at
            if session_at > present:
                return False
            else:
                return True
        return False



    def get_mentor(self,obj):
        output = PersonalProfileSerializer(obj.mentor.profile,many=False).data
        return output

    def get_mentee(self,obj):
        user = self.context["user"]
        output = PersonalProfileSerializer(obj.mentee.profile,many=False).data
        return output

    def get_session_at(self,obj):
        user = self.context["user"]
        user_tz = user.profile.timezone
        utc_tz = obj.session_at
        try:
            output_tz = utc_tz.astimezone(pytz.timezone(user_tz))
        except:
            output_tz = utc_tz
        period = split_datetime_into_components(output_tz)
        output = {
            "date":period[0],
            "time":period[1]
        }
        return output


class RetrieveMentorSearchAndRetrieveSerializer(serializers.ModelSerializer):
    first_name = serializers.SerializerMethodField()
    last_name = serializers.SerializerMethodField()
    middle_name = serializers.SerializerMethodField()
    years_of_experience = serializers.SerializerMethodField()
    technical_skills = serializers.SerializerMethodField()
    current_job = serializers.SerializerMethodField()
    profile_photo = serializers.SerializerMethodField()

    class Meta:
        model = Users
        fields = ["id","first_name","last_name","middle_name","years_of_experience","technical_skills","current_job","profile_photo"]

    def get_first_name(self,obj):
        return obj.profile.first_name

    def get_last_name(self,obj):
        return obj.profile.last_name

    def get_middle_name(self,obj):
        return obj.profile.middle_name

    def get_years_of_experience(self,obj):
        return obj.profile.years_of_experience

    def get_technical_skills(self,obj):
        return obj.profile.technical_skills

    def get_current_job(self,obj):
        return obj.profile.current_job

    def get_profile_photo(self,obj):
        return obj.profile.profile_photo



class SaveMentorSerializer(serializers.Serializer):
    mentor = serializers.PrimaryKeyRelatedField(queryset=Users.objects.all())

    def validate_mentor(self,value):
        user = self.context["user"]
        if user == value:
            raise serializers.ValidationError("Cannot save self.")
        if value.user_type != "mentor":
            raise serializers.ValidationError("This user is not a mentor.")
        if models.SavedMentors.objects.filter(saver=user,saved=value).exists():
            raise serializers.ValidationError("This User has already been saved")
        return value

    def create(self,validated_data):
        validated_data["saver"] = self.context["user"]
        validated_data["saved"] = validated_data.pop("mentor")

        output_instance = models.SavedMentors.objects.create(**validated_data)
        return output_instance


class UnsaveMentorSerializer(serializers.Serializer):
    mentor = serializers.PrimaryKeyRelatedField(queryset=Users.objects.all())

    def validate(self,data):
        user = self.context["user"]
        mentor = data.get("mentor")
        saved_instance = models.SavedMentors.objects.filter(saver=user,saved=mentor)

        if not saved_instance.exists():
            raise serializers.ValidationError("This Mentor have not been previously saved.")
        return saved_instance




class RetrieveSavedMentorSerializer(serializers.ModelSerializer):
    saved = serializers.SerializerMethodField()

    class Meta:
        model = models.SavedMentors
        fields = ["saved"]

    def get_saved(self,obj):
        output = RetrieveMentorSearchAndRetrieveSerializer(obj.saved,many=False).data
        return output
