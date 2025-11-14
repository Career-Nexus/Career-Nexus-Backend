from django.forms import fields
from rest_framework import serializers
from django.conf import settings

from . import models
from users.options import get_choices
from users.models import PersonalProfile

from users.serializers import industry_options

import os
import joblib
import uuid

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
CHOICES = get_choices()

employment_type = CHOICES["employment_category"]

work_type = CHOICES["work_type"]

experience_level = CHOICES["experience_level"]



class JobsSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    employment_type = serializers.ChoiceField(choices=employment_type)
    work_type = serializers.ChoiceField(choices=work_type)
    experience_level = serializers.ChoiceField(choices=experience_level)
    status = serializers.ChoiceField(choices=models.JOB_STATUS,default="active",required=False)

    class Meta:
        model = models.Jobs
        fields = ["id","title","organization","employment_type","work_type","country","salary","overview","description","experience_level","status"]

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
            "industry":job.industry,
            "experience_level":job.experience_level,
        }
        return output

    def update(self,instance,validated_data):
        all_attr = validated_data.keys()
        for attr in all_attr:
            value = validated_data.get(attr)
            setattr(instance,attr,value)
        instance.save()
        return instance




class RetrieveJobSerializer(serializers.ModelSerializer):
    is_saved = serializers.SerializerMethodField()

    class Meta:
        model = models.Jobs
        fields = ["id","title","organization","employment_type","work_type","country","salary","overview","description","experience_level","time_stamp","is_saved"]

    def get_is_saved(self,obj):
        user = self.context["user"]
        if models.SavedJobs.objects.filter(saver=user,job=obj).exists():
            return True
        else:
            return False

class RetrieveJobMiniSerializer(serializers.ModelSerializer):
    posted_on = serializers.SerializerMethodField()

    class Meta:
        model = models.Jobs
        fields = ["id","title","employment_type","salary","country","organization","posted_on"]

    def get_posted_on(self,obj):
        return obj.time_stamp


class RetrieveAppliedJobs(serializers.ModelSerializer):
    job = RetrieveJobMiniSerializer()

    class Meta:
        model = models.JobApplication
        fields = ["id","job"]


class JobApplicantSerializer(serializers.ModelSerializer):

    class Meta:
        model = PersonalProfile
        fields = ["id","first_name","last_name","middle_name","profile_photo","qualification","resume"]

class RetrieveRecentJobApplicantsSerializer(serializers.ModelSerializer):
    applicant = serializers.SerializerMethodField()
    job_name = serializers.SerializerMethodField()

    class Meta:
        model = models.JobApplication
        fields = ["id","applicant","job_name"]

    def get_applicant(self,obj):
        name = f"{obj.applicant.profile.first_name} {obj.applicant.profile.last_name}"
        return name

    def get_job_name(self,obj):
        return obj.job.title


class JobApplicationSerializer(serializers.Serializer):
    job = serializers.PrimaryKeyRelatedField(queryset=models.Jobs.objects.all())

    def validate_job(self,value):
        user = self.context["user"]
        if user.user_type == "employer":
            raise serializers.ValidationError("Employers are not allowed to apply for a job.")
        if value.status == "closed":
            raise serializers.ValidationError("This job has been closed")
        if models.JobApplication.objects.filter(job=value,applicant=user).exists():
            raise serializers.ValidationError("You have already applied for this job.")
        return value

    def create(self,validated_data):
        validated_data["applicant"] = self.context["user"]
        application = models.JobApplication.objects.create(**validated_data)
        return application


class RetrieveJobApplicationSerializer(serializers.ModelSerializer):
    applicant = serializers.SerializerMethodField()

    class Meta:
        model = models.JobApplication
        fields = ["id","applicant"]

    def get_applicant(self,obj):
        output = JobApplicantSerializer(obj.applicant.profile,many=False).data
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
        
        #Creating a custom combination for unique preferences with ref_no to be used in constructing Group_name in JobNotification consumer.
        preference_combination = f"{instance.title.lower().replace(' ','_')}_{instance.employment_type.lower()}_{instance.work_type.lower()}_{instance.industry.lower()}_{instance.experience_level.lower()}"
        
        if models.JobPreferenceSuffix.objects.filter(preference_combination=preference_combination).exists():
            pass
        else:
            models.JobPreferenceSuffix.objects.create(ref_no=str(uuid.uuid4()),preference_combination=preference_combination)
        return instance



class SaveJobSerializer(serializers.Serializer):
    job = serializers.PrimaryKeyRelatedField(queryset=models.Jobs.objects.all())

    def validate_job(self,value):
        user = self.context["user"]
        if models.SavedJobs.objects.filter(saver=user,job=value).exists():
            raise serializers.ValidationError("This Job has already been saved.")
        return value

    def create(self,validated_data):
        validated_data["saver"] = self.context["user"]
        output_instance = models.SavedJobs.objects.create(**validated_data)
        return output_instance

class UnsaveJobSerializer(serializers.Serializer):
    job = serializers.PrimaryKeyRelatedField(queryset=models.Jobs.objects.all())

    def validate(self,data):
        saver = self.context["user"]
        job = data["job"]

        saved_instance = models.SavedJobs.objects.filter(saver=saver,job=job)
        if not saved_instance.exists():
            raise serializers.ValidationError("This job has not been previously saved.")
        return saved_instance



class RetrieveSavedJobSerializer(serializers.ModelSerializer):
    job = JobsSerializer()

    class Meta:
        model = models.SavedJobs
        fields = ["job"]

class JobStatusUpdateSerializer(serializers.Serializer):
    job = serializers.PrimaryKeyRelatedField(queryset=models.Jobs.objects.all(),required=True)
    status = serializers.ChoiceField(choices=models.JOB_STATUS,required=True)

    def validate_job(self,value):
        user = self.context["user"]
        if value.poster != user:
            raise serializers.ValidationError("Job Posting belongs to another user.")
        return value

    def update(self,instance,validated_data):
        job = validated_data.get("job")
        job.status = validated_data.get("status")
        job.save()
        return job
