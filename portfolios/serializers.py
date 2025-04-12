from . import models
from rest_framework import serializers

from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

import uuid



class RetrieveProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Project
    fields = ["title","description","image"]

class ProjectSerializer(serializers.ModelSerializer):
    image = serializers.ImageField()
    class Meta:
        model = models.Project
        fields = ["title","description","image"]

    def create(self,validated_data):
        validated_data["user"] = self.context["user"]
        image = validated_data.get("image","")

        if image != "":
            file_name = f"project/{uuid.uuid4()}{image.name}"
            file_path = default_storage.save(file_name,ContentFile(image.read()))
            validated_data["image"] = default_storage.url(file_path)
        else:
            validated_data["image"] = ""
        project = models.Project.objects.create(**validated_data)
        output = {
            "title":project.title,
            "description":project.description,
            "image":project.image
        }
        return output
