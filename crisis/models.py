# Create your models here.
from django.contrib.auth.models import User
from django.contrib.gis.db.models import PointField
from django.db import models

# Create your models here.
from django.db.models import fields, ManyToManyField
from django_countries.fields import CountryField
from phone_field import PhoneField
from safedelete import HARD_DELETE_NOCASCADE

from management.models import Ability
from safedelete.models import SafeDeleteModel
from safedelete.models import SOFT_DELETE_CASCADE


class Crisis(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE_CASCADE

    id = fields.AutoField(primary_key=True)
    name = fields.CharField(max_length=100)
    active = fields.BooleanField(default=True)
    started_at = fields.DateTimeField()

    def __repr__(self):
        return f"{self.id}-{self.name}"

    def __str__(self):
        return f"{self.id}-{self.name}"


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
    crisis = models.ForeignKey(Crisis, on_delete=models.CASCADE)
    type = fields.CharField(max_length=2, choices=TYPE_OF_PARTICIPANT)

    first_line_of_address = fields.CharField(max_length=255)
    second_line_of_address = fields.CharField(max_length=255)
    country = CountryField(blank_label="(select country)")
    place_id = fields.CharField(verbose_name="Place id from Google", max_length=150)

    position = PointField(null=True, blank=True)
    post_code = fields.CharField(verbose_name="Postal code", max_length=10)
    city = fields.CharField(verbose_name="City", max_length=40)
    phone = PhoneField(blank=True, help_text="Contact phone number")

    created_at = fields.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.id}-{self.crisis.name}-{self.user.first_name}"


class Request(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE_CASCADE

    TYPE_OF_REQUEST = [("G", "Grocery"), ("M", "Medicine")]
    TYPE_OF_REQUEST_STATUSES = [
        ("P", "Pending"),
        ("T", "Transit"),
        ("F", "Finished"),
        ("C", "Cancelled"),
    ]
    owner = models.ForeignKey(
        Participant, related_name="owner", on_delete=models.CASCADE
    )
    assignee = models.ForeignKey(
        Participant, related_name="assignee", null=True, on_delete=models.DO_NOTHING
    )

    status = fields.CharField(choices=TYPE_OF_REQUEST_STATUSES, max_length=2)
    created_at = fields.DateTimeField(auto_now_add=True)
    modified_at = fields.DateTimeField(auto_now=True)
    type = models.CharField(choices=TYPE_OF_REQUEST, max_length=2)
    deadline = models.DateTimeField(null=True)
    description = models.TextField()

    def __str__(self):
        return f"{self.id}-{self.owner.first_name}-{self.get_type_display()}-deadline-{self.deadline}"


class RequestAssignment(SafeDeleteModel):
    """
    We will use this to constantly track the progress of an assignment.
    Mostly used for logging, and karma points ?
    """

    _safedelete_policy = SOFT_DELETE_CASCADE

    TYPE_OF_ASSIGNMENT_STATUSES = [
        ("A", "Assigned"),
        ("D", "Dropped"),
        ("C", "Completed"),
    ]
    status = fields.CharField(choices=TYPE_OF_ASSIGNMENT_STATUSES, max_length=2)
    request = models.ForeignKey(Request, on_delete=models.CASCADE)
    assignee = models.ForeignKey(Participant, on_delete=models.CASCADE)

    assigned_at = models.DateTimeField(auto_created=True)
    modified_at = fields.DateTimeField(auto_now=True)
    did_complete = fields.BooleanField(default=False)

    def __str__(self):
        return (
            f"{self.id}-{self.assignee.first_name}-request-"
            f"{self.request.id}-status-{self.get_status_display()}"
        )
