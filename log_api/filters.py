from django_filters import rest_framework as filters
from log_api.models import Event, Execution


class ExecutionFilterSet(filters.FilterSet):
 
    class Meta:
        model = Execution
        fields = {
            'environment': ['iexact']}

class EventFilterSet(filters.FilterSet):
    level = filters.ChoiceFilter(lookup_expr='exact')
    class Meta:
        model = Event
        fields = {
            'level': ['iexact'],
            'frequency': ['a']}
        