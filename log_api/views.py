from django.shortcuts import render
from rest_framework_json_api.views import RelationshipView, ModelViewSet
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


class MachineViewSet(NestedViewSetMixin, ModelViewSet):
    queryset = Machine.objects.all()
    serializer_class = MachineModelSerializer

class MachineRelationshipView(RelationshipView):
    queryset = Machine.objects

class ApplicationViewSet(ModelViewSet):
    queryset = Application.objects.all()
    serializer_class = ApplicationModelSerializer
    

    def get_queryset(self):
            queryset = super(ApplicationViewSet, self).get_queryset()

            # if this viewset is accessed via the 'order-lineitems-list' route,
            # it wll have been passed the `order_pk` kwarg and the queryset
            # needs to be filtered accordingly; if it was accessed via the
            # unnested '/lineitems' route, the queryset should include all LineItems
            if 'machine_pk' in self.kwargs:
                machine_pk = self.kwargs['machine_pk']
                queryset = queryset.filter(machine__pk=machine_pk)

            return queryset


class ApplicationRelationshipView(RelationshipView):
    queryset = Application.objects

class ExecutionViewSet(
    NestedViewSetMixin,
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
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
