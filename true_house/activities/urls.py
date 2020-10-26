from django.urls import include, path

from rest_framework.routers import DefaultRouter

from activities.views import ActivityViewSet, PropertyViewSet, SurveyViewSet

router = DefaultRouter()
router.register(r"activities", ActivityViewSet, basename="activity")
router.register(r"properties", PropertyViewSet, basename="property")
router.register(r"surveys", SurveyViewSet, basename="survey")

urlpatterns = [path("", include(router.urls))]
