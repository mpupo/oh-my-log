from django.conf.urls import url

from log_api import views

urlpatterns = [
    url(
        regex=r'^machine/(?P<pk>[^/.]+)/relationships/(?P<related_field>[^/.]+)$',
        view=views.MachineRelationshipView.as_view(),
        name='machine-relationships'
    ),
    url(
        regex=r'^applications/(?P<pk>[^/.]+)/relationships/(?P<related_field>[^/.]+)$',
        view=views.ApplicationRelationshipView.as_view(),
        name='application-relationships'
    ),
    url(r'^machines/(?P<pk>[^/.]+)/(?P<related_field>\w+)/$',
        views.MachineViewSet.as_view({'get': 'retrieve_related'}),
        name='machine-related')
]
