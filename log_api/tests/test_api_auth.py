import datetime
from django.test import TestCase
from django.urls import include, path, reverse
from rest_framework.test import APITestCase
from rest_framework.test import APIRequestFactory, URLPatternsTestCase
from rest_framework import status
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from log_api.models import User
from log_api import views

# Create your tests here.


class TestUserAPI(APITestCase, URLPatternsTestCase):
    router = DefaultRouter()
    router.register(r"users", views.UserViewSet)

    urlpatterns = [
        path("api", include(router.urls)),
        path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
        path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    ]

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(
            username="Murilo", email="murilo@gmail.com", password="123456789"
        )

    def test_get_token(self):
        response_token = self.client.post(
            reverse("token_obtain_pair"),
            {
                "username": "Murilo",
                "email": "murilo@gmail.com",
                "password": "123456789",
            },
            format="json",
            follow=True,
        )
        self.assertEqual(
            response_token.status_code, status.HTTP_200_OK, msg=f"{response_token.data}"
        )

    def test_refresh_token(self):
        request_token = self.client.post(
            reverse("token_obtain_pair"),
            {
                "username": "Murilo",
                "email": "murilo@gmail.com",
                "password": "123456789",
            },
            format="json",
            follow=True,
        )
        test_token = request_token.data["refresh"]
        response_token_refresh = self.client.post(
            reverse("token_refresh"),
            {"refresh": test_token},
            format="json",
            follow=True,
        )
        self.assertEqual(
            response_token_refresh.status_code,
            status.HTTP_200_OK,
            msg=f"{response_token_refresh.data}",
        )
