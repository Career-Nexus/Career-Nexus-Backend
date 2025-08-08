#from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from . import serializers, models



class ProjectCatalogueView(APIView):
    permission_classes = [
        IsAuthenticated,
    ]

    def post(self,request):
        user = request.user
        serializer = serializers.CreateProjectCatalogueSerializer(data=request.data,context={"user":user})
        if serializer.is_valid(raise_exception=True):
            output_instance = serializer.save()
            output = serializers.ProjectCatalogueSerializer(output_instance,many=False).data
            return Response(output,status=status.HTTP_201_CREATED)


