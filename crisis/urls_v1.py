from django.conf.urls import url
from django.urls import path

from crisis.views import CrisisListAPIV1, ListAffectedParticipantsAPIV1

urlpatterns = [
    url(r"^$", CrisisListAPIV1.as_view(), name="list_crisies"),
    path(
        "<int:crisis_id>/affected-participants/",
        ListAffectedParticipantsAPIV1.as_view(),
        name="list_affected_participants",
    ),
]
