#from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from . import serializers, models



class ProjectView(APIView):
    permission_classes = [
        IsAuthenticated,
    ]
    serializer_class = serializers.ProjectSerializer
    
    def post(self,request):
        serializer = self.serializer_class(data=request.data,context={"user":request.user})
        if serializer.is_valid(raise_exception=True):
            output = serializer.save()
            return Response(output,status=status.HTTP_201_CREATED)

    def get(self,request):
        user = request.user
        portfolios = models.Project.objects.filter(user=user)
        portfolios = serializers.RetrieveProjectSerializer(portfolios,many=True).data
        return Response(portfolios,status=status.HTTP_200_OK)
