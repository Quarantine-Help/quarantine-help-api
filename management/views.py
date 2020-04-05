# Create your views here.


# Create your views here.
from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated

from authentication.permissions import IsAffectedUser, IsOwnerOfRequest, IsAssigneeOfRequest
from authentication.serializer import ParticipantSerializer
from crisis.models import Request
from management.models import Participant
from management.serializer import RequestSerializer, AssigneeRequestUpdateSerializer


class MeRetrieveUpdateAPIViewV1(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ParticipantSerializer

    def get_object(self):
        return self.request.user.related_participant


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
        request_object.status = Request.STATUS_CANCELLED
        request_object.save()
        return self.retrieve(request=request, *args, **kwargs)

    def get_object(self):
        return Request.objects.get(id=self.kwargs.get("pk", None))


class MeAssignedRequestsAPIV1(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = RequestSerializer

    def get_queryset(self):
        return Request.objects.filter(assignee__user=self.request.user)


class MeAssignedRequestViewUpdateAPIV1(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsAssigneeOfRequest]
    serializer_class = RequestSerializer
    assignee_serializer_class = AssigneeRequestUpdateSerializer

    def get_object(self):
        return Request.objects.get(id=self.kwargs.get("pk", None))

    def get_serializer_class(self):
        if self.action == 'partial_update':
            return self.assignee_serializer_class

        return super().get_serializer_class()
