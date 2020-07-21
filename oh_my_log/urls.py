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


router =  NestedDefaultRouter(trailing_slash=False)
router.register(r"users", views.UserViewSet)
applications_router = router.register(r"applications", views.ApplicationViewSet)
(applications_router.register(r"executions", views.ExecutionViewSet, basename='apps-executions', parents_query_lookups=['application_id'])
.register(r"events", views.EventViewSet, basename='apps-executions-events', parents_query_lookups=['execution_id_id', 'execution_id']))

router.register(r"executions/?", views.ExecutionViewSet)
router.register(r"events/?", views.EventViewSet)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
    url("api/", include('log_api.urls')),
    path("api/token", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh", TokenRefreshView.as_view(), name="token_refresh"),
]
