from rest_framework.serializers import ModelSerializer

from crisis.models.crisis import Crisis

from authentication.serializer import ParticipantSerializer
from management.serializer import RequestSerializer


class CrisisSerializer(ModelSerializer):
    class Meta:
        model = Crisis
        fields = "__all__"


class AffectedParticipantSerializer(ParticipantSerializer):
    requests = RequestSerializer(many=True, source="created_request")

    class Meta(ParticipantSerializer.Meta):
        fields = ParticipantSerializer.Meta.fields + ("requests",)
