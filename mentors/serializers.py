from rest_framework import serializers

from users.models import PersonalProfile



experience_level_choices = (
    ("junior","junior"),
    ("mid","mid"),
    ("senior","senior")
)



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
    experience_level = serializers.ChoiceField(choices=experience_level_choices)

