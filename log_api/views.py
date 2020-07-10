from django.shortcuts import render
from rest_framework import viewsets, mixins, generics, status
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework_extensions.mixins import NestedViewSetMixin
from log_api.models import User, Machine, OperationSystem
from log_api.serializers import (
    UserModelSerializer, MachineModelSerializer, OperationSystemModelSerializer)

# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserModelSerializer
    #permission_classes = [permissions.IsAuthenticated]

class MachineViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    queryset = Machine.objects.all()
    serializer_class = MachineModelSerializer

class OperationSystemViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    queryset = OperationSystem.objects.all()
    serializer_class = OperationSystemModelSerializer
