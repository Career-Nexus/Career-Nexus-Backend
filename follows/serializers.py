from rest_framework import serializers
from . import models

from users.models import Users, PersonalProfile
from users.views import delete_cache

from notifications.utils import send_notification



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

        send_notification(following.user_following,f"{following.user_follower.profile.first_name} {following.user_follower.profile.last_name} just followed you.",page="Profile",route=f"/user/retrieve-profile/?user_id={following.user_follower.id}",obj_id=following.user_follower.id)

        output = {
                    "follower":following.user_follower.id,
                    "following":following.user_following.id,
                }
        #Clear cahes to avoid returning stale data
        delete_cache(f"{following.user_follower.id}_profile")
        delete_cache(f"{following.user_following.id}_profile")
        return output


class UnfollowSerializer(serializers.Serializer):
    user_following = serializers.PrimaryKeyRelatedField(queryset=Users.objects.all())

    def validate(self,data):
        user = self.context["user"]
        user_following = data.get("user_following")
        if user == user_following:
            raise serializers.ValidationError("Cannot follow/unfollow self.")
        if not models.UserFollow.objects.filter(user_follower=user,user_following=user_following).exists():
            raise serializers.ValidationError("This user is not currently being followed.")
        data["user"] = user
        return data

    def create(self,validated_data):
        user_follower = validated_data.get("user")
        user_following = validated_data.get("user_following")

        #Clear cahes to avoid returning stale data
        delete_cache(f"{user_follower.id}_profile")
        delete_cache(f"{user_following.id}_profile")

        models.UserFollow.objects.get(user_follower=user_follower,user_following=user_following).delete()
        output = {
            "status":"Unfollowed user"
        }
        return output






class RetrieveFollowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonalProfile
        fields = ["id","first_name","last_name","middle_name","profile_photo","qualification"]
