from rest_framework import serializers

from users.models import PersonalProfile



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
