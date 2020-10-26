# Django REST framework
from rest_framework import serializers

# Models
from activities.models import Survey


class SurveySerializer(serializers.ModelSerializer):
    class Meta:
        model = Survey
        fields = "__all__"
