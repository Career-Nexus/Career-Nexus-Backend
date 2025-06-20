#from django.utils import connection
from django.db.models.base import connection
from rest_framework import serializers

from . import models
from users.models import Users
from posts.serializers import PersonalProfileSerializer

from users.models import Users


status_options = (
    ("Accept","Accept"),
    ("Reject","Reject")
)


class ConnectionSerializer(serializers.ModelSerializer):
    connection = serializers.PrimaryKeyRelatedField(queryset=Users.objects.all())

    class Meta:
        model = models.Connection
        fields = ["connection"]

    def validate(self,data):
        user = self.context.get("user")
        connection = data.get("connection")
        if user == connection:
            raise serializers.ValidationError({"error":"Cannot connect with self"})
        elif models.Connection.objects.filter(user=user,connection=connection).exists() or models.Connection.objects.filter(user=connection,connection=user).exists():
            raise serializers.ValidationError({"error":"Connection Initiated"})
        else:
            data["user"] = user
            return data

    def create(self,validated_data):
        validated_data["status"] = "PENDING"
        connection_instance = models.Connection.objects.create(**validated_data)
        output = {
            "user":connection_instance.user.id,
            "connection":connection_instance.connection.id,
            "status":"PENDING"
        }
        return output


class RetrieveConnectionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    connection = serializers.SerializerMethodField()

    def get_connection(self,obj):
        user = self.context["user"]
        if obj.user == user:
            connection = obj.connection.profile
        else:
            connection = obj.user.profile
        data = PersonalProfileSerializer(connection).data 
        data["status"] = obj.status
        data["user_id"] = data.pop("id")
        return data


class ConnectionStatusSerializer(serializers.Serializer):
    connection_id = serializers.PrimaryKeyRelatedField(queryset=models.Connection.objects.all())
    status = serializers.ChoiceField(choices=status_options)

    def validate(self,data):
        user = self.context["user"]
        connect = data["connection_id"].connection
        if user != connect:
            raise serializers.ValidationError("Cannot Accept/Reject")
        elif data["connection_id"].status == "CONFIRMED":
            raise serializers.ValidationError("Connection already accepted")
        else:
            data["user"] = user
            return data 

    def create(self,validated_data):
        connection_instance = validated_data.get("connection_id")
        status = validated_data.get("status")
        if status == "Reject":
            connection_instance.delete()
            return {
                "status":"Rejected"
            }
        else:
            connection_instance.status = "CONFIRMED"
            connection_instance.save()
            return {
                "status":"Accepted"
            }

class RetrieveRecommendationDetailSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    qualification = serializers.SerializerMethodField()

    class Meta:
        model = Users
        fields = ["id","name","qualification"]

    def get_name(self,obj):
        return f"{obj.profile.first_name} {obj.profile.last_name}"

    def get_qualification(self,obj):
        qualification = obj.profile.qualification
        return qualification
