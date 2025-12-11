from django.forms import fields
from rest_framework import serializers, status

from django.db import transaction
from decimal import Decimal

from users.options import get_choices
from users.models import PersonalProfile,Users
from posts.serializers import PersonalProfileSerializer
from info.models import ExchangeRate
from notifications.utils import send_notification

from . import models

from datetime import datetime
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
    rating = serializers.SerializerMethodField()

    class Meta:
        model = PersonalProfile
        fields = ["id","first_name","last_name","middle_name","profile_photo","current_job","years_of_experience","technical_skills","session_rate","rating","is_saved"]

    def get_rating(self,obj):
        mentor = obj.user
        try:
            mentor_ratings = mentor.rating
            average_rating = sum(mentor_ratings.ratings)/len(mentor_ratings.ratings)
        except:
            average_rating = 0
        return average_rating

    def get_session_rate(self,obj):
        session_rate = obj.session_rate
        user = self.context["user"]
        rate_instance = self.context["rate_instance"]
        if not rate_instance:
            return f"{session_rate}USD"
        else:
            amount = int(rate_instance.exchange_rate*session_rate)
            currency = rate_instance.currency_initials
            return f"{amount}{currency}"

    def get_id(self,obj):
        return obj.user.id

    def get_is_saved(self,obj):
        saved_mentors = self.context["saved_mentors"]
        if obj.id in saved_mentors:
            return True
        return False



class MentorSearchAndFilterSerializer(serializers.Serializer):
    text = serializers.CharField(max_length=1000,required=False)
    experience_level = serializers.ChoiceField(choices=experience_level_choices,required=False)
    skills = serializers.CharField(max_length=500,required=False)
    availability = serializers.ChoiceField(choices=availability_options,required=False)



class CreateMentorshipSessionSerializer(serializers.Serializer):
    mentor = serializers.PrimaryKeyRelatedField(queryset=Users.objects.all())
    session_type = serializers.ChoiceField(choices=session_categories)
    invitees = serializers.JSONField(required=False)
    date = serializers.DateField()
    time = serializers.TimeField()
    discourse = serializers.CharField()

    def validate_invitees(self,value):
        user = self.context["user"]
        if not isinstance(value,list):
            raise serializers.ValidationError("invitees must be a list of valid user ids.")
        #Exclude oneself from the list to avoid inviting self for a session
        valid_users = Users.objects.filter(id__in=value).exclude(id=user.id)
        valid_users_ids = valid_users.values_list("id",flat=True)

        outliers = list(set(value) - set(valid_users_ids))

        if len(outliers) != 0:
            raise serializers.ValidationError(f"No user(s) with ids {outliers}")
        #Ensuring not more than 10 users can be invited for a session
        return valid_users[0:10]


    def validate_mentor(self,value):
        if Users.objects.filter(id=value.id).first().user_type != "mentor":
            raise serializers.ValidationError("This User is not a mentor.")
        return value

    def validate(self,data):
        user = self.context["user"]
        if user == data["mentor"]:
            raise serializers.ValidationError("Cannot schedule a mentorship session with yourself.")
        session_type = data.get("session_type")

        #Ensuring invitees are provided are provided in group sessions.
        if (session_type == "group") and not (data.get("invitees")):
            raise serializers.ValidationError("Invitees must be provided in group sessions.")

        #Remove all invitees if session_type == "Individual"
        if (session_type == "individual"):
            data["invitees"] = []

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
        invitees = validated_data.pop("invitees")
        validated_data["room_name"] = f"Room_{mentee.id}_{mentor.id}_{uuid.uuid4()}"

        if mentor.profile.session_rate == 0:
            validated_data["is_paid"] = True

        session_instance = models.Sessions.objects.create(**validated_data)

        if invitees:
            container = []
            for invitee in invitees:
                container.append(models.InvitedSessions(session=session_instance,invitee=invitee))
            models.InvitedSessions.objects.bulk_create(container,batch_size=100)

        send_notification(session_instance.mentor, f"{session_instance.mentee.profile.first_name} {session_instance.mentee.profile.last_name} requested a mentorship session from you.",page="Mentorship Sessions")

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
            send_notification(session.mentee,f"Mentor {session.mentor.profile.first_name} {session.mentor.profile.last_name} rejected your mentorship request.",page="Mentorship Sessions")
            session.delete()
        else:
            send_notification(session.mentee,f"Mentor {session.mentor.profile.first_name} {session.mentor.profile.last_name} accepted your mentorship request.",page="Mentorship Sessions")
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
    invitees = serializers.SerializerMethodField()
    join = serializers.SerializerMethodField()
    session_type = serializers.CharField()
    session_at = serializers.SerializerMethodField()
    discourse = serializers.CharField()
    amount = serializers.SerializerMethodField()
    rating = serializers.IntegerField()
    status = serializers.CharField()
    is_paid = serializers.BooleanField()

    def get_invitees(self,obj):
        invitees = obj.invitedsessions_set.all().select_related("invitee")
        output = RetrieveInviteesSerializer(invitees,many=True).data
        return output


    def get_amount(self,obj):
        mentor_rate = obj.mentor.profile.session_rate
        user = self.context["user"]
        rate_instance = self.context["rate_instance"]
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


class RetrieveInviteesSerializer(serializers.ModelSerializer):
    invitee = serializers.SerializerMethodField()

    class Meta:
        model = models.InvitedSessions
        fields = ["invitee"]

    def get_invitee(self,obj):
        output = PersonalProfileSerializer(obj.invitee.profile,many=False).data
        return output


