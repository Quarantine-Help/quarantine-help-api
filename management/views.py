# Create your views here.


# Create your views here.
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from authentication.permissions import IsAffectedUser, IsOwnerOfRequest
from crisis.models import Request
from management.models import Participant
from management.serializer import RequestSerializer


class ListCreateRequestsAPIV1(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, IsAffectedUser]
    serializer_class = RequestSerializer

    def get_queryset(self):
        return Request.objects.filter(owner__user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(
            owner=Participant.affected.get(user=self.request.user),
            status=Request.STATUS_PENDING,
        )


class MeRequestDetailAPIV1(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, IsAffectedUser, IsOwnerOfRequest]
    serializer_class = RequestSerializer

    def destroy(self, request, *args, **kwargs):
        request_object = self.get_object()
        request_object.status = "C"
        request_object.save()
        return self.retrieve(request=request, *args, **kwargs)

    def get_object(self):
        return Request.objects.get(id=self.kwargs.get("pk", None))
