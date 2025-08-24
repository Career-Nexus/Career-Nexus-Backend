from rest_framework import serializers

from . import models
from users.models import PersonalProfile
from follows.models import UserFollow

from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.utils.text import get_valid_filename
from django.db.models import Q

from users.tasks import send_email
from notifications.utils import notify, send_notification

import uuid
import joblib
import os





directory = os.path.dirname(os.path.abspath(__file__))
model_directory = os.path.join(directory,"models")
resources_directory = os.path.join(directory,"resources")
model_file = os.path.join(model_directory,"industry_classifier_model.pkl")
binarizer_file = os.path.join(model_directory,"industry_label_binarizer.pkl")


new_comment_template = os.path.join(resources_directory,"new_comment.html")
new_like_template = os.path.join(resources_directory,"post_like.html")
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
    pic1 = serializers.FileField(required=False,allow_null=False)
    pic2 = serializers.FileField(required=False,allow_null=False)
    pic3 = serializers.FileField(required=False,allow_null=False)
    video = serializers.FileField(required=False,allow_null=False)
    article = serializers.CharField(required=False,allow_null=False)

    def validate_format(self,filename,allowed_formats):
        if filename.lower().endswith(allowed_formats):
            return filename
        else:
            raise serializers.ValidationError("Invalid file format")

    def validate_size(self,file_size,permitted_size_in_bytes):
        if file_size/1000000 > permitted_size_in_bytes:
            raise serializers.ValidationError("File too large")
        else:
            return file_size

    def validate(self,data):
        request = self.context["request"]
        profile_instance = PersonalProfile.objects.get(user=request.user)
        data["profile"] = profile_instance
        return data
    
    def validate_pic1(self,file):
        self.validate_format(file.name,(".png",".jpg",".jpeg"))
        self.validate_size(file.size,1)
        return file

    def validate_pic2(self,file):
        self.validate_format(file.name,(".png",".jpg",".jpeg"))
        self.validate_size(file.size,1)
        return file

    def validate_pic3(self,file):
        self.validate_format(file.name,(".png",".jpg",".jpeg"))
        self.validate_size(file.size,1)
        return file

    def validate_video(self,file):
        self.validate_format(file.name,(".mp4",".webm"))
        self.validate_size(file.size,5)
        return file



    def create(self,validated_data):
        pic1 = validated_data.get("pic1","N/A")
        pic2 = validated_data.get("pic2","N/A")
        pic3 = validated_data.get("pic3","N/A")
        video = validated_data.get("video","N/A")
        validated_data["industries"] = classify_content(validated_data["body"])
        #TODO Allow article uploads

        if pic1 and hasattr(pic1,"read"):
            #Preventing malicious directory transversal with get_valid_filename
            file_name = f"posts/pic/{uuid.uuid4()}{get_valid_filename(pic1.name)}"
            file_path = default_storage.save(file_name,ContentFile(pic1.read()))
            validated_data["pic1"] = default_storage.url(file_path)

        if pic2 != "N/A":
            file_name = f"posts/pic/{uuid.uuid4()}{get_valid_filename(pic2.name)}"
            file_path = default_storage.save(file_name,ContentFile(pic2.read()))
            validated_data["pic2"] = default_storage.url(file_path)

        if pic3 != "N/A":
            file_name = f"posts/pic/{uuid.uuid4()}{get_valid_filename(pic3.name)}"
            file_path = default_storage.save(file_name,ContentFile(pic3.read()))
            validated_data["pic3"] = default_storage.url(file_path)

        if video != "N/A":
            file_name = f"posts/video/{uuid.uuid4()}{get_valid_filename(video.name)}"
            file_path = default_storage.save(file_name,ContentFile(video.read()))
            validated_data["video"] = default_storage.url(file_path)


        post = models.Posts.objects.create(**validated_data)
        output = {
                    "body":post.body,
                    "pic1":post.pic1,
                    "pic2":post.pic2,
                    "pic3":post.pic3,
                    "video":post.video,
                    "article":post.article,
                    "time_stamp":post.time_stamp
                }
        return output

class PersonalProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonalProfile
        fields = ["id","first_name","last_name","middle_name","profile_photo","qualification"]

