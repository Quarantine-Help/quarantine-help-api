# Create your views here.


# Create your views here.
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from authentication.permissions import IsAffectedUser, IsOwnerOfRequest
from authentication.serializer import ParticipantSerializer
from crisis.models import Request
from management.models import Participant
from management.serializer import RequestSerializer


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
        request_object.status = "C"
        request_object.save()
        return self.retrieve(request=request, *args, **kwargs)

    def get_object(self):
        return Request.objects.get(id=self.kwargs.get("pk", None))
