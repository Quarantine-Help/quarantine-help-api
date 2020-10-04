from django.urls import path

from authentication.views import (
    EmailAuthToken,
    CreateParticipantsAPIV1,
    CreateParticipantsBulkAPIV1,
)

urlpatterns = [
    path(
        "register/", CreateParticipantsAPIV1.as_view(), name="create_list_participants"
    ),
    path(
        "bulk-register/",
        CreateParticipantsBulkAPIV1.as_view(),
        name="create_bulk_participants",
    ),
    path("login/", EmailAuthToken.as_view(), name="login_participant"),
]
