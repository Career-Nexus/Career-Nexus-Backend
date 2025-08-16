from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

from rest_framework import serializers
from . import models

import uuid


class InformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Information
        fields = ["title","content","items"]

    def validate(self,data):
        title = data.get("title").lower().replace(" ","_")
        if models.Information.objects.filter(title=title).exists():
            raise serializers.ValidationError("Existent title")
        else:
            data["title"] = data["title"].lower().replace(" ","_")
            return data

    def create(self,validated_data):
        if validated_data.get("items"):
            validated_data["items"] = validated_data["items"].split(",")
        entry = models.Information.objects.create(**validated_data)
        output = {
            "title":entry.title,
            "content":entry.content,
            "items":entry.items,
        }
        return output



class AlterInformationSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=200,required=False)
    content = serializers.CharField(required=False)
    items = serializers.CharField(required=False)

    def update(self,instance,validated_data):
        instance.title = validated_data.get("title",instance.title)
        instance.content = validated_data.get("content",instance.content)
        instance.items = validated_data.get("items",instance.items)
        instance.save()
        return instance


class CountryPermitSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Countrycodes
        fields = ["id","country","code"]




class AlterCountryPermitSerializer(serializers.Serializer):
    country = serializers.PrimaryKeyRelatedField(queryset=models.Countrycodes.objects.all())
    status = serializers.ChoiceField(
        choices=(
            ("enable","enable"),
            ("disable","disable")
        )
    )

    def validate(self,data):
        #print(data["country"])
        country_obj = data["country"]
        status = data["status"]
        if country_obj.permitted == True and status == "enable":
            raise serializers.ValidationError("Country already permitted.")
        elif country_obj.permitted == False and status == "disable":
            raise serializers.ValidationError("Country already unpermitted.")
        else:
            if data["status"] == "enable":
                data["status"] = True
            else:
                data["status"] = False
            return data

    def create(self,validated_data):
        #Treat create as an update since we're modifying an existing object
        country_obj = validated_data.get("country")
        country_obj.permitted = validated_data.get("status")
        country_obj.save()
        return country_obj

class ChoiceFieldSerializer(serializers.Serializer):
    field_name = serializers.CharField(max_length=200,required=True)
    value = serializers.CharField(max_length=255,required=True)

class LibrarySerializer(serializers.Serializer):
    title = serializers.CharField(max_length=250)
    description = serializers.CharField()
    tags = serializers.JSONField()
    file = serializers.FileField()

    def validate_title(self,value):
        if models.Library.objects.filter(title__iexact=value).exists():
            raise serializers.ValidationError("A Library content with this title already exists.")
        return value

    def validate_tags(self,value):
        if not isinstance(value,list):
            raise serializers.ValidationError("Tags must be a list of Texts.")
        return value

    def validate_file(self,file):
        file_size = file.size 
        if (file_size/1000000) > 5:
            raise serializers.ValidationError("File too large.")
        return file

    def create(self,validated_data):
        file = validated_data.get("file")
        if file:
            file_name = f"Library/uploads/{str(uuid.uuid4())}_{file.name}"
            file_path = default_storage.save(file_name,ContentFile(file.read()))
            validated_data["file"] = default_storage.url(file_path)

        output_instance = models.Library.objects.create(**validated_data)
        return output_instance



class RetrieveLibrarySerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Library
        fields = ["id","title","description","tags","file"]
