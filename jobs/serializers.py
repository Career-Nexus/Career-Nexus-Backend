from rest_framework import serializers
from django.conf import settings

from . import models

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




class JobsSerializer(serializers.ModelSerializer):

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
            "employement_type":job.employment_type,
            "work_type":job.work_type,
            "country":job.country,
            "salary":job.salary,
            "overview":job.overview,
            "description":job.description,
            "industry":job.industry
        }
        return output
