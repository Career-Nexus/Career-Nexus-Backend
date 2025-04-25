from rest_framework import serializers

from . import models
from users.models import PersonalProfile

from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

import uuid
import joblib
import os

directory = os.path.dirname(os.path.abspath(__file__))
model_directory = os.path.join(directory,"models")
model_file = os.path.join(model_directory,"industry_classifier_model.pkl")
binarizer_file = os.path.join(model_directory,"industry_label_binarizer.pkl")

model = joblib.load(model_file)
binarizer = joblib.load(binarizer_file)

def classify_content(text):
    prediction = model.predict([text])
    industries = binarizer.inverse_transform(prediction)
    output = ",".join(industries[0])
    if output == "":
        return "others"
    else:
        return output



class PostSerializer(serializers.Serializer):
    body = serializers.CharField(max_length=10000)
    media = serializers.FileField(required=False)
    article = serializers.CharField(required=False)

    def validate(self,data):
        request = self.context["request"]
        profile_instance = PersonalProfile.objects.get(user=request.user)
        data["profile"] = profile_instance
        return data


    def create(self,validated_data):
        media = validated_data.get("media","")
        validated_data["industries"] = classify_content(validated_data["body"])
        #article = validated_data.get("article","")

        if media != "":
            file_name = f"posts/media/{uuid.uuid4()}{media.name}"
            file_path = default_storage.save(file_name,ContentFile(media.read()))
            validated_data["media"] = default_storage.url(file_path)
        #if article != "":
            #file_name = f"posts/article/{uuid.uuid4()}{article.name}"
            #file_path = default_storage.save(file_name,ContentFile(article.read()))
            #validated_data["article"] = default_storage.url(file_path)

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

class ParentPostSerializer(serializers.ModelSerializer):
    profile = PersonalProfileSerializer()
    class Meta:
        model = models.Posts
        fields = ["profile","body","media","article","time_stamp"]


class RetrievePostSerializer(serializers.ModelSerializer):
    comment_count = serializers.SerializerMethodField()
    #comment_count = serializers.IntegerField()
    like_count = serializers.SerializerMethodField()
    share_count = serializers.SerializerMethodField()
    profile = PersonalProfileSerializer()
    parent = ParentPostSerializer()

    class Meta:
        model = models.Posts
        fields = ["profile","id","body","media","article","time_stamp","comment_count","like_count","share_count","parent"]

    def get_comment_count(self,obj):
        #comments = obj.comment_set.all()
        comments = models.Comment.objects.filter(post=obj,parent__isnull=True)
        return len(comments)
    def get_like_count(self,obj):
        likes = obj.like_set.all()
        return len(likes)
    def get_share_count(self,obj):
        shares = obj.share_set.all()
        return len(shares)
    def to_representation(self,instance):
        representation = super().to_representation(instance)
        representation["post_id"] = representation.pop("id")
        #representation["poster"] = representation.pop("profile")
        return representation

    #def get_mainpost(self,obj):
        #parents = obj.mainpost.all()
        #data = RetrievePostSerializer(parents,many=True).data
        #return data


class CommentSerializer(serializers.ModelSerializer):
    post = serializers.PrimaryKeyRelatedField(queryset=models.Posts.objects.all())
    #user = serializers.StringRelatedField()
    commenter = serializers.SerializerMethodField()
    body = serializers.CharField(max_length=5000)
    parent = serializers.PrimaryKeyRelatedField(queryset=models.Comment.objects.all())
    #replies = serializers.PrimaryKeyRelatedField(many=True,read_only=True)
    replies = serializers.SerializerMethodField()

    class Meta:
        model = models.Comment
        fields = ["id","post","commenter","body","parent","replies","time_stamp"]

    def get_replies(self,obj):
        replies = obj.replies.all()
        data = CommentSerializer(replies,many=True).data
        return data
    def get_commenter(self,obj):
        commenter_profile = obj.user.profile
        output = {
            "name":commenter_profile.name,
            "profile_picture":commenter_profile.profile_photo
        }
        return output
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["comment_id"] = representation.pop("id")
        return representation



class CreateCommentSerializer(serializers.Serializer):
    post = serializers.PrimaryKeyRelatedField(queryset=models.Posts.objects.all())
    body = serializers.CharField(max_length=5000)

    def create(self,validated_data):
        validated_data["user"] = self.context["request"].user
        comment = models.Comment.objects.create(**validated_data)
        output = {
                    "user":comment.user.name,
                    "body":comment.body,
                    "time_stamp":comment.time_stamp
                }
        return output

class CreateReplySerializer(serializers.Serializer):
    parent = serializers.PrimaryKeyRelatedField(queryset=models.Comment.objects.all())
    body = serializers.CharField(max_length=5000)

    def create(self,validated_data):
        validated_data["user"] = self.context["request"].user
        validated_data["post"] = validated_data["parent"].post
        comment = models.Comment.objects.create(**validated_data)
        output = {
                    "user":comment.user.name,
                    "body":comment.body
                }
        return output

class CreateLikeSerializer(serializers.Serializer):
    post = serializers.PrimaryKeyRelatedField(queryset=models.Posts.objects.all())
    #user = serializers.PrimaryKeyRelatedField(queryset=)

    def validate(self,data):
        user = self.context["user"]
        if models.Like.objects.filter(user=user,post=data.get("post")).exists():
            raise serializers.ValidationError({"error":"Post Already Liked"})
        else:
            data["user"] = user
            return data
    
    def create(self,validated_data):
        #validated_data["user"] = self.context["user"]
        like = models.Like.objects.create(**validated_data)
        output = {
                    "post":like.post.id
                }
        return output

class RepostSerializer(serializers.Serializer):
    parent = serializers.PrimaryKeyRelatedField(queryset=models.Posts.objects.all())
    body = serializers.CharField(max_length=2000,default="")

    def create(self,validated_data):
        user = self.context["user"]
        validated_data["profile"] = PersonalProfile.objects.get(user=user)
        #validated_data["body"] = ""
        repost = models.Posts.objects.create(**validated_data)
        output = ParentPostSerializer(repost)
        return output.data

class SavePostSerializer(serializers.ModelSerializer):
    post = serializers.PrimaryKeyRelatedField(queryset=models.Posts.objects.all())

    class Meta:
        model = models.PostSave
        fields = ["post"]

    def create(self,validated_data):
        validated_data["user"] = self.context["user"]
        save = models.PostSave.objects.create(**validated_data)
        output = {
                    "post_id":save.post.id 
                }
        return output

class RetrieveSavePostSerializer(serializers.ModelSerializer):
    post = ParentPostSerializer()
    class Meta:
        model = models.PostSave
        fields = ["post"]

class ShareSerializer(serializers.ModelSerializer):
    post = serializers.PrimaryKeyRelatedField(queryset=models.Posts.objects.all())

    class Meta:
        model = models.Share
        fields = ["post","user"]

        read_only_fields = ["user"]

    def create(self,validated_data):
        validated_data["user"] = self.context["user"]
        models.Share.objects.create(**validated_data)
        return {
                "post_id":validated_data["post"].id
                }

