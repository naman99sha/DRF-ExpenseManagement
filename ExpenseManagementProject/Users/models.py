from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from .managers import CustomUserManager


class User(AbstractUser):
    name = models.CharField(max_length=250)
    email = models.EmailField(max_length=250, unique=True)
    password = models.CharField(max_length=200)
    username = None

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []