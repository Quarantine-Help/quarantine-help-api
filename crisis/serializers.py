from rest_framework.serializers import ModelSerializer

from crisis.models import Crisis, Request
from management.serializer import UserSerializer, ParticipantSerializer


class CrisisSerializer(ModelSerializer):
    class Meta:
        model = Crisis
        fields = "__all__"


class RequestSerializer(ModelSerializer):
    assignee = UserSerializer(source="assignee.user", allow_null=True)

    class Meta:
        model = Request
        fields = ("type", "deadline", "description", "assignee", "status")


class AffectedParticipantSerializer(ParticipantSerializer):
    requests = RequestSerializer(many=True, source="created_request")
