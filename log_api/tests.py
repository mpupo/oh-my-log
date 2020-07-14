import datetime
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

    def test_retrieve_user_by_id(self):
        pass

    def test_delete_user(self):
        pass

    def test_edit_user(self):
        pass


class TestExecutionAPI(APITestCase, URLPatternsTestCase):

    router = DefaultRouter()
    router.register(r'executions', views.ExecutionViewSet)

    urlpatterns = [
        path('', include(router.urls))
    ]

    def test_create_execution(self):
        execution_data = dict(
            machine_id=1,
            application_id=1,
            dateref=str(datetime.datetime.now()),
            success=True)

        response = self.client.post('/executions/', execution_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Execution.objects.count(),1)

    def test_retrieve_executions(self):
        response = self.client.get('/executions')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_execution_by_id(self):
        response = self.client.get('/executions/1')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_delete_execution_by_id(self):
        response = self.client.delete('/executions/1')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)