from datetime import timedelta

# Django
from django.utils import timezone

# Django REST framework
from rest_framework import serializers

# Models
from activities.models import Activity, Property

# Serializers
from .property import PropertyNestedSerializer


def get_activities_by_property_and_hour(curr_property, schedule, activity_id=None):
    an_hour_after_schedule = schedule + timedelta(hours=1)
    an_hour_before_schedule = schedule - timedelta(hours=1)
    activities = Activity.objects.filter(
        property=curr_property,
        schedule__range=(an_hour_before_schedule, an_hour_after_schedule),
        status="active",
    )

    if activity_id:
        activities.filter(id != activity_id)

    return activities


class ActivitySerializer(serializers.ModelSerializer):
    property = PropertyNestedSerializer(read_only=True)
    property_id = serializers.IntegerField(write_only=True)
    condition = serializers.SerializerMethodField(read_only=True)
    survey = serializers.HyperlinkedRelatedField(
        read_only=True, view_name="survey-detail"
    )

    class Meta:
        model = Activity
        fields = "__all__"

    def get_condition(self, obj):
        condition = "unknown"
        if obj.status == "done":
            condition = "Finalizada"
        else:
            now = timezone.now()
            if obj.status == "active" and now > obj.schedule:
                condition = "Atrasada"
            elif obj.status == "active" and now <= obj.schedule:
                condition = "Pendiente a realizar"
        return condition

    def validate_property_id(self, value):

        if Property.objects.get(pk=value).status != "active":
            raise serializers.ValidationError("Property is not available.")

        return value

    def create(self, validated_data):
        property_id = validated_data.get("property_id")
        curr_property = Property.objects.get(pk=property_id)
        schedule = validated_data.get("schedule")
        activities = get_activities_by_property_and_hour(curr_property, schedule)

        if activities:
            raise serializers.ValidationError(
                "An activity has been schedule already at that time."
            )

        return Activity.objects.create(**validated_data)


class ScheduleActivitySerializer(serializers.Serializer):
    schedule = serializers.DateTimeField()

    def update(self, instance, validated_data):
        curr_property = instance.property
        schedule = validated_data.get("schedule")
        activities = get_activities_by_property_and_hour(
            curr_property, schedule, instance.id
        )

        if instance.status == "cancelled":
            raise serializers.ValidationError(
                "Cancelled activities can not be re-scheduled"
            )

        if activities:
            raise serializers.ValidationError(
                "An activity has been schedule already at that time."
            )

        instance.schedule = schedule
        instance.save()
        return instance


class StatusActivitySerializer(serializers.Serializer):
    status = serializers.CharField(max_length=35)

    def update(self, instance, validated_data):
        instance.status = validated_data.get("status")
        instance.save()
        return instance
