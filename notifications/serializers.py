from rest_framework import serializers

from . import models
from posts.serializers import PersonalProfileSerializer


class ChatSerializer(serializers.ModelSerializer):
    initiator = serializers.SerializerMethodField()
    contributor = serializers.SerializerMethodField()

    class Meta:
        model = models.Chatroom
        fields = ["id","initiator","contributor"]

    def get_initiator(self,obj):
        initiator_profile = obj.initiator.profile 
        data = PersonalProfileSerializer(initiator_profile,many=False).data
        return data

    def get_contributor(self,obj):
        contributor_profile = obj.contributor.profile
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
