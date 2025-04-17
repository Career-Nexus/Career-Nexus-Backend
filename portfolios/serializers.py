from . import models
from rest_framework import serializers

from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

import uuid



class RetrieveProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Project
        fields = ["cover_image","title","description","role","tools","image"]

class ProjectSerializer(serializers.ModelSerializer):
    image = serializers.ImageField()
    cover_image = serializers.ImageField()
    class Meta:
        model = models.Project
        fields = ["cover_image","role","tools","title","description","image"]

    def create(self,validated_data):
        validated_data["user"] = self.context["user"]
        image = validated_data.get("image","")
        cover_image = validated_data.get("cover_image","")

        if cover_image != "":
            image_name = f"project/{uuid.uuid4()}{cover_image.name}"
            path = default_storage.save(image_name,ContentFile(cover_image.read()))
            validated_data["cover_image"] = default_storage.url(path)
        else:
            validated_data["cover_image"] = ""

        if image != "":
            file_name = f"project/{uuid.uuid4()}{image.name}"
            file_path = default_storage.save(file_name,ContentFile(image.read()))
            validated_data["image"] = default_storage.url(file_path)
        else:
            validated_data["image"] = ""
        project = models.Project.objects.create(**validated_data)
        output = {
            "cover_image":project.cover_image,
            "title":project.title,
            "description":project.description,
            "role":project.role,
            "tools":project.tools,
            "image":project.image,
        }
        return output
