from django.urls import path

from crisis.views.af_crisis_participant_views import \
    ListCreateAffectedParticipantRequestsAPIV1
from crisis.views.common_views import CrisisListAPIV1, \
    ListAffectedParticipantsAPIV1
from crisis.views.hl_crisis_participant_views import AssignRequestAsHLAPIView

urlpatterns = [
    path("", CrisisListAPIV1.as_view(), name="list_crisies"),
    path(
        "<int:crisis_id>/affected-participants/",
        ListAffectedParticipantsAPIV1.as_view(),
        name="list_affected_participants",
    ),
    path(
        "<int:crisis_id>/affected-participants/<int:participant_id>/requests/",
        ListCreateAffectedParticipantRequestsAPIV1.as_view(),
        name="list_create_requests",
    ),
    path(
        "<int:crisis_id>/affected-participants/<int:participant_id>/requests"
        "/<int:request_id>/assign/",
        AssignRequestAsHLAPIView.as_view(),
        name="assign_request_as_hl",
    ),
]
