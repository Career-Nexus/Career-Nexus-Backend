from rest_framework import serializers

from . import models
from posts.serializers import PersonalProfileSerializer

from .utils import notify

from users.models import Users


class ChatSerializer(serializers.ModelSerializer):
    contributor = serializers.SerializerMethodField()

    class Meta:
        model = models.Chatroom
        fields = ["id","contributor"]

    def get_contributor(self,obj):
        user = self.context["user"]
        if obj.initiator == user:
            contributor_profile = obj.contributor.profile
        else:
            contributor_profile = obj.initiator.profile
        data = PersonalProfileSerializer(contributor_profile,many=False).data
        return data

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["chat_id"] = data.pop("id")
        return data

class ChatMessageSerializer(serializers.ModelSerializer):
    person = serializers.SerializerMethodField()

    class Meta:
        model = models.Message
        fields = ["person","message","timestamp"]

    def get_person(self,obj):
        person_profile = obj.person.profile
        data = PersonalProfileSerializer(person_profile,many=False).data
        return data

class NotificationSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Notification
        fields = ["id","text","timestamp"]

class TestNotificationSerializer(serializers.Serializer):
    user = serializers.PrimaryKeyRelatedField(queryset=Users.objects.all())
    message = serializers.CharField()

    def create(self,validated_data):
        user = validated_data.get("user")
        message = validated_data.get("message")
        notify(user.id,message)
        return {}
