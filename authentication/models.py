# Create your models here.
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(unique=True)

    def full_name(self):
        full_name = f'{self.first_name} {self.last_name}'.rstrip()
        return full_name
