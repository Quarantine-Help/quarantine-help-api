from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.db.models import fields, ManyToManyField
from django_countries.fields import CountryField
from phone_field import PhoneField

from crisis.models import Ability


class Participant(models.Model):
    TYPE_OF_PARTICIPANT = [
        ("HL", "Helper"),
        ("AF", "Affected"),
        ("AU", "Authorities"),
        ("TP", "Third Parties"),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    type = fields.CharField(max_length=2, choices=TYPE_OF_PARTICIPANT)
    birth_date = fields.DateField()

    first_line_of_address = fields.CharField(max_length=255)
    second_line_of_address = fields.CharField(max_length=255)
    country = CountryField(blank_label="(select country)")
    place_id = fields.CharField(verbose_name="Place id from Google", max_length=150)
    latitude = fields.CharField(verbose_name="Latitude of the user", max_length=15)
    longitude = fields.CharField(verbose_name="Longitude of the user", max_length=15)
    post_code = fields.CharField(verbose_name="Postal code", max_length=10)
    city = fields.CharField(verbose_name="City", max_length=40)
    phone = PhoneField(blank=True, help_text="Contact phone number")
    abilities = ManyToManyField(Ability)
    is_available = fields.BooleanField(default=True)
