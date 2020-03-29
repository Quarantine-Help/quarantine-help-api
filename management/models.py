from django.conf import settings
from django.contrib.gis.db.models import PointField
from django.db import models

# Create your models here.
from django.db.models import fields, manager
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_countries.fields import CountryField
from phone_field import PhoneField
from rest_framework.authtoken.models import Token
from safedelete import HARD_DELETE_NOCASCADE
from safedelete.models import SafeDeleteModel

from authentication.models import User
from crisis.models import Crisis


class Ability(models.Model):
    """
    Define what kind of help a participant can do ? Probably we just keep on
    creating it at the backend and provide them as checkboxes for the
    frontend.
    """

    TYPE_OF_VERBS = [
        ("F", "Fetch"),
        ("P", "Provide"),
        ("T", "Transport"),
        ("N", "Notify"),
    ]
    id = fields.AutoField(primary_key=True)
    title = fields.CharField(verbose_name="Name of ability", max_length=30)
    verb = fields.CharField(
        verbose_name="Action on the title, (eg, GET)",
        default="F",
        max_length=3,
        choices=TYPE_OF_VERBS,
    )

    def __str__(self):
        return f"{self.get_verb_display()}-{self.title}"


class AffectedParticipantManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(type="AF")


class HelperParticipantManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(type="HL")


class Participant(SafeDeleteModel):
    _safedelete_policy = HARD_DELETE_NOCASCADE
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
    type = fields.CharField(max_length=2, choices=TYPE_OF_PARTICIPANT)
    crisis = models.ForeignKey(Crisis, on_delete=models.DO_NOTHING)
    first_line_of_address = fields.CharField(max_length=255)
    second_line_of_address = fields.CharField(max_length=255)
    country = CountryField(blank_label="(select country)")
    place_id = fields.CharField(verbose_name="Place id from Google", max_length=150)

    position = PointField(null=True, blank=True)
    post_code = fields.CharField(verbose_name="Postal code", max_length=10)
    city = fields.CharField(verbose_name="City", max_length=40)
    phone = PhoneField(blank=True, help_text="Contact phone number")

    objects = manager.Manager()
    helpers = HelperParticipantManager()
    affected = AffectedParticipantManager()

    created_at = fields.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.id}-{self.user.first_name}-({self.get_type_display()})"


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
