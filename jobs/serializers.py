from rest_framework import serializers
from django.conf import settings

from . import models
from users.serializers import industry_options

import os
import joblib

BASE_DIR = settings.BASE_DIR
predictor_dir = os.path.join(BASE_DIR,"ML_Models")

model = os.path.join(predictor_dir,"industry_classifier_model.pkl")
binarizer = os.path.join(predictor_dir,"industry_label_binarizer.pkl")

predictor = joblib.load(model)
binarizer = joblib.load(binarizer)

def classify_jobs(text):
    prediction = predictor.predict([text])
    industries = binarizer.inverse_transform(prediction)
    output = ",".join(industries[0])
    if output == "":
        return "others"
    else:
        return output
#Valid Options
employment_type = (
    ("full_time","full_time"),
    ("part_time","part_time"),
    ("internship","internship"),
    ("freelance","freelance"),
    ("contract","contract")
)

work_type = (
    ("remote","remote"),
    ("onsite","onsite"),
    ("hybrid","hybrid")
)

experience_level = (
    ("entry","entry"),
    ("mid","mid"),
    ("senior","senior"),
    ("executive","executive")
)




class JobsSerializer(serializers.ModelSerializer):
    employment_type = serializers.ChoiceField(choices=employment_type)
    work_type = serializers.ChoiceField(choices=work_type)

    class Meta:
        model = models.Jobs
        fields = ["title","organization","employment_type","work_type","country","salary","overview","description"]

    def create(self,validated_data):
        validated_data["poster"] = self.context["user"]
        texts = f"{validated_data.get('overview','')}. {validated_data.get('description','')}"
        validated_data["industry"] = classify_jobs(texts)
        job = models.Jobs.objects.create(**validated_data)

        output = {
            "title":job.title,
            "organization":job.organization,
            "employment_type":job.employment_type,
            "work_type":job.work_type,
            "country":job.country,
            "salary":job.salary,
            "overview":job.overview,
            "description":job.description,
            "industry":job.industry
        }
        return output

class JobPreferenceSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=250)
    employment_type = serializers.ChoiceField(choices=employment_type)
    work_type = serializers.ChoiceField(choices=work_type)
    industry = serializers.ChoiceField(choices=industry_options)
    experience_level = serializers.ChoiceField(choices=experience_level)

    def update(self,instance,validated_data):
        instance.title = validated_data.get("title",instance.title)
        instance.employment_type = validated_data.get("employment_type",instance.employment_type)
        instance.work_type = validated_data.get("work_type",instance.work_type)
        instance.industry = validated_data.get("industry",instance.industry)
        instance.experience_level = validated_data.get("experience_level",instance.experience_level)
        instance.save()
        return instance


