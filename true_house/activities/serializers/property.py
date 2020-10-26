# Django REST framework
from rest_framework import serializers

# Models
from activities.models import Property


class PropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = "__all__"


class PropertyNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = ("id", "title", "address")
