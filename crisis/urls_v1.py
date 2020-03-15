from django.conf.urls import url
from django.urls import include, path

from crisis.views import CrisisListAPIV1, CreateListParticipantsAPIV1

urlpatterns = [
    url(r"^$", CrisisListAPIV1.as_view(), name="list_crisies"),
    path(
        "<int:crisis_id>/participants/",
        CreateListParticipantsAPIV1.as_view(),
        name="create_list_participants",
    ),
]
