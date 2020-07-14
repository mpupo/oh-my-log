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
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_extensions.routers import NestedRouterMixin
from log_api import views

# To make a nested api rotes like 'machines/1/os/2':
class NestedDefaultRouter(NestedRouterMixin, DefaultRouter):
    pass


router = NestedDefaultRouter()

# User Router:
user_router = router.register(r"users", views.UserViewSet)

# OS Router:
os_router = router.register(r"os", views.OperationSystemViewSet)
os_router.register(
    "installed-apps",
    views.ApplicationViewSet,
    basename="app-os",
    parents_query_lookups=["operationsystem"],
)

# Machine Router:
machines_router = router.register("machines", views.MachineViewSet)
machines_router.register(
    "os",
    views.OperationSystemViewSet,
    basename="machine-os",
    parents_query_lookups=["machine"],
)

# Applications router:
application_router = router.register("applications", views.ApplicationViewSet)


# Events router:
events_router = router.register("events", views.EventViewSet)

# Executions router:
executions_router = router.register("executions", views.ExecutionViewSet)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include(router.urls)),
]
