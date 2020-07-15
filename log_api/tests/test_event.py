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


class TestEvents(APITestCase, URLPatternsTestCase):
    router = DefaultRouter()
    router.register(r"events", views.EventViewSet)

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

    def test_create_event(self):
        event_data = dict(
            level="DEBUG",
            dateref="2020-07-10T00:00:06.111Z",
            archived=False,
            description="error in System.Out.PrintIn",
            execution_id=1,
        )
        response = self.client.post("/events/", event_data, format="json", follow=True)
        self.assertEqual(
            response.status_code, status.HTTP_201_CREATED, msg=f"{response.data}"
        )
        self.assertEqual(Event.objects.count(), 1)
