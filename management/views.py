# Create your views here.


# Create your views here.
from rest_framework import generics

from authentication.permissions import IsAffectedUser
from crisis.models import Request
from management.models import Participant
from management.serializer import RequestSerializer


class ListCreateRequestsAPIV1(generics.ListCreateAPIView):
    permission_classes = [IsAffectedUser]
    serializer_class = RequestSerializer

    def get_queryset(self):
        return Request.objects.filter(owner__user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(
            owner=Participant.affected.get(user=self.request.user),
            status=Request.STATUS_PENDING,
        )
