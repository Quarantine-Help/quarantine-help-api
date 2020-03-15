from django.db import models

# Create your models here.
from django.db.models import fields


class Ability(models.Model):
    """
    Define what kind of help a participant can do ? Probably we just keep on
    creating it at the backend and provide them as checkboxes for the
    frontend.
    """

    id = fields.AutoField(primary_key=True)
    title = fields.CharField(verbose_name="Name of ability", max_length=30)
