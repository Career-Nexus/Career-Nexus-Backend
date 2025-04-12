from rest_framework import serializers
from . import models

from users.models import Users, PersonalProfile



class FollowSerializer(serializers.ModelSerializer):
    #follower = serializers.PrimaryKeyRelatedField(queryset=Users.objects.all())
    user_following = serializers.PrimaryKeyRelatedField(queryset=Users.objects.all())

    class Meta:
        model=models.UserFollow
        fields = ["user_following"]

        read_only_fields = ["user_follower"]

    def validate(self,data):
        user_follower = self.context["user"]
        user_following = data.get("user_following")
        if user_follower == user_following:
            raise serializers.ValidationError({"error":"Cannot follow self"})
        else:
            if models.UserFollow.objects.filter(user_follower=user_follower,user_following=user_following).exists():
                raise serializers.ValidationError({"error":"User already followed"})
            else:
                data["user_follower"] = user_follower
                return data

    def create(self,validated_data):
        #validated_data["user_follower"] = self.context["user"]
        following = models.UserFollow.objects.create(**validated_data)
        output = {
                    "follower":following.user_follower.id,
                    "following":following.user_following.id,
                }
        return output

class RetrieveFollowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonalProfile
        fields = ["id","name","profile_photo","qualification"]
