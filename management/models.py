from django.db import models

# Create your models here.
from django.db.models import fields


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
