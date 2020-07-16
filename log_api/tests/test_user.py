import datetime
from django.test import TestCase
from django.urls import include, path, reverse
from rest_framework.test import APITestCase
from rest_framework.test import APIRequestFactory, URLPatternsTestCase
from rest_framework import status
from rest_framework.routers import DefaultRouter
from log_api.models import User, Application, Execution, Event, Machine
from log_api import views

# Create your tests here.


class TestUserAPI(APITestCase, URLPatternsTestCase):
    router = DefaultRouter()
    router.register(r"users", views.UserViewSet)

    urlpatterns = [path("", include(router.urls))]

    def test_create_user(self):
        user_data = dict(name="Murilo", email="murilo@gmail.com", password="123456789")
        response = self.client.post("/users/", user_data, format="json", follow=True)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().name, "Murilo")

    def test_retrieve_user_by_id(self):
        pass

    def test_delete_user(self):
        pass

    def test_edit_user(self):
        pass
