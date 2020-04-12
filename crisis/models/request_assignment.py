from django.db import models
from django.db.models import fields
from safedelete import SOFT_DELETE_CASCADE
from safedelete.models import SafeDeleteModel


class RequestAssignment(SafeDeleteModel):
    """
    We will use this to constantly track the progress of an assignment.
    Mostly used for logging, and karma points ?
    """

    class Meta:
        app_label = 'crisis'
        db_table = 'crisis_requestassignment'

    _safedelete_policy = SOFT_DELETE_CASCADE

    STATUS_ASSIGNED = "A"
    STATUS_DROPPED = "D"
    STATUS_COMPLETED = "C"

    TYPE_OF_ASSIGNMENT_STATUSES = [
        (STATUS_ASSIGNED, "Assigned"),
        (STATUS_DROPPED, "Dropped"),
        (STATUS_COMPLETED, "Completed"),
    ]
    status = fields.CharField(choices=TYPE_OF_ASSIGNMENT_STATUSES,
                              max_length=2)
    request = models.ForeignKey(
        "crisis.Request", on_delete=models.CASCADE,
        related_name="related_assignment"
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
