from django.shortcuts import render
from rest_framework import viewsets, mixins, generics, status
from rest_framework.response import Response
from rest_framework import permissions
from log_api.models import User
from log_api.serializers import UserModelSerializer

# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserModelSerializer
    #permission_classes = [permissions.IsAuthenticated]