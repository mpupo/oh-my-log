from django.db import models
from django.core import validators

# Create your models here.
class User(models.Model):
    "User model"
    name = models.CharField("Name", max_length=50)
    email = models.EmailField(
        "E-mail", max_length=254, validators=[validators.EmailValidator()]
    )
    password = models.CharField(
        "Password", max_length=50, validators=[validators.MinLengthValidator(8)]
    )
    last_login = models.DateTimeField("Last login", auto_now_add=True)


class Group(models.Model):
    pass


class Application(models.Model):
    "Application model"

    name = models.CharField("Name", max_length=50, null=False, default="App-Name")
    active = models.BooleanField("Active", null=False, default=True)
    description = models.TextField("Description", null=True)
    version = models.CharField("Version", max_length=8, null=True)


class OperationSystem(models.Model):
    "Operation systems model"

    name = models.CharField("Name", max_length=50)
    version = models.CharField("Version", max_length=8)
    installed_apps = models.ManyToManyField(Application)


class Machine(models.Model):
    "Machine model"

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
    operation_systems = models.ManyToManyField(OperationSystem)


class Execution(models.Model):
    "Execution model"

    machine_id = models.ForeignKey(
        Machine, on_delete=models.deletion.DO_NOTHING, related_name="machine_execution"
    )
    application_id = models.ForeignKey(
        Application,
        on_delete=models.deletion.DO_NOTHING,
        related_name="application_execution",
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
        Execution, on_delete=models.deletion.CASCADE, related_name="execution_id"
    )
