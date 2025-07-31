from shutil import register_unpack_format
from django.utils.timezone import make_aware
from rest_framework import serializers
from rest_framework.response import Serializer


from users.options import get_choices
from users.models import PersonalProfile,Users
from posts.serializers import PersonalProfileSerializer

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
    experience_level = serializers.SerializerMethodField()

    class Meta:
        model = PersonalProfile
        fields = ["first_name","last_name","middle_name","profile_photo","current_job","experience_level"]

    def get_experience_level(self,obj):
        if obj.years_of_experience:
            if obj.years_of_experience <= 2:
                return "Junior"
            elif obj.years_of_experience > 2 and obj.years_of_experience <=5:
                return "Mid"
            else:
                return "Senior"
        else:
            return "Junior"

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
            raise serializers.ValidationError("A Date and time must be set wen booking sessions.")

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
            #TODO Notify the initiator of the session that the session was rejected.
            session.delete()
        else:
            #TODO Notify the initiator of the session that the session was accepted.
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
    status = serializers.CharField()

    def get_join(self,obj):
        if obj.status != "PENDING":
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

