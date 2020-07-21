from rest_framework_json_api.views import RelationshipView, ModelViewSet
from rest_framework import viewsets, mixins
from rest_framework import permissions
from rest_framework_extensions.mixins import NestedViewSetMixin
from rest_framework import filters
from log_api.models import User,  Application, Execution, Event
from log_api.serializers import (
    UserModelSerializer,
    ApplicationModelSerializer,
    EventModelSerializer,
    ExecutionModelSerializer,
)

# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserModelSerializer
    # permission_classes = [permissions.IsAuthenticated]

class ApplicationViewSet(ModelViewSet):
    queryset = Application.objects.all()
    serializer_class = ApplicationModelSerializer
    
    
class ApplicationRelationshipView(RelationshipView):
    queryset = Application.objects

class ExecutionViewSet(
    NestedViewSetMixin,ModelViewSet,
):
    queryset = Execution.objects.all()
    serializer_class = ExecutionModelSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ("environment")
    
    

class ExecutionRelationshipView(RelationshipView):
    queryset = Execution.objects

class EventViewSet(
    NestedViewSetMixin,
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Event.objects.all()
    serializer_class = EventModelSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ("level")
    
class EventRelationshipView(RelationshipView):
    queryset = Event.objects