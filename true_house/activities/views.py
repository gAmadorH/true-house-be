from datetime import datetime, timedelta

from rest_framework import status, mixins, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from activities.serializers import (
    ActivitySerializer,
    StatusActivitySerializer,
    ScheduleActivitySerializer,
    PropertySerializer,
    SurveySerializer,
)

from activities.models import Activity, Property, Survey


class ActivityViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = ActivitySerializer

    def get_queryset(self):
        queryset = Activity.objects.all()

        q_from = self.request.query_params.get("from", None)
        q_to = self.request.query_params.get("to", None)
        q_status = self.request.query_params.get("status", None)

        if self.action == "list":
            if (q_from and q_to) or q_status:
                if q_from and q_to:
                    queryset.filter(schedule__range=(q_from, q_to))
                if q_status:
                    queryset.filter(status=q_status)
            else:
                now = datetime.now()
                high_l = now + timedelta(weeks=2)
                low_l = now - timedelta(days=3)
                queryset = queryset.filter(schedule__range=(low_l, high_l))

        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = ActivitySerializer(
            queryset, context={"request": request}, many=True
        )

        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["patch"])
    def schedule(self, request, pk=None):
        activity = self.get_object()
        serializer = ScheduleActivitySerializer(activity, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=["patch"])
    def status(self, request, pk=None):
        activity = self.get_object()
        serializer = StatusActivitySerializer(activity, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_204_NO_CONTENT)


class PropertyViewSet(viewsets.ModelViewSet):
    serializer_class = PropertySerializer
    queryset = Property.objects.all()


class SurveyViewSet(viewsets.ModelViewSet):
    serializer_class = SurveySerializer
    queryset = Survey.objects.all()
