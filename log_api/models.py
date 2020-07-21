from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.core import validators

# Create your models here.
class User(AbstractUser):
    "User model"
    username = models.CharField("Name", max_length=100, unique=True)
    email = models.EmailField(
        _("Email address"),
        max_length=254,
        validators=[validators.EmailValidator()],
        unique=True,
    )

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email", "first_name", "last_name"]

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class UserProfile(models.Model):
    "User Profile model"
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile"
    )
    nickname = models.CharField("Nickname", max_length=100)
    last_login = models.DateTimeField("Last login", auto_now_add=True)
    active = models.BooleanField("Active")
    created_at = models.DateField("Created at", auto_now_add=True)
    last_time_modified = models.DateTimeField("Last time modified", auto_now_add=True)


class Application(models.Model):
    "Application model"

    name = models.CharField("Name", max_length=50, null=False, default="App-Name")
    active = models.BooleanField("Active", null=False, default=True)
    description = models.TextField("Description", null=True)
    version = models.CharField("Version", max_length=8, null=True)


class Execution(models.Model):
    "Execution model"

    class ExecutionEnvChoices(models.TextChoices):
        "A Class to choose a variety of environment types"
        DEV = "DEV", "Development"
        PROD = "PROD", "Production"
        QA = "QA", "Quality Assurance"
        TEST = "TEST", "Test"

    application_id = models.ForeignKey(
        Application,
        on_delete=models.deletion.CASCADE,
        related_name="apps",
    )

    environment = models.CharField(
        "Enviroment",
        max_length=30,
        choices=ExecutionEnvChoices.choices,
        default=ExecutionEnvChoices.DEV,
    )

    dateref = models.DateTimeField("DateRef", auto_now_add=True)
    success = models.BooleanField("Success", null=False)


class Event(models.Model):
    "Event model"

    class EventLevelChoices(models.TextChoices):
        "A Class to choose a variety of event types"
        CRITICAL = "CRITICAL", "CRITICAL"
        DEBUG = "DEBUG", "DEBUG"
        WARNING = "WARNING", "WARNING"
        INFO = "INFO", "INFO"

    level = models.CharField(
        "Level",
        max_length=20,
        choices=EventLevelChoices.choices,
        default=EventLevelChoices.INFO,
    )
    dateref = models.DateTimeField("DateRef")
    archived = models.BooleanField("Archived")
    description = models.TextField("Description")
    execution_id = models.ForeignKey(
        Execution, on_delete=models.deletion.CASCADE, related_name="events"
    )
