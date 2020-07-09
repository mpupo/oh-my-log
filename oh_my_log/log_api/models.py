from django.db import models
from django.core import validators
# Create your models here.
class User(models.Model):
    "User model"
    name = models.CharField('Name', max_length=50)
    email = models.EmailField('E-mail', max_length=254, validators=[validators.EmailValidator()])
    password = models.CharField('Password', max_length=50, validators=[validators.MinLengthValidator(8)])
    last_login = models.DateTimeField('Last login', auto_now_add=True)

class Group(models.Model):
    pass

class Machine(models.Model):
    pass

class Application(models.Model):
    pass

class Event(models.Model):
    pass

class Execution(models.Model)
    pass

