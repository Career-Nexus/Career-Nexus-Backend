from rest_framework import serializers

from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

from . import models

from users.models import Users
from posts.serializers import PersonalProfileSerializer

import uuid



class SubscribeSerializer(serializers.Serializer):
    #subscriber = serializers.PrimaryKeyRelatedField(queryset=Users.objects.all())

    def validate(self,data):
        user = self.context["user"]
        if models.NewsletterSubscribers.objects.filter(subscriber=user).exists():
            raise serializers.ValidationError("Already subscribed to NewsLetter.")
        data["subscriber"] = user
        return data

    def create(self,validated_data):
        output_instance = models.NewsletterSubscribers.objects.create(**validated_data)
        return output_instance


class NewsletterSubscriberSerializer(serializers.ModelSerializer):
    subscriber = serializers.SerializerMethodField()

    class Meta:
        model = models.NewsletterSubscribers
        fields = ["subscriber","subscribed_at"]

    def get_subscriber(self,obj):
        output = PersonalProfileSerializer(obj.subscriber.profile,many=False).data
        return output



class UnsubscribeSerializer(serializers.Serializer):

    def validate(self,data):
        user = self.context["user"]
        if not models.NewsletterSubscribers.objects.filter(subscriber=user).exists():
            raise serializers.ValidationError("Not previously subscribed to NewsLetter.")
        data["subscriber"] = user
        return data

    def create(self,validated_data):
        subscriber = validated_data.get("subscriber")
        models.NewsletterSubscribers.objects.filter(subscriber=subscriber).delete()
        return {
            "status":"Unsubscribed from Newsletter"
        }


class CreateNewsLetterSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=500)
    content = serializers.CharField()
    image = serializers.ImageField(required=False)

    def validate_image(self,file):
        permitted_formats = (".png",".jpg",".jpeg")
        if not file.name.lower().endswith(permitted_formats):
            raise serializers.ValidationError("Image format is not supported.")
        return file

    def create(self,validated_data):
        image = validated_data.get("image")

        if not image:
            validated_data["image"] = ""
        else:
            file_name = f"Newsletter/Images/{str(uuid.uuid4())}/{image.name}"
            file_path = default_storage.save(file_name,ContentFile(image.read()))
            validated_data["image"] = default_storage.url(file_path)

        output_instance =models.NewsLetter.objects.create(**validated_data)
        return output_instance

class NewsLetterSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.NewsLetter
        fields = ["title","content","image","timestamp"]


