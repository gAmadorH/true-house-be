from django.test import TestCase
from ..models import Property, Survey, Activity
from datetime import datetime
from django.utils import timezone


class PropertyTest(TestCase):
    """ Test module for Property model """

    def setUp(self):
        Property.objects.create(
            title="test 1",
            address="mexico",
            description="super property",
            status="active",
        )

    def test_property_fields(self):
        property = Property.objects.get(title="test 1")

        self.assertEqual(property.title, "test 1")
        self.assertEqual(property.address, "mexico")
        self.assertEqual(property.description, "super property")
        self.assertIsNotNone(property.created_at)
        self.assertIsNotNone(property.updated_at)
        self.assertIsNone(property.disabled_at)
        self.assertEqual(property.status, "active")


class SurveyTest(TestCase):
    """ Test module for Survey model """

    def setUp(self):
        Survey.objects.create(
            answers="",
        )

    def test_survey_fields(self):
        survey = Survey.objects.get()

        self.assertEqual(survey.answers, "")
        self.assertIsNotNone(survey.created_at)


class ActivityTest(TestCase):
    """ Test module for Activity model """

    def setUp(self):
        property = Property.objects.create(
            title="a property",
            address="mexico",
            description="super property",
            status="active",
        )
        Activity.objects.create(
            property=property,
            schedule=datetime.now(tz=timezone.utc),
            title="one tittle",
            status="active",
            survey=None,
        )

    def test_property_fields(self):
        activity = Activity.objects.get()

        self.assertIsNotNone(activity.property)
        self.assertIsNotNone(activity.schedule)
        self.assertEqual(activity.title, "one tittle")
        self.assertIsNotNone(activity.created_at)
        self.assertIsNotNone(activity.updated_at)
        self.assertEqual(activity.status, "active")
        self.assertIsNone(activity.survey)
