from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from crisis.models import Request
from management.serializer import RequestSerializer


class ListCreateAffectedParticipantRequestsAPIV1(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = RequestSerializer

    def get_queryset(self):
        participant_id = self.kwargs.get("participant_id", None)
        return Request.objects.filter(
            owner=participant_id, status__in=Request.UNFINISHED_STATUSES
        )
