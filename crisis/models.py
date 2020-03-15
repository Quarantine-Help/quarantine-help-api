from django.db import models

# Create your models here.
from django.db.models import fields


class Crisis(models.Model):
    id = fields.AutoField(primary_key=True)
    name = fields.CharField(max_length=100)
    active = fields.BooleanField(default=True)
    started_at = fields.DateTimeField()


class Ability(models.Model):
    """
    Define what kind of help a participant can do ? Probably we just keep on
    creating it at the backend and provide them as checkboxes for the
    frontend.
    """

    id = fields.AutoField(primary_key=True)
    title = fields.CharField(verbose_name="Name of ability", max_length=30)
