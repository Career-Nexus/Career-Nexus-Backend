from django.db.models import Q

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.pagination import PageNumberPagination

from notifications.utils import send_notification

from users.models import PersonalProfile
from info.models import ExchangeRate

from . import serializers,models
from users.models import Users
from utilities.permissions import IsMentor

import uuid



class MentorRecommendationPagination(PageNumberPagination):
    page_size = 4


def extract_years_from_experience_level(text):
    if text.lower() == "entry":
        return [0,2]
    elif text.lower() == "mid":
        return [3,5]
    elif text.lower() == "senior":
        return [6,10]
    elif text.lower() == "executive":
        return [11,50]
    return [0,100]

def split_datetime_into_components(datetime):
    return [datetime.date(),datetime.time()]




class MentorRecommendationView(APIView):
    permission_classes = [
        IsAuthenticated,
    ]
    def get(self,request):
        user = request.user
        industry = request.user.industry
        mentors = PersonalProfile.objects.filter(user__user_type="mentor",user__industry=industry).exclude(user=user)
        rate_instance = ExchangeRate.objects.filter(country__code=user.profile.country_code).first()
        if not rate_instance:
            rate_instance = None
        saved_mentors_ids = models.SavedMentors.objects.filter(saver=user).values_list("saved_id",flat=True)
        
        paginator = MentorRecommendationPagination()
        paginated_items = paginator.paginate_queryset(mentors,request)
        serialized_items = serializers.MentorRecommendationSerializer(paginated_items,many=True,context={"user":request.user,"rate_instance":rate_instance,"saved_mentors":saved_mentors_ids}).data


        output = paginator.get_paginated_response(serialized_items).data
        return Response(output,status=status.HTTP_200_OK)


class MentorSearchAndFilterView(APIView):
    permission_classes = [
        IsAuthenticated,
    ]

    def get(self,request):
        serializer = serializers.MentorSearchAndFilterSerializer(data=request.query_params)
        if serializer.is_valid(raise_exception=True):
            search_data = serializer.validated_data

            #Multi-level filtering
            mentors = Users.objects.filter(user_type="mentor")
            if "text" in search_data:
                filter = search_data["text"]
                mentors = mentors.filter(
                    Q(profile__first_name__icontains=filter) |
                    Q(profile__last_name__icontains=filter) |
                    Q(profile__middle_name__icontains=filter) |
                    Q(profile__bio__icontains=filter) |
                    Q(profile__areas_of_expertise__contains=[filter]) |
                    Q(profile__technical_skills__contains=[filter])
                )

            if "experience_level" in search_data:
                experience_range =  extract_years_from_experience_level(search_data["experience_level"])
                print(experience_range)
                mentors = mentors.filter(profile__years_of_experience__range=(experience_range[0],experience_range[1]))

            if "skills" in search_data:
                filter = search_data["skills"]
                mentors = mentors.filter(profile__technical_skills__contains=[filter])

            if "availability" in search_data:
                filter = search_data["availability"]
                mentors = mentors.filter(profile__availability=filter)
                
            output = serializers.RetrieveMentorSearchAndRetrieveSerializer(mentors,many=True).data
            return Response(output,status=status.HTTP_200_OK)


class CreateMentorshipSessionView(APIView):
    permission_classes = [
        IsAuthenticated,
    ]

    def post(self,request):
        user = request.user
        serializer = serializers.CreateMentorshipSessionSerializer(data=request.data,context={"user":request.user})
        if serializer.is_valid(raise_exception=True):
            output_instance = serializer.save()
            #TODO Create notification for the mentor about the session request
            rate_instance = ExchangeRate.objects.filter(country__code=user.profile.country_code).first()
            if not rate_instance:
                rate_instance = None
            output = serializers.SessionRetrieveSerializer(output_instance,many=False,context={"user":request.user,"rate_instance":rate_instance}).data
            return Response(output,status=status.HTTP_201_CREATED)


class AcceptRejectMentorshipSessionsView(APIView):
    permission_classes = [
        IsAuthenticated,
        IsMentor,
    ]
    def post(self,request):
        serializer = serializers.AcceptRejectMentorshipSessionSerializer(data=request.data,context={"user":request.user})
        if serializer.is_valid(raise_exception=True):
            output = serializer.save()
            return Response(output,status=status.HTTP_200_OK)



