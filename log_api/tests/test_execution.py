import datetime
from django.test import TestCase
from django.urls import include, path, reverse
from rest_framework.test import APITestCase
from rest_framework.test import APIRequestFactory, URLPatternsTestCase
from rest_framework import status
from rest_framework.routers import DefaultRouter
from log_api.models import User, Application, Execution, Event, OperationSystem, Machine
from log_api import views

# Create your tests here.


class TestExecutionAPI(APITestCase):

    router = DefaultRouter()
    router.register(r"executions", views.ExecutionViewSet)

    urlpatterns = [path("", include(router.urls))]

    @classmethod
    def setUpTestData(cls):
        machine = Machine.objects.create(
            name="MachineTest1", active=True, environment="PROD", address="172.16.254.1"
        )
        application = Application.objects.create(
            name="ApplicationTest1", active=True, description="TestTest", version="1.0"
        )

        execution_test = Execution.objects.create(
            machine_id=machine,
            application_id=application,
            dateref=datetime.datetime.now().strftime(format="%Y-%m-%d"),
            success=True,
        )

    def test_create_execution(self):
        execution_data = dict(
            machine_id=1,
            application_id=1,
            dateref=datetime.datetime.now().strftime(format="%Y-%m-%d"),
            success=True,
        )

        response = self.client.post(
            "/executions/", execution_data, format="json", follow=True
        )
        self.assertEqual(
            response.status_code, status.HTTP_201_CREATED, msg=f"{response.data}"
        )
        self.assertEqual(Execution.objects.count(), 2)

    def test_retrieve_executions(self):
        response = self.client.get("/executions", follow=True)
        self.assertEqual(
            response.status_code, status.HTTP_200_OK, msg=f"{response.data}"
        )

    def test_retrieve_execution_by_id(self):
        response = self.client.get("/executions/1", follow=True)
        self.assertEqual(
            response.status_code, status.HTTP_200_OK, msg=f"{response.data}"
        )

    def test_delete_execution_is_not_allowed(self):
        response = self.client.delete("/executions/1/", follow=True)
        self.assertEqual(
            response.status_code,
            status.HTTP_405_METHOD_NOT_ALLOWED,
            msg=f"{response.data}",
        )
