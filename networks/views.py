from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from rest_framework.pagination import PageNumberPagination


from django.http import Http404
from django.db.models import Q
from django.core.cache import cache

from . import serializers
from . import models
from users.models import Users




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
            return Response(output,status=status.HTTP_200_OK)

class ConnectionPendingView(APIView):
    permission_classes = [
        IsAuthenticated,
    ]
    serializer_class = serializers.RetrieveConnectionSerializer

    def get(self,request):
        user = request.user
        pending_confirmation = user.connect.select_related("user","connection").filter(status="PENDING")
        pending_count = pending_confirmation.count()
        serialized_data = self.serializer_class(pending_confirmation,many=True,context={"user":user}).data
        output = {
            "pending_requests":serialized_data,
            "count":pending_count
        }
        return Response(output,status=status.HTTP_200_OK)


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

        base_url = request.build_absolute_uri()
        base_url = base_url.split("?")[0]

        if not criteria:
            return Response({"error":"Recommendation criteria not provided"},status=status.HTTP_400_BAD_REQUEST)

        else:  
            if criteria.lower() == "industry":
                industry_recommendations = Users.objects.filter(industry=user_industry).exclude(id=user.id)
                recommendations = industry_recommendations.exclude(Q(connection_user__connection=user) | Q(connect__user=user)).order_by("id")



            elif criteria.lower() == "location":
                location_recommendations = Users.objects.select_related("profile").filter(profile__location__icontains=user.profile.location).exclude(id=user.id)
                recommendations = location_recommendations.exclude(Q(connection_user__connection = user) | Q(connect__user = user)).order_by("id")

            else:
                return Response({"criteria error":"Unrecognized recommendation criteria."},status=status.HTTP_400_BAD_REQUEST)

            paginator = RecommendationPaginator()
            paginated_items = paginator.paginate_queryset(recommendations,request)

            serializer = self.serializer_class(paginated_items,many=True)

            item_count = recommendations.count()
            page_full = item_count//paginator.page_size
            if item_count % paginator.page_size == 0:
                pages = page_full
            else:
                pages = page_full + 1 

            response = paginator.get_paginated_response(serializer.data).data
            response["last_page"] = f"{base_url}?page={pages}"
            #serialized_data = self.serializer_class(recommendations,many=True).data
            return Response(response,status=status.HTTP_200_OK)

class ConnectionsCountView(APIView):
    permission_classes=[
        IsAuthenticated,
    ]
    def get(self,request):
        user = request.user
        connection_count = models.Connection.objects.filter(
            Q(user=user,status="CONFIRMED") |
            Q(connection=user,status="CONFIRMED")
        ).count()
        output = {
            "connections_count":connection_count
        }
        return Response(output,status=status.HTTP_200_OK)

class ConnectionRequestSentView(APIView):
    permission_classes=[
        IsAuthenticated,
    ]
    def get(self,request):
        user = request.user
        requests_sent = models.Connection.objects.filter(user=user,status="PENDING")
        requests_count = requests_sent.count()
        request_output = serializers.RetrieveConnectionSerializer(requests_sent,many=True,context={"user":user}).data
        output = {
            "connection_requests":request_output,
            "count":requests_count
        }
        return Response(output,status=status.HTTP_200_OK)
