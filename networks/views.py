#from django.shortcuts import render
#from django.db.models.base import connection
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from rest_framework.pagination import PageNumberPagination


from django.http import Http404
from django.db.models import Q

from . import serializers
from . import models
from users.models import Users,PersonalProfile



connection_status = ["PENDING","CONFIRMED"]

class RecommendationPaginator(PageNumberPagination):
    page_size = 5



class ConnectionView(APIView):
    permission_classes = [
        IsAuthenticated,
    ]
    serializer_class = serializers.ConnectionSerializer

    def post(self,request):
        serializer = self.serializer_class(data=request.data,context={"user":request.user})
        if serializer.is_valid(raise_exception=True):
            output = serializer.save()
            return Response(output,status=status.HTTP_201_CREATED)

    def get(self,request):
        user = request.user
        connections = models.Connection.objects.select_related("user","connection").filter(Q(user=user,status="CONFIRMED") | Q(connection=user,status="CONFIRMED"))
        serialized_data = serializers.RetrieveConnectionSerializer(connections,many=True,context={"user":request.user}).data
        return Response(serialized_data,status=status.HTTP_200_OK)
       



class ConnectionStatusView(APIView):
    permission_classes = [
        IsAuthenticated,
    ]
    serializer_class = serializers.ConnectionStatusSerializer

    def post(self,request):
        serializer = self.serializer_class(data=request.data,context={"user":request.user})
        if serializer.is_valid(raise_exception=True):
            output = serializer.save()
            return Response(output,status=status.HTTP_201_CREATED)

class ConnectionPendingView(APIView):
    permission_classes = [
        IsAuthenticated,
    ]
    serializer_class = serializers.RetrieveConnectionSerializer

    def get(self,request):
        user = request.user
        pending_confirmation = user.connect.select_related("user","connection").filter(status="PENDING")
        serialized_data = self.serializer_class(pending_confirmation,many=True,context={"user":user}).data
        return Response(serialized_data,status=status.HTTP_200_OK)


class ConnectionRecommendationView(APIView):
    permission_classes = [
        IsAuthenticated,
    ]
    serializer_class = serializers.RetrieveRecommendationDetailSerializer
#TODO Setup db_indexing for locations and industry fields in users models for optimization.
    def get(self,request):
        user = request.user
        user_industry = user.industry

        criteria = request.query_params.get("criteria",None)

        if not criteria:
            return Response({"error":"Recommendation criteria not provided"},status=status.HTTP_400_BAD_REQUEST)

        else:  
            if criteria.lower() == "industry":
                industry_recommendations = Users.objects.filter(industry=user_industry).exclude(id=user.id)
                recommendations = industry_recommendations.exclude(Q(connection_user__connection=user) | Q(connect__user=user))


            elif criteria.lower() == "location":
                location_recommendations = Users.objects.select_related("profile").filter(profile__location__icontains=user.profile.location).exclude(id=user.id)
                recommendations = location_recommendations.exclude(Q(connection_user__connection = user) | Q(connect__user = user))
            else:
                return Response({"criteria error":"Unrecognized recommendation criteria."},status=status.HTTP_400_BAD_REQUEST)

            serialized_data = self.serializer_class(recommendations,many=True).data
            return Response(serialized_data,status=status.HTTP_200_OK)
