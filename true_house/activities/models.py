from django.db import models
from django.contrib.postgres.fields import JSONField


class Property(models.Model):
    title = models.CharField(max_length=255)
    address = models.TextField()
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    disabled_at = models.DateTimeField(null=True)
    status = models.CharField(max_length=35)


class Survey(models.Model):
    answers = JSONField()
    created_at = models.DateTimeField(auto_now_add=True)


class Activity(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    schedule = models.DateTimeField()
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=35)
    survey = models.OneToOneField(Survey, on_delete=models.CASCADE, null=True)
