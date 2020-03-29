# Create your models here.
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(unique=True)
