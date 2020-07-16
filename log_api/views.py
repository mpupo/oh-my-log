from django.shortcuts import render
from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework_extensions.mixins import NestedViewSetMixin
from rest_framework.parsers import FileUploadParser
from log_api.models import User, Machine, Application, Execution, Event
from log_api.serializers import (
    UserModelSerializer,
    MachineModelSerializer,
    ApplicationModelSerializer,
    EventModelSerializer,
    ExecutionModelSerializer,
)

# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserModelSerializer
    # permission_classes = [permissions.IsAuthenticated]


class MachineViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    queryset = Machine.objects.all()
    serializer_class = MachineModelSerializer


class ApplicationViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    queryset = Application.objects.all()
    serializer_class = ApplicationModelSerializer


class ExecutionViewSet(
    NestedViewSetMixin,
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Execution.objects.all()
    serializer_class = ExecutionModelSerializer


class EventViewSet(
    NestedViewSetMixin,
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Event.objects.all()
    serializer_class = EventModelSerializer
