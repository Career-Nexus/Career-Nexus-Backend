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

    def get(self,request):
        param = request.query_params.get("portfolio_id")
        if not param:
            all_portfolios = models.ProjectCatalogue.objects.filter(owner=request.user)
            output = serializers.ProjectCatalogueSerializer(all_portfolios,many=True).data
            return Response(output,status=status.HTTP_200_OK)
        else:
            portfolio = models.ProjectCatalogue.objects.filter(id=param).first()
            if not portfolio:
                return Response({"error":"Invalid Portfolio ID"},status=status.HTTP_400_BAD_REQUEST)
            else:
                output = serializers.ProjectCatalogueSerializer(portfolio,many=False).data
                return Response(output,status=status.HTTP_200_OK)

    def delete(self,request):
        user = request.user
        param = request.query_params.get("portfolio_id")
        if not param:
            return Response({"error":"No portfolio_id is provided"},status=status.HTTP_400_BAD_REQUEST)
        else:
            project = models.ProjectCatalogue.objects.filter(owner=user,id=param).first()
            if not project:
                return Response({"error":"Invalid portfolio ID"},status=status.HTTP_400_BAD_REQUEST)
            else:
                project.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)


