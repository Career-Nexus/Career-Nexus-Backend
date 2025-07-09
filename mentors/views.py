from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import AllowAny,IsAuthenticated

from users.models import PersonalProfile

from . import serializers


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



class TestView(APIView):
    permission_classes = [
        AllowAny,
    ]
    def get(self,request):
        return Response({"Installed"},status=status.HTTP_200_OK)
