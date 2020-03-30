# Create your models here.
from django.db import models

# Create your models here.
from django.db.models import fields
from safedelete.models import SOFT_DELETE_CASCADE
from safedelete.models import SafeDeleteModel

from authentication.models import User


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


class Request(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE_CASCADE

    TYPE_OF_REQUEST = [("G", "Grocery"), ("M", "Medicine")]
    UNFINISHED_STATUSES = ["P", "T"]
    TYPE_OF_REQUEST_STATUSES = [
        ("P", "Pending"),
        ("T", "Transit"),
        ("F", "Finished"),
        ("C", "Cancelled"),
    ]
    owner = models.ForeignKey(
        "management.Participant",
        related_name="created_request",
        on_delete=models.CASCADE,
    )
    assignee = models.ForeignKey(
        "management.Participant",
        related_name="assigned_request",
        null=True,
        blank=True,
        on_delete=models.DO_NOTHING,
    )

    status = fields.CharField(choices=TYPE_OF_REQUEST_STATUSES, max_length=2)
    created_at = fields.DateTimeField(auto_now_add=True)
    modified_at = fields.DateTimeField(auto_now=True)
    type = models.CharField(choices=TYPE_OF_REQUEST, max_length=2)
    deadline = models.DateTimeField(null=True)
    description = models.TextField()

    def __str__(self):
        return (
            f"{self.id}-{self.owner.user.first_name}"
            f"-{self.get_type_display()}-deadline-{self.deadline}"
        )


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
    assignee = models.ForeignKey(
        "management.Participant", on_delete=models.CASCADE, related_name="assignment"
    )

    assigned_at = models.DateTimeField(auto_created=True)
    modified_at = fields.DateTimeField(auto_now=True)
    did_complete = fields.BooleanField(default=False)

    def __str__(self):
        return (
            f"{self.id}-{self.assignee.first_name}-request-"
            f"{self.request.id}-status-{self.get_status_display()}"
        )
