from django.shortcuts import render
from rest_framework_json_api.views import RelationshipView, ModelViewSet
from rest_framework_json_api import filters
from rest_framework_json_api import django_filters
from rest_framework.filters import SearchFilter
from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework_extensions.mixins import NestedViewSetMixin
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


class MachineViewSet(ModelViewSet):
    queryset = Machine.objects.all()
    serializer_class = MachineModelSerializer
    filter_backends = (filters.QueryParameterValidationFilter, filters.OrderingFilter,
                       django_filters.DjangoFilterBackend)
    filterset_fields = {
        "id": ("exact", "lt", "gt", "gte", "lte", "in"),
       "name": ("exact","contains"),
       "active": ("exact",),
       "environment": ("exact", "in", "contains"),
       "address": ("exact","in", "contains")
   }
    
    search_fields = ("machine", "application")

class ApplicationViewSet(ModelViewSet):
    queryset = Application.objects.all()
    serializer_class = ApplicationModelSerializer
    filter_backends = (filters.QueryParameterValidationFilter, filters.OrderingFilter,
                       django_filters.DjangoFilterBackend, SearchFilter)
    filterset_fields = {
        "id": ("exact", "lt", "gt", "gte", "lte", "in"),
        "name": ("exact", "in", "contains"),
       "active": ("exact",),
       "description": ("exact", "in", "contains"),
       "version": ("exact", "in", "contains"),
   }
    search_fields = ("name", "description")

class ExecutionViewSet(ModelViewSet):
    queryset = Execution.objects.all()
    serializer_class = ExecutionModelSerializer
    filter_backends = (filters.QueryParameterValidationFilter, filters.OrderingFilter,
                       django_filters.DjangoFilterBackend, SearchFilter)
    filterset_fields = {
        "id": ("exact", "lt", "gt", "gte", "lte", "in"),
       "archived": ("exact",),
       "machine": ("exact", "in"),
       "application": ("exact", "in"),
       "success": ("exact",)
   }
    
    search_fields = ("machine__name", "application__name")
    
class ExecutionRelationshipView(RelationshipView):
   queryset = Execution.objects.all()

class EventViewSet(NestedViewSetMixin,
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Event.objects.all()
    serializer_class = EventModelSerializer
    
    filter_backends = (filters.QueryParameterValidationFilter, filters.OrderingFilter,
                       django_filters.DjangoFilterBackend, SearchFilter)
    filterset_fields = {
        "id": ("exact", "lt", "gt", "gte", "lte", "in"),
       "level": ("icontains", "iexact", "contains"),
       "dateref": ("exact", "lt", "gt", "gte", "lte", "in"),
       "description": ("icontains", "iexact", "contains"),
       "execution": ("exact","in")
   }
    search_fields = ("level", "description")

class EventRelationshipView(RelationshipView):
   queryset = Event.objects.all()
