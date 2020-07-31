from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.core import validators

# Create your models here.
class User(AbstractUser):
    "User data"
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
        return f"{self.username}"


class UserProfile(models.Model):
    "Stores additional data from User."
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user_info"
    )
    nickname = models.CharField("Nickname", max_length=100)
    last_login = models.DateTimeField("Last login", auto_now_add=True)
    active = models.BooleanField("Active")
    created_at = models.DateField("Created at", auto_now_add=True)
    last_time_modified = models.DateTimeField("Last time modified", auto_now_add=True)


class Application(models.Model):
    """An application is an program who is installed on a machine and triggers many
    executions, generating event logs.
    """

    name = models.CharField("Name", max_length=50, null=False, default="App-Name")
    active = models.BooleanField("Active", null=False, default=True)
    description = models.TextField("Description", null=True)
    version = models.CharField("Version", max_length=8, null=True)
    
    def __str__(self):
        return f"{self.name} version {self.version}"


class Machine(models.Model):
    "An machine is the environment where the applications are installed"

    class MachineEnvChoices(models.TextChoices):
        "A Class to choose a variety of environment types"
        DEV = "DEV", "Development"
        PROD = "PROD", "Production"
        QA = "QA", "Quality Assurance"
        TEST = "TEST", "Test"

    name = models.CharField("Name", max_length=50, null=True)
    active = models.BooleanField("Active", null=False, default=True)
    environment = models.CharField(
        "Enviroment",
        max_length=30,
        choices=MachineEnvChoices.choices,
        default=MachineEnvChoices.DEV,
    )
    address = models.GenericIPAddressField(
        protocol="IPV4", validators=[validators.validate_ipv4_address], null=True
    )
    
    def __str__(self):
        return f"{self.name}|{self.environment}|{self.address}"


class Execution(models.Model):
    """An execution is a record of an start from an application. It is the
    beginning of an log record."""

    machine = models.ForeignKey(
        Machine, on_delete=models.deletion.DO_NOTHING, related_name="executions"
    )
    application = models.ForeignKey(
        Application,
        on_delete=models.deletion.DO_NOTHING,
        related_name="executions",
    )
    dateref = models.DateTimeField("DateRef", auto_now_add=True)
    success = models.BooleanField("Success", null=True)
    archived = models.BooleanField("Archived", default=False)


class Event(models.Model):
    "An event is the every log occurrence."
    
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
    description = models.TextField("Description")
    execution = models.ForeignKey(
        Execution, on_delete=models.deletion.CASCADE, related_name="related_execution"
    )

