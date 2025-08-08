from . import models
from rest_framework import serializers

from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

import uuid



class CreateProjectCatalogueSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=150)
    description = serializers.CharField()
    image = serializers.ImageField(required=False)
    download_material = serializers.FileField(required=False)

    def validate_image(self,file):
        allowed_formats = (".png",".jpg",".jpeg")
        if not file.name.lower().endswith(allowed_formats):
            raise serializers.ValidationError("Image format is not supported.")
        if (file.size/1000000) > 1:
            raise serializers.ValidationError("Images size too large.")
        return file

    def validate_download_material(self,file):
        if (file.size/1000000) > 5:
            raise serializers.ValidationError("File too large.")
        return file

    def create(self,validated_data):
        image = validated_data.get("image")
        if image:
            file_name = f"portfolio/image/{str(uuid.uuid4())}{image.name}"
            file_path = default_storage.save(file_name,ContentFile(image.read()))
            validated_data["image"] = default_storage.url(file_path)

        download_material = validated_data.get("download_material")
        if download_material:
            file_name = f"portfolio/material/{str(uuid.uuid4())}{download_material.name}"
            file_path = default_storage.save(file_name,ContentFile(download_material.read()))
            validated_data["download_material"] = default_storage.url(file_path)

        validated_data["owner"] = self.context["user"]

        output_instance = models.ProjectCatalogue.objects.create(**validated_data)
        return output_instance




class ProjectCatalogueSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.ProjectCatalogue
        fields = ["id","title","description","image","download_material"]
