# Create your models here.
from django.contrib.auth.models import User
from django.contrib.gis.db.models import PointField
from django.db import models

# Create your models here.
from django.db.models import fields, ManyToManyField
from django_countries.fields import CountryField
from phone_field import PhoneField

from management.models import Ability


class Crisis(models.Model):
    id = fields.AutoField(primary_key=True)
    name = fields.CharField(max_length=100)
    active = fields.BooleanField(default=True)
    started_at = fields.DateTimeField()

    def __repr__(self):
        return f"{self.id}-{self.name}"

    def __str__(self):
        return f"{self.id}-{self.name}"


class Participant(models.Model):
    """
    This is a participant for a crisis
    """

    TYPE_OF_PARTICIPANT = [
        ("HL", "Helper"),
        ("AF", "Affected"),
        ("AU", "Authorities"),
        ("TP", "Third Parties"),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    crisis = models.OneToOneField(Crisis, on_delete=models.CASCADE)
    type = fields.CharField(max_length=2, choices=TYPE_OF_PARTICIPANT)

    first_line_of_address = fields.CharField(max_length=255)
    second_line_of_address = fields.CharField(max_length=255)
    country = CountryField(blank_label="(select country)")
    place_id = fields.CharField(verbose_name="Place id from Google", max_length=150)

    position = PointField(null=True, blank=True)
    post_code = fields.CharField(verbose_name="Postal code", max_length=10)
    city = fields.CharField(verbose_name="City", max_length=40)
    phone = PhoneField(blank=True, help_text="Contact phone number")
    abilities = ManyToManyField(Ability)
    is_available = fields.BooleanField(default=True)
    created_at = fields.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.id}-{self.crisis.name}-{self.user.first_name}"
