from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from django.db.models.signals import post_save

from app.models import BaseModel


class User(AbstractUser):
    birthday = models.DateField(null=True)
    phone_number = PhoneNumberField(null=True, blank=True)
    more_informations = models.CharField(null=True, blank=True, max_length=255)

