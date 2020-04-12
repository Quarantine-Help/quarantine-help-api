from django.db.models import fields
from safedelete import SOFT_DELETE_CASCADE
from safedelete.models import SafeDeleteModel


class Crisis(SafeDeleteModel):
    class Meta:
        app_label = 'crisis'
        db_table = 'crisis_crisis'

    _safedelete_policy = SOFT_DELETE_CASCADE

    id = fields.AutoField(primary_key=True)
    name = fields.CharField(max_length=100)
    active = fields.BooleanField(default=True)
    started_at = fields.DateTimeField()

    def __repr__(self):
        return f"{self.id}-{self.name}"

    def __str__(self):
        return f"{self.id}-{self.name}"
