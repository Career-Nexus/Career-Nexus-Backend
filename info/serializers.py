from rest_framework import serializers
from . import models


class InformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Information
        fields = ["title","content","items"]

    def validate(self,data):
        title = data.get("title").lower().replace(" ","_")
        if models.Information.objects.filter(title=title).exists():
            raise serializers.ValidationError("Existent title")
        else:
            data["title"] = data["title"].lower().replace(" ","_")
            return data

    def create(self,validated_data):
        if validated_data.get("items"):
            validated_data["items"] = validated_data["items"].split(",")
        entry = models.Information.objects.create(**validated_data)
        output = {
            "title":entry.title,
            "content":entry.content,
            "items":entry.items,
        }
        return output

    def update(self,instance,validated_data):
        instance.title = validated_data.get("title",instance.title)
        instance.content = validated_data.get("content",instance.content)
        instance.items = validated_data.get("items",instance.items)
        instance.save()
        return instance
