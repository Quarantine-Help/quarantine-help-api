# Create your models here.
from django.core.exceptions import ValidationError
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
    STATUS_PENDING = "P"
    STATUS_TRANSIT = "T"
    STATUS_FINISHED = "F"
    STATUS_CANCELLED = "C"
    UNFINISHED_STATUSES = [STATUS_PENDING, STATUS_TRANSIT]
    FINISHED_STATUSES = [STATUS_FINISHED, STATUS_CANCELLED]
    TYPE_OF_REQUEST_STATUSES = [
        (STATUS_PENDING, "Pending"),
        (STATUS_TRANSIT, "Transit"),
        (STATUS_FINISHED, "Finished"),
        (STATUS_CANCELLED, "Cancelled"),
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

    @property
    def related_request_assignment(self):
        return RequestAssignment.objects.get(assignee=self.assignee, request=self)

    def clean(self):
        if self.status in ["T"] and not self.assignee:
            raise ValidationError("Assignee missing while changing status to assigned.")

    def __str__(self):
        return (
            f"{self.id}-{self.owner.user.first_name}"
            f"-{self.get_type_display()}-deadline-{self.deadline}"
        )

    def assign_user(self, assignee_participant):
        self.status = self.STATUS_TRANSIT
        self.assignee = assignee_participant
        RequestAssignment.objects.create(
            status=RequestAssignment.STATUS_ASSIGNED,
            request=self,
            assignee=assignee_participant,
        )
        # Notify the original dude here ?
        self.save()

    def notify_request_owner_about_assignment(self):
        # @TODO
        pass

    def notify_request_owner_about_assignment_drop(self):
        # @TODO
        pass

    def notify_request_owner_about_assignment_finish(self):
        # @TODO
        pass

    def resolve_request_from_assignee(self, status=STATUS_FINISHED):
        """
        Called when an asignee updates the status of a request. Depending on the
         status, we have to update the related RequestAssignment model too.
        :param status:
        :return:
        """
        related_assignment = self.related_request_assignment

        if status == self.STATUS_FINISHED:
            related_assignment.status = RequestAssignment.STATUS_COMPLETED
            related_assignment.did_complete = True

        related_assignment.save()
        return

    def drop_request_from_assignee(self):
        related_assignment = self.related_request_assignment

        if self.status == Request.STATUS_FINISHED:
            raise Exception("Cannot update this request at this point. Sorry.")
        related_assignment.status = RequestAssignment.STATUS_DROPPED
        related_assignment.save()
        self.status = self.STATUS_PENDING
        self.save()
        self.notify_request_owner_about_assignment_drop()
        return


class RequestAssignment(SafeDeleteModel):
    """
    We will use this to constantly track the progress of an assignment.
    Mostly used for logging, and karma points ?
    """

    _safedelete_policy = SOFT_DELETE_CASCADE

    STATUS_ASSIGNED = "A"
    STATUS_DROPPED = "D"
    STATUS_COMPLETED = "C"

    TYPE_OF_ASSIGNMENT_STATUSES = [
        (STATUS_ASSIGNED, "Assigned"),
        (STATUS_DROPPED, "Dropped"),
        (STATUS_COMPLETED, "Completed"),
    ]
    status = fields.CharField(choices=TYPE_OF_ASSIGNMENT_STATUSES, max_length=2)
    request = models.ForeignKey(
        Request, on_delete=models.CASCADE, related_name="related_assignment"
    )
    assignee = models.ForeignKey(
        "management.Participant",
        on_delete=models.CASCADE,
        related_name="created_assignment",
    )
    created_at = fields.DateTimeField(auto_now_add=True)
    modified_at = fields.DateTimeField(auto_now=True)
    did_complete = fields.BooleanField(default=False)

    def __str__(self):
        return (
            f"{self.id}-{self.assignee.user.first_name}-request-"
            f"{self.request.id}-status-{self.get_status_display()}"
        )
