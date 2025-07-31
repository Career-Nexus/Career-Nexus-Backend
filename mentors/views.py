from django.db.models import Q

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import AllowAny,IsAuthenticated

from users.models import PersonalProfile, experience

from . import serializers,models
from users.models import Users

import uuid


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
        industry = request.user.industry
        mentors = PersonalProfile.objects.filter(user__user_type="mentor",user__industry=industry)
        #TODO Paginate results
        output = serializers.MentorRecommendationSerializer(mentors,many=True).data
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
                
            output = serializers.RetrieveMentorsSerializer(mentors,many=True).data
            return Response(output,status=status.HTTP_200_OK)


class CreateMentorshipSessionView(APIView):
    permission_classes = [
        IsAuthenticated,
    ]

    def post(self,request):
        serializer = serializers.CreateMentorshipSessionSerializer(data=request.data,context={"user":request.user})
        if serializer.is_valid(raise_exception=True):
            output_instance = serializer.save()
            #TODO Create notification for the mentor about the session request
            output = serializers.SessionRetrieveSerializer(output_instance,many=False,context={"user":request.user}).data
            return Response(output,status=status.HTTP_201_CREATED)


class AcceptRejectMentorshipSessionsView(APIView):
    permission_classes = [
        IsAuthenticated,
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
            valid_parameters = ["requested","accepted","scheduled"]
            if param.lower() not in valid_parameters:
                return Response({"error":"Invalid query parameter. Paramter can only be requested,accepted,pending"},status=status.HTTP_400_BAD_REQUEST)
            else:
                if param.lower() == "requested":
                    sessions =models.Sessions.objects.filter(mentee=user,status="PENDING")
                elif param.lower() == "scheduled":
                    #scheduled sessions can only be called by mentors.
                    if user.user_type != "mentor":
                        return Response({"error":"Scheduled sessions are only available to mentors"},status=status.HTTP_400_BAD_REQUEST)
                    sessions = models.Sessions.objects.filter(mentor=user)
                else:
                    sessions = models.Sessions.objects.filter(mentee=user,status="ACCEPTED")
                output = serializers.SessionRetrieveSerializer(sessions,many=True,context={"user":user}).data
                
                return Response(output,status=status.HTTP_200_OK)





class TestView(APIView):
    permission_classes = [
        AllowAny,
    ]
    def get(self,request):
        return Response({"Installed"},status=status.HTTP_200_OK)