class RetrieveInvitedSessionsSerializer(serializers.ModelSerializer):
    session = serializers.SerializerMethodField()

    class Meta:
        model = models.InvitedSessions
        fields = ["id","session"]

    def get_session(self,obj):
        output =  SessionRetrieveSerializer(obj.session,many=False,context={"user":self.context["user"],"rate_instance":None}).data
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

class AnnotateMentorshipSessionSerializer(serializers.Serializer):
    session = serializers.PrimaryKeyRelatedField(queryset=models.Sessions.objects.all())
    mark_completed = serializers.BooleanField()
    rating = serializers.IntegerField()

    def validate_session(self,session):
        user = self.context["user"]
        if session.mentee != user:
            raise serializers.ValidationError("This session was not initiated by you.")
        #Ensure a session has been paid for without which attendance is impossible.
        if not session.is_paid:
            raise serializers.ValidationError("Cannot annotate a session that has not been paid for.")
        #Check if the session has been previously marked as completed.
        if session.status == "COMPLETED":
            raise serializers.ValidationError("This session has been completed.")
        #Check if the session is still in the future
        timezone = pytz.timezone("UTC")
        session_at = session.session_at
        now = timezone.localize(datetime.now())
        if session.status != "ACCEPTED" or (session_at > now):
            raise serializers.ValidationError("This session has not been Completed.")
        return session

    def validate_mark_completed(self,value):
        if value == False:
            raise serializers.ValidationError("The session mark_completed must be True to annotate a session")
        return value

    def validate_rating(self,value):
        rating_range = list(range(1,6))
        if value not in rating_range:
            raise serializers.ValidationError("A rating can only range from 1 to 5")
        return value

    def create(self,validated_data):
        session = validated_data.get("session")
        mentor = session.mentor

        with transaction.atomic():
            #Mark session as completed
            session.status = "COMPLETED"
            session.save()

            #Cleanup invited sessions
            session.invitedsessions_set.all().delete()
            
            #Update the amount earned by mentor
            transaction_instance = session.sessiontransactions_set.filter(status="successful").first()
            #The platform keeps 20% of mentor earnings && Decimal converts from float
            if transaction_instance:
                paid_amount = Decimal((transaction_instance.central_amount * 0.8))
                mentor.vault.amount += paid_amount
                mentor.vault.save()

                #Update vault transaction 
                models.VaultTransactions.objects.create(mentor=mentor,action="EARN",amount=paid_amount,extra_data={"session_id":session.id,"session_type":session.session_type})


        rating = validated_data.get("rating")

        session.rating = rating
        session.save()

        mentor_rating, created = models.MentorRating.objects.get_or_create(mentor=mentor)
        mentor_rating.ratings.append(rating)
        mentor_rating.save()

        return session



class CancelSessionSerializer(serializers.Serializer):
    session = serializers.PrimaryKeyRelatedField(queryset=models.Sessions.objects.all())

    def validate_session(self,session):
        user = self.context["user"]
        if user != session.mentee:
            raise serializers.ValidationError("Only this session's mentee can cancel this session.")
        if session.is_paid:
            raise serializers.ValidationError("Cannot cancel an already paid session.")
        return session

    def create(self,validated_data):
        session =validated_data.get("session")
        session.delete()
        return True


class JoinSessionSerializer(serializers.Serializer):
    session = serializers.PrimaryKeyRelatedField(queryset=models.Sessions.objects.all())

    def validate_session(self,session):
        user = self.context["user"]
        if (user != session.mentor) and (user != session.mentee) and not (user.invited_sessions.filter(session=session).exists()):
            raise serializers.ValidationError("You are not a participant in this session.")
        if not session.is_paid:
            raise serializers.ValidationError("This session has not yet been paid for.")
        if session.status == "COMPLETED":
            raise serializers.ValidationError("This session has already been completed.")
        now = datetime.now()
        timezone = pytz.timezone("UTC")
        now = timezone.localize(now)
        if now < session.session_at:
            raise serializers.ValidationError("Not yet time for this session.")

        return session

class MentorVaultSerializer(serializers.ModelSerializer):
    amount = serializers.SerializerMethodField()
    recent_transaction_history = serializers.SerializerMethodField()

    class Meta:
        model = models.MentorVault
        fields = ["amount","recent_transaction_history"]

    def get_amount(self,obj):
        central_amount = obj.amount
        country_code = obj.mentor.profile.country_code
        rate = ExchangeRate.objects.filter(country__code=country_code).first()
        if not rate:
            return {
                "amount":central_amount,
                "currency":"USD"
            }
        else:
            return {
                "amount":central_amount*rate.exchange_rate,
                "currency":rate.currency_initials
            }

    def get_recent_transaction_history(self,obj):
        mentor = obj.mentor
        country_code = mentor.profile.country_code
        rate = ExchangeRate.objects.filter(country__code=country_code).first()
        recent_transactions = models.VaultTransactions.objects.filter(mentor=mentor).order_by("-timestamp")[0:11]
        if not rate:
            output = VaultTransactionsSerializer(recent_transactions,many=True,context={"rate":None,"currency":None}).data
        else:
            output = VaultTransactionsSerializer(recent_transactions,many=True,context={"rate":rate.exchange_rate,"currency":rate.currency_initials}).data
        return output


class VaultTransactionsSerializer(serializers.ModelSerializer):
    amount = serializers.SerializerMethodField()

    class Meta:
        model = models.VaultTransactions
        fields = ["id","action","amount","extra_data","timestamp"]

    def get_amount(self,obj):
        rate = self.context["rate"]
        currency = self.context["currency"]
        if not rate:
            return {
                "value":obj.amount,
                "currency":"USD"
            }
        else:
            return {
                "value":rate*obj.amount,
                "currency":currency
            }
