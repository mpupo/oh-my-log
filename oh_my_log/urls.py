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
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_extensions.routers import NestedRouterMixin
from log_api import views


class NestedDefaultRouter(NestedRouterMixin, routers.DefaultRouter):
    pass

#router = routers.SimpleRouter(trailing_slash=False)
router = NestedDefaultRouter(trailing_slash=False)
router.register(r"users/?", views.UserViewSet)
router.register(r"applications/?", views.ApplicationViewSet)
router.register(r'machines/?', views.MachineViewSet)
execution_router = router.register(r"executions/?", views.ExecutionViewSet)
execution_router.register(r"events/?", views.EventViewSet, basename='executions-events', parents_query_lookups=['execution_id', 'execution'])

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
    url("api/", include('log_api.urls')),
    path("api/token", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh", TokenRefreshView.as_view(), name="token_refresh"),
]