class ParentPostSerializer(serializers.ModelSerializer):
    profile = PersonalProfileSerializer()
    class Meta:
        model = models.Posts
        fields = ["profile","body","pic1","pic2","pic3","video","article","time_stamp"]


class RetrievePostSerializer(serializers.ModelSerializer):
    comment_count = serializers.SerializerMethodField()
    #comment_count = serializers.IntegerField()
    like_count = serializers.SerializerMethodField()
    share_count = serializers.SerializerMethodField()
    profile = PersonalProfileSerializer()
    parent = ParentPostSerializer()
    can_like = serializers.SerializerMethodField()
    can_follow = serializers.SerializerMethodField()
    is_self = serializers.SerializerMethodField()
    is_saved = serializers.SerializerMethodField()

    class Meta:
        model = models.Posts
        fields = ["profile","id","body","pic1","pic2","pic3","video","article","time_stamp","comment_count","like_count","share_count","parent","can_like","can_follow","is_self","is_saved"]

    def get_is_saved(self,obj):
        user = self.context["user"]
        if models.PostSave.objects.filter(user=user,post=obj).exists():
            return True
        return False

    def get_is_self(self,obj):
        poster = obj.profile.user
        user = self.context["user"]
        if poster == user:
            return True
        else:
            return False

    def get_can_follow(self,obj):
        poster = obj.profile.user
        user = self.context.get("user")
        if poster == user:
            return False
        if UserFollow.objects.filter(user_follower=user,user_following=poster).exists():
            return False
        else:
            return True

    def get_can_like(self,obj):
        user = self.context.get("user")
        if user:
            if models.Like.objects.filter(post=obj,user=user).exists():
                return False
            else:
                return True
        return "N/A"

    def get_comment_count(self,obj):
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
    commenter = serializers.SerializerMethodField()
    body = serializers.CharField(max_length=5000)
    parent = serializers.PrimaryKeyRelatedField(queryset=models.Comment.objects.all())
    replies = serializers.SerializerMethodField()
    likes = serializers.SerializerMethodField()
    can_like = serializers.SerializerMethodField()

    class Meta:
        model = models.Comment
        fields = ["id","post","commenter","body","media","parent","replies","likes","time_stamp","can_like"]

    def get_can_like(self,obj):
        user = self.context["user"]
        if models.CommentLike.objects.filter(user=user,comment=obj).exists():
            return False
        else:
            return True


    def get_likes(self,obj):
        number_of_likes = models.CommentLike.objects.filter(comment=obj).count()
        return number_of_likes

    def get_replies(self,obj):
        replies = obj.replies.all()
        data = CommentSerializer(replies,context=self.context,many=True).data
        return data

    def get_commenter(self,obj):
        commenter_profile = obj.user.profile
        output = {
            "first_name":commenter_profile.first_name,
            "last_name":commenter_profile.last_name,
            "middle_name":commenter_profile.middle_name,
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
    media = serializers.ImageField(required=False)

    def validate_media(self,image):
        if image.size/1000000 > 1:
            raise serializers.ValidationError("Image size too large.")
        return image

    def create(self,validated_data):
        validated_data["user"] = self.context["request"].user
        post = validated_data.get("post")
        media = validated_data.get("media")
        if media:
            file_name = f"comments/media/{uuid.uuid4()}{get_valid_filename(media.name)}"
            file_path = default_storage.save(file_name,ContentFile(media.read()))
            validated_data["media"] = default_storage.url(file_path)
        comment = models.Comment.objects.create(**validated_data)
        #Email Notification for first comment
        post_owner = post.profile.user
        if post_owner.email_notify:
            text = post.body[0:30]
            container = {"{NAME}":post.profile.first_name,"{PHRASE}":text}
            if not models.Comment.objects.filter(post=post).first():
                send_email.delay(template=new_comment_template,subject="A New Comment",container=container,recipient=post_owner.email)

        output = {
                    "user":PersonalProfileSerializer(comment.user.profile,many=False).data,
                    "body":comment.body,
                    "media":comment.media,
                    "time_stamp":comment.time_stamp
                }
        return output

class CreateReplySerializer(serializers.Serializer):
    parent = serializers.PrimaryKeyRelatedField(queryset=models.Comment.objects.all())
    body = serializers.CharField(max_length=5000)

    def create(self,validated_data):
        user = self.context["request"].user
        validated_data["user"] = user
        validated_data["post"] = validated_data["parent"].post

        comment_owner = validated_data["parent"].user
        if user != comment_owner:
            send_notification(comment_owner,f"{user.profile.first_name} {user.profile.last_name} just replied to your comment.")

        comment = models.Comment.objects.create(**validated_data)
        output = {
                    "user":PersonalProfileSerializer(comment.user.profile,many=False).data,
                    "body":comment.body
                }
        return output

class CreateLikeSerializer(serializers.Serializer):
    post = serializers.PrimaryKeyRelatedField(queryset=models.Posts.objects.all())

    def validate(self,data):
        user = self.context["user"]
        if models.Like.objects.filter(user=user,post=data.get("post")).exists():
            raise serializers.ValidationError({"error":"Post Already Liked"})
        else:
            data["user"] = user
            return data
    
    def create(self,validated_data):
        post = validated_data.get("post")
        post_owner = post.profile.user
        if post_owner.email_notify:
            if not models.Like.objects.filter(post=post).first():
                container = {"{NAME}":post_owner.profile.first_name,"{PHRASE}":post.body[0:30]}
                send_email.delay(template=new_like_template,subject="Your Post Got a Like!!",container=container,recipient=post_owner.email)
                send_notification(post_owner,text="Someone just liked your post.")

        like = models.Like.objects.create(**validated_data)
        output = {
                    "post":like.post.id
                }
        return output

class UnlikePostSerializer(serializers.Serializer):
    post = serializers.PrimaryKeyRelatedField(queryset=models.Posts.objects.all())


    def validate(self,data):
        user = self.context["user"]
        post = data.get("post")
        if not models.Like.objects.filter(post=post,user=user).exists():
            raise serializers.ValidationError("Post is yet to be liked")
        data["user"] = user
        return data

    def create(self,validated_data):
        user = validated_data.get("user")
        post = validated_data.get("post")
        models.Like.objects.get(user=user,post=post).delete()
        output = {
            "status":"Unliked post"
        }
        return output



class CommentLikeSerializer(serializers.Serializer):
    comment = serializers.PrimaryKeyRelatedField(queryset=models.Comment.objects.all())

    def validate(self,data):
        user = self.context["user"]
        comment = data.get("comment")
        if models.CommentLike.objects.filter(user=user,comment=comment).exists():
            raise serializers.ValidationError("Comment already liked.")
        data["user"] = user
        return data

    def create(self,validated_data):
        instance = models.CommentLike.objects.create(**validated_data)

        user = validated_data["user"]
        comment_owner = validated_data.get("comment").user
        #if user != comment_owner:
        send_notification(comment_owner,f"{user.profile.first_name} {user.profile.last_name} just liked your comment.")

        return instance


class CommentUnlikeSerializer(serializers.Serializer):
    comment = serializers.PrimaryKeyRelatedField(queryset=models.Comment.objects.all())

    def validate(self,data):
        user = self.context["user"]
        comment = data.get("comment")
        if not models.CommentLike.objects.filter(user=user,comment=comment).exists():
            raise serializers.ValidationError("Comment has not been previously liked.")
        return data



class RepostSerializer(serializers.Serializer):
    parent = serializers.PrimaryKeyRelatedField(queryset=models.Posts.objects.all())
    body = serializers.CharField(max_length=2000,default="")

    def create(self,validated_data):
        user = self.context["user"]
        validated_data["profile"] = PersonalProfile.objects.get(user=user)
        parent = validated_data.get("parent")

        new_classification = classify_content(validated_data["body"])
        old_classification = validated_data["parent"].industries
        validated_data["industries"] = f"{old_classification},{new_classification}"

        #Check if the parent post was reposted and reference the main parent post instead.
        if parent.parent:
            validated_data["parent"] = parent.parent
        
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
    post = RetrievePostSerializer()
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

