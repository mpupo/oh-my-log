from django.test import TestCase
from django.urls import include, path, reverse
from rest_framework.test import APITestCase
from rest_framework.test import APIRequestFactory, URLPatternsTestCase
from rest_framework import status
from rest_framework.routers import DefaultRouter
from log_api.models import User
from log_api import views

# Create your tests here.

class TestUserLocal(TestCase):
    def setUp(self):
        user_1 = User.objects.create(name='Murilo',email='murilo@gmail.com', password='123456789')
        user_2 = User.objects.create(name='Fulano',email='fulano@gmail.com', password='123456789')
        user_3 = User.objects.create(name='Ciclano',email='ciclano@gmail.com', password='123456789')

    def test_get_user_Fulano(self):
        user = User.objects.get(name='Fulano')
        self.assertEqual(user.email, 'fulano@gmail.com')
    
    def test_get_all_test_users(self):
        users = User.objects.all()
        self.assertEqual(users.count(), 3)

class TestUserAPI(APITestCase, URLPatternsTestCase):

    router = DefaultRouter()
    router.register(r'users', views.UserViewSet)

    urlpatterns = [
        path('', include(router.urls))
    ]

    def test_create_user(self):
        user_data = dict(name='Murilo',email='murilo@gmail.com', password='123456789')
        response = self.client.post('/users/', user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(),1)
        self.assertEqual(User.objects.get().name, 'Murilo')
