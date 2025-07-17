from rest_framework import serializers
from users.options import get_choices

from users.models import PersonalProfile,Users


CHOICES = get_choices()

experience_level_choices= CHOICES["experience_level"]
availability_options = CHOICES["availability"]




class RetrieveMentorsSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    qualification = serializers.SerializerMethodField()
    position = serializers.SerializerMethodField()
    years_of_experience = serializers.SerializerMethodField()
    technical_skills = serializers.SerializerMethodField()

    class Meta:
        model = Users
        fields = ["id","name","qualification","position","years_of_experience","technical_skills"]

    def get_name(self,obj):
        return f"{obj.profile.first_name} {obj.profile.middle_name} {obj.profile.last_name}"

    def get_qualification(self,obj):
        return obj.profile.qualification

    def get_position(self,obj):
        return obj.profile.position

    def get_years_of_experience(self,obj):
        return obj.profile.years_of_experience

    def get_technical_skills(self,obj):
        return obj.profile.technical_skills





class MentorRecommendationSerializer(serializers.ModelSerializer):
    experience_level = serializers.SerializerMethodField()

    class Meta:
        model = PersonalProfile
        fields = ["first_name","last_name","middle_name","profile_photo","current_job","experience_level"]

    def get_experience_level(self,obj):
        if obj.years_of_experience:
            if obj.years_of_experience <= 2:
                return "Junior"
            elif obj.years_of_experience > 2 and obj.years_of_experience <=5:
                return "Mid"
            else:
                return "Senior"
        else:
            return "Junior"

class MentorSearchAndFilterSerializer(serializers.Serializer):
    text = serializers.CharField(max_length=1000,required=False)
    experience_level = serializers.ChoiceField(choices=experience_level_choices,required=False)
    skills = serializers.CharField(max_length=500,required=False)
    availability = serializers.ChoiceField(choices=availability_options,required=False)

