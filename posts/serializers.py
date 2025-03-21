from rest_framework import serializers

from . import models
from users.models import PersonalProfile

from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

import uuid

class PostSerializer(serializers.Serializer):
    body = serializers.CharField(max_length=10000)
    media = serializers.FileField(required=False)
    article = serializers.FileField(required=False)

    def validate(self,data):
        request = self.context["request"]
        profile_instance = PersonalProfile.objects.get(user=request.user)
        data["profile"] = profile_instance
        return data


    def create(self,validated_data):
        media = validated_data.get("media","")
        article = validated_data.get("article","")

        if media != "":
            file_name = f"posts/media/{uuid.uuid4()}{media.name}"
            file_path = default_storage.save(file_name,ContentFile(media.read()))
            validated_data["media"] = default_storage.url(file_path)
        if article != "":
            file_name = f"posts/article/{uuid.uuid4()}{article.name}"
            file_path = default_storage.save(file_name,ContentFile(article.read()))
            validated_data["article"] = default_storage.url(file_path)

        post = models.Posts.objects.create(**validated_data)
        output = {
                    "body":post.body,
                    "media":post.media,
                    "article":post.article,
                    "time_stamp":post.time_stamp
                }
        return output

class PersonalProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonalProfile
        fields = ["id","name","profile_photo","qualification"]

class RetrievePostSerializer(serializers.ModelSerializer):
    profile = PersonalProfileSerializer()
    class Meta:
        model = models.Posts
        fields = ["profile","id","body","media","article","time_stamp"]

