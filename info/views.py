#from django.shortcuts import render
from django.conf import settings

from django.http import Http404
from rest_framework.response import Response, Serializer
from rest_framework.permissions import IsAdminUser, IsAuthenticated,AllowAny
from rest_framework import status
from rest_framework.views import APIView

from . import serializers, models

import json


class InformationView(APIView):

    def get_permissions(self):
        if self.request.method == "POST":
            #TODO Change permission to IsAdminUser
            return [AllowAny()]
        elif self.request.method == "GET":
            return [AllowAny()]
        elif self.request.method == "PUT":
            #TODO Change permission to IsAdminUser
            return [AllowAny()]
        return super().get_permissions()

    serializer_class = serializers.InformationSerializer
    
    def post(self,request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            output = serializer.save()
            return Response(output,status=status.HTTP_201_CREATED)

    def get(self,request):
        params = request.query_params.get("title")
        available_titles = list(models.Information.objects.values_list("title",flat=True))
        if not params:
            output = {
                "Status":"Failed",
                "Message":"No query parameter provided.",
                "Available_titles":available_titles
            }
            return Response(output,status=status.HTTP_400_BAD_REQUEST)
        else:
            title = models.Information.objects.filter(title=params)
            if len(title) == 0:
                output = {
                    "Status":"Failed",
                    "Message":"Invalid information Title",
                    "Available_titles":available_titles
                }
                return Response(output,status=status.HTTP_404_NOT_FOUND)
            else:
                item = title.first()
                info = {
                    "title":item.title,
                    "content":item.content,
                    "items":item.items,
                    "updated":item.updated_at
                }
                output ={
                    "status":"Success",
                    "content":info,
                    "Available_titles":available_titles
                }
                return Response(output,status=status.HTTP_200_OK)

        
    def put(self,request):
        params = request.query_params.get("title")
        if not params:
            return Response({"error":"No query parameter provided!"},status=status.HTTP_400_BAD_REQUEST)
        else:
            instances = models.Information.objects.filter(title=params)
            if len(instances) == 0:
                return Response({"error":"Inexistent content"},status=status.HTTP_400_BAD_REQUEST)
            else:
                instance = instances.first()
                serializer = serializers.AlterInformationSerializer(data=request.data,instance=instance)
                if serializer.is_valid(raise_exception=True):
                    instance = serializer.save()
                    output = {
                        "status":"Updated",
                        "title":instance.title,
                        "content":instance.content,
                        "items":instance.items,
                        "updated":instance.updated_at
                    }
                    return Response(output,status=status.HTTP_200_OK)

    def delete(self,request):
        params = request.query_params.get("title")
        if not params:
            return Response({"error":"No query parameter provided"},status=status.HTTP_400_BAD_REQUEST)
        else:
            try:
                models.Information.objects.get(title=params).delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            except:
                return Response({"error":"Inexistent content"},status=status.HTTP_400_BAD_REQUEST)

class CountryPermitView(APIView):
    permission_classes = [
        AllowAny,
    ]
    serializer_class =serializers.CountryPermitSerializer

    def get(self,request):
        allowed_params = ["enable","disable"]
        params = request.query_params.get("status")
        if not params:
            permitted_countries = models.Countrycodes.objects.all()
            serialized_data = self.serializer_class(permitted_countries,many=True).data
            return Response(serialized_data,status=status.HTTP_200_OK)
        else:
            if params.strip().lower() not in allowed_params:
                return Response({"error":"Invalid Query Parameter"},status=status.HTTP_400_BAD_REQUEST)
            else:
                if params == "enable":
                    params = True
                else:
                    params=False
                countries = models.Countrycodes.objects.filter(permitted=params)
                serialized_data = self.serializer_class(countries,many=True).data
                return Response(serialized_data,status=status.HTTP_200_OK)


    def put(self,request):
        serializer = serializers.AlterCountryPermitSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            instance = serializer.save()
            output = {
                "country":instance.country,
                "permitted":instance.permitted
            }
            return Response(output,status=status.HTTP_200_OK)


class ChoiceFieldView(APIView):
    permission_classes = [
        IsAuthenticated,#TODO Add IsAdminUser to permission classes
    ]
    serializer_class = serializers.ChoiceFieldSerializer
    
    CHOICE_DIR = settings.CHOICE_FIELD_DB

    with open(CHOICE_DIR,"r") as file:
        choices = json.load(file)

    def verify_fieldname(self,value):
        choices_keys = list(self.choices.keys())
        if value not in choices_keys:
            raise Http404("Invalid field name")
        else:
            return value


    def get(self,request):
        param = request.query_params.get("field_name")
        choices_keys = list(self.choices.keys())

        if not param:
            return Response({"field_names":choices_keys},status=status.HTTP_200_OK)
        else:
            if param not in choices_keys:
                return Response({'error':'Invalid field name.','Avalable_names':choices_keys},status=status.HTTP_400_BAD_REQUEST)
            else:
                valid_data = self.choices[param]
                return Response({"field_name":param,"Valid options":valid_data},status=status.HTTP_200_OK)

    def post(self,request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            validated_data = serializer.validated_data
            choices_keys = list(self.choices.keys())
            field_name = validated_data.get("field_name")
            if field_name not in choices_keys:
                return Response({"error":"Invalid field name"},status=status.HTTP_400_BAD_REQUEST)
            else:
                self.choices[field_name].append(validated_data.get("value"))
                #Preventing duplication of values in list
                self.choices[field_name] = list(set(self.choices[field_name]))

                with open(self.CHOICE_DIR,"w") as file:
                    json.dump(self.choices,file)
                return Response({"status":"success","message":f"Added value '{validated_data.get('value')}' to field name '{field_name}'"},status=status.HTTP_200_OK)

    def delete(self,request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            validated_data = serializer.validated_data
            field_name = self.verify_fieldname(validated_data["field_name"])
            try:
                self.choices[field_name].remove(validated_data["value"])
                with open(self.CHOICE_DIR,"w") as file:
                    json.dump(self.choices,file)
                return Response({"status":f"Deleted {validated_data['value']} from choice list"},status=status.HTTP_200_OK)
            except ValueError:
                return Response({"error":"Inexistent value in field options"},status=status.HTTP_400_BAD_REQUEST)
