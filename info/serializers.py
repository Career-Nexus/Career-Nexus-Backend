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



class AlterInformationSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=200,required=False)
    content = serializers.CharField(required=False)
    items = serializers.CharField(required=False)

    def update(self,instance,validated_data):
        instance.title = validated_data.get("title",instance.title)
        instance.content = validated_data.get("content",instance.content)
        instance.items = validated_data.get("items",instance.items)
        instance.save()
        return instance


class CountryPermitSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Countrycodes
        fields = ["id","country","code"]




class AlterCountryPermitSerializer(serializers.Serializer):
    country = serializers.PrimaryKeyRelatedField(queryset=models.Countrycodes.objects.all())
    status = serializers.ChoiceField(
        choices=(
            ("enable","enable"),
            ("disable","disable")
        )
    )

    def validate(self,data):
        #print(data["country"])
        country_obj = data["country"]
        status = data["status"]
        if country_obj.permitted == True and status == "enable":
            raise serializers.ValidationError("Country already permitted.")
        elif country_obj.permitted == False and status == "disable":
            raise serializers.ValidationError("Country already unpermitted.")
        else:
            if data["status"] == "enable":
                data["status"] = True
            else:
                data["status"] = False
            return data

    def create(self,validated_data):
        #Treat create as an update since we're modifying an existing object
        country_obj = validated_data.get("country")
        country_obj.permitted = validated_data.get("status")
        country_obj.save()
        return country_obj