class RetrieveMentorshipSessionsView(APIView):
    permission_classes = [
        IsAuthenticated,
    ]
    def get(self,request):
        user = request.user
        param = request.query_params.get("status")
        if not param:
            return Response({"error":"No query parameter is provided for this request."},status=status.HTTP_400_BAD_REQUEST)
        else:
            valid_parameters = ["requested","accepted","scheduled","completed"]
            if param.lower() not in valid_parameters:
                return Response({"error":"Invalid query parameter. Paramter can only be requested,accepted,pending"},status=status.HTTP_400_BAD_REQUEST)
            else:
                if param.lower() == "requested":
                    if user.user_type != "mentor":
                        sessions =models.Sessions.objects.filter(mentee=user,status="PENDING").select_related("mentee__profile","mentor__profile")
                    else:
                        sessions = models.Sessions.objects.filter(mentor=user,status="PENDING").select_related("mentee__profile","mentor__profile")
                elif param.lower() == "scheduled":
                    #scheduled sessions can only be called by mentors.
                    if user.user_type != "mentor":
                        return Response({"error":"Scheduled sessions are only available to mentors"},status=status.HTTP_400_BAD_REQUEST)
                    sessions = models.Sessions.objects.filter(mentor=user,status="ACCEPTED").select_related("mentee__profile","mentor__profile")
                elif param.lower() == "completed":
                    if user.user_type != "mentor":
                        sessions = models.Sessions.objects.filter(mentee=user,status="COMPLETED").select_related("mentee__profile")
                    else:
                        sessions = models.Sessions.objects.filter(mentor=user,status="COMPLETED").select_related("mentee__profile","mentor__profile")
                else:
                    sessions = models.Sessions.objects.filter(mentee=user,status="ACCEPTED").select_related("mentee__profile","mentor__profile")
                rate_instance = ExchangeRate.objects.filter(country__code=user.profile.country_code).first()
                if not rate_instance:
                    rate_instance = None
                output = serializers.SessionRetrieveSerializer(sessions,many=True,context={"user":user,"rate_instance":rate_instance}).data
                
                return Response(output,status=status.HTTP_200_OK)


class SaveMentorView(APIView):
    permission_classes=[
        IsAuthenticated,
    ]
    def post(self,request):
        serializer = serializers.SaveMentorSerializer(data=request.data,context={'user':request.user})
        if serializer.is_valid(raise_exception=True):
            output_instance = serializer.save()
            output = serializers.RetrieveSavedMentorSerializer(output_instance,many=False).data
            return Response(output,status=status.HTTP_201_CREATED)

    def get(self,request):
        user = request.user
        saved_mentors = user.mentor_saver.all()
        output = serializers.RetrieveSavedMentorSerializer(saved_mentors,many=True).data
        return Response(output,status=status.HTTP_200_OK)

    def delete(self,request):
        user = request.user
        param = request.query_params.get("mentor")
        if not param:
            return Response({"error":"A mentor query parameter is required to Unsave a mentor."},status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer = serializers.UnsaveMentorSerializer(data=request.query_params,context={"user":user})
            if serializer.is_valid(raise_exception=True):
                saved_instance = serializer.validated_data
                saved_instance.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)


class AnnotateMentorshipSessionView(APIView):
    permission_classes = [
        IsAuthenticated,
    ]

    def post(self,request):
        user = request.user
        if user.user_type != "learner":
            return Response({"error":"Mentorship session annotation can only be carried out by learners"},status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer = serializers.AnnotateMentorshipSessionSerializer(data=request.data,context={"user":user})
            if serializer.is_valid(raise_exception=True):
                output_instance = serializer.save()
                rate_instance = ExchangeRate.objects.filter(country__code=user.profile.country_code).first()
                if not rate_instance:
                    rate_instance = None
                output = serializers.SessionRetrieveSerializer(output_instance,many=False,context={"user":user,"rate_instance":rate_instance}).data
                return Response(output,status=status.HTTP_200_OK)


class CancelSessionView(APIView):
    permission_classes = [
        IsAuthenticated,
    ]
    def post(self,request):
        user = request.user
        serializer = serializers.CancelSessionSerializer(data=request.data,context={"user":user})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"status":"Success","message":"Cancelled Mentorship session"},status=status.HTTP_200_OK)


class JoinSessionView(APIView):
    permission_classes = [
        IsAuthenticated,
    ]

    def get(self,request):
        user = request.user
        param = request.query_params.get("session")
        if not param:
            return Response({"error":"A session query parameter is required for this request"},status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer = serializers.JoinSessionSerializer(data=request.query_params,context={"user":user})
            if serializer.is_valid(raise_exception=True):
                session = serializer.validated_data.get("session")
                output = {
                    'session_id':session.id,
                    'room_name':session.room_name
                }
                return Response(output,status=status.HTTP_200_OK)


class MentorVaultView(APIView):
    permission_classes = [
        IsAuthenticated,
        IsMentor,
    ]

    def get(self,request):
        user = request.user
        vault, _ = models.MentorVault.objects.get_or_create(mentor=user)
        output = serializers.MentorVaultSerializer(vault,many=False).data
        return Response(output,status=status.HTTP_200_OK)

class RetrieveMentorVaultTransactionsView(APIView):
    permission_classes = [
        IsAuthenticated,
        IsMentor,
    ]

    def get(self,request):
        user = request.user
        country_code = user.profile.country_code
        currency=None
        rate = ExchangeRate.objects.filter(country__code=country_code).first()
        if rate:
            currency = rate.currency_initials
            rate = rate.exchange_rate


        all_transactions = user.vault_transactions.all().order_by("-timestamp")
        output = serializers.VaultTransactionsSerializer(all_transactions,many=True,context={"rate":rate,"currency":currency}).data
        return Response(output,status=status.HTTP_200_OK)



class TestView(APIView):
    permission_classes = [
        AllowAny,
    ]
    def get(self,request):
        return Response({"Installed"},status=status.HTTP_200_OK)
