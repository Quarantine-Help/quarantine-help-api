# Create your views here.


# Create your views here.
from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated

from authentication.permissions import (
    IsAffectedUser,
    IsOwnerOfRequest,
    IsAssigneeOfRequest,
)
from authentication.serializer import ParticipantSerializer
from crisis.models import Request
from management.models import Participant
from management.serializer import RequestSerializer, AssigneeRequestUpdateSerializer


class MeRetrieveUpdateAPIViewV1(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ParticipantSerializer
    http_method_names = ["get", "patch", "options"]

    def perform_update(self, serializer):
        validated_data = serializer.validated_data
        user_data_changed = False

        participant_instance = self.get_object()
        user_instance = participant_instance.user

        user_data = validated_data.pop("user", None)

        email_data = user_data.get("email", None)
        if email_data and not email_data == user_instance.email:
            user_instance.email = email_data
            user_data_changed = True
        first_name_data = user_data.get("first_name", None)
        if first_name_data and not first_name_data == user_instance.first_name:
            user_instance.first_name = first_name_data
            user_data_changed = True
        last_name_data = user_data.get("last_name", None)
        if last_name_data and not last_name_data == user_instance.last_name:
            user_instance.last_name = last_name_data
            user_data_changed = True

        if user_data_changed:
            user_instance.save()
            user_instance.refresh_from_db()

        serializer.save(user=user_instance)

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
        return (
            Request.objects.filter(assignee__user=self.request.user)
            .exclude(status=Request.STATUS_CANCELLED)
            .order_by("status")
        )


class MeAssignedRequestViewUpdateAPIV1(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsAssigneeOfRequest]
    serializer_class = RequestSerializer
    assignee_serializer_class = AssigneeRequestUpdateSerializer
    http_method_names = ["get", "options", "patch", "delete"]

    def get_object(self):
        return Request.objects.get(id=self.kwargs.get("pk", None))

    def destroy(self, request, *args, **kwargs):
        request_object: Request = self.get_object()
        request_object.drop_request_from_assignee()
        # Hack to get a full output.
        self.assignee_serializer_class = self.serializer_class
        return self.retrieve(request=request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        super().update(request=request, *args, **kwargs)
        # Hack to get a full output.
        self.assignee_serializer_class = self.serializer_class
        return self.retrieve(request=request, *args, **kwargs)

    def perform_update(self, serializer):
        """
        An update would be to move something in Transit to Completed. Not
        supporting a move back to assigned sadly at this point.
        :param serializer:
        :return:
        """
        assert serializer.validated_data["status"] == Request.STATUS_FINISHED, (
            "You can only change your status " "to finished on this method."
        )
        self.get_object().resolve_request_from_assignee()
        serializer.save()

    def get_serializer_class(self):
        if self.action in ["partial_update", "destroy"]:
            return self.assignee_serializer_class

        return super().get_serializer_class()
