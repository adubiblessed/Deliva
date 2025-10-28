from django.db import models
import uuid
from enum import Enum

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _  # for translation


# Enum is used to define user roles instead of hardcoding strings
class Role (Enum):
    ADMIN = "ADMIN"
    USER = "USER"
    COURIER = "COURIER"
    RESTAURANT_OWNER = "RESTAURANT_OWNER"

class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    role = models.CharField(max_length=20, choices=[(role.value, role.value) for role in Role], default=Role.USER.value)
    phone_no = models.CharField(null=True, blank=True)
    email = models.EmailField(unique=True, verbose_name='email address', help_text=_('Required. Enter a valid email address.'))
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [
        "first_name",
        "last_name",
        "username",
    ]
    def __str__(self):
        return "{}".format(self.email)




