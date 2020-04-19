from rest_framework.serializers import ModelSerializer

from authentication.serializer import (
    ParticipantSerializer,
    ParticipantAnonymizedSerializer,
)
from crisis.models.crisis import Crisis
from management.serializer import RequestSerializer, RequestAnonymizedSerializer


class CrisisSerializer(ModelSerializer):
    class Meta:
        model = Crisis
        fields = "__all__"


class AffectedParticipantSerializer(ParticipantSerializer):
    requests = RequestSerializer(many=True, source="created_request")

    class Meta(ParticipantSerializer.Meta):
        fields = ParticipantSerializer.Meta.fields + ("requests",)


class AffectedParticipantAnonymizedSerializer(ParticipantAnonymizedSerializer):
    requests = RequestAnonymizedSerializer(many=True, source="created_request")

    class Meta(ParticipantSerializer.Meta):
        fields = ParticipantSerializer.Meta.fields + ("requests",)
