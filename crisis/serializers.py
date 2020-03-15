from rest_framework.serializers import ModelSerializer

from crisis.models import Crisis, Participant


class CrisisSerializer(ModelSerializer):
    class Meta:
        model = Crisis
        fields = "__all__"


class ParticipantSerializer(ModelSerializer):
    class Meta:
        model = Participant
        fields = "__all__"
