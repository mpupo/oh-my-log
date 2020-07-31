from django.conf.urls import url

from log_api import views

urlpatterns = [
    url(
        regex=r'^executions/(?P<pk>[^/.]+)/relationships/(?P<related_field>[^/.]+)$',
        view=views.ExecutionRelationshipView.as_view(),
        name='execution-relationships'
    ),
    url(r'^executions/(?P<pk>[^/.]+)/(?P<related_field>\w+)/$',
        views.ExecutionViewSet.as_view({'get': 'retrieve_related'}),
        name='execution-related'),
    url(
        regex=r'^events/(?P<pk>[^/.]+)/relationships/(?P<related_field>[^/.]+)$',
        view=views.EventRelationshipView.as_view(),
        name='event-relationships'
    ),
    url(r'^events/(?P<pk>[^/.]+)/(?P<related_field>\w+)/$',
        views.EventViewSet.as_view({'get': 'retrieve_related'}),
        name='event-related')
]
