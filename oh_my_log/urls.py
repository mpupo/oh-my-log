"""oh_my_log URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls import url
from rest_framework.routers import DefaultRouter
from rest_framework_extensions.routers import NestedRouterMixin
from rest_framework_nested import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from log_api import views

# To make a nested api rotes like 'machines/1/apps/2':
class NestedDefaultRouter(NestedRouterMixin, DefaultRouter):
    pass


router = routers.SimpleRouter(trailing_slash=False)
router.register(r"users", views.UserViewSet)
router.register(r"applications", views.ApplicationViewSet)
router.register(r'machines', views.MachineViewSet)
router.register(r"events", views.EventViewSet)
router.register(r"executions", views.ExecutionViewSet)

# User Router:
#user_router = router.register(r"users/?", views.UserViewSet)

# Machine Router:
machines_app_router = routers.NestedSimpleRouter(router,'machines', lookup='machine')
machines_app_router.register(
    "applications",
    views.ApplicationViewSet,
    basename="machines-applications"
)
apps_execs_router = routers.NestedSimpleRouter(machines_app_router, 'applications', lookup='application')
apps_execs_router.register("executions", views.ExecutionViewSet, basename='machines-applications-executions')

execs_events_router = routers.NestedSimpleRouter(apps_execs_router, 'executions', lookup='execution')
execs_events_router.register("events", views.EventViewSet, basename='machine-applications-executions-events')


# Applications router:
#application_router = router.register(r"applications/?", views.ApplicationViewSet, basename="apps")

# Events router:
#events_router = router.register(r"events/?", views.EventViewSet)

# Executions router:
#executions_router = router.register(r"executions/?", views.ExecutionViewSet)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
    path("api/", include(machines_app_router.urls)),
    path("api/", include(apps_execs_router.urls)),
    path("api/", include(execs_events_router.urls)),
    url("api/", include('log_api.urls')),
    path("api/token", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh", TokenRefreshView.as_view(), name="token_refresh"),
]
