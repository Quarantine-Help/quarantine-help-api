# Create your views here.
import coreapi
import coreschema
from rest_framework import generics
from rest_framework.schemas import AutoSchema

from crisis.models import Crisis
from crisis.serializers import CrisisSerializer, AffectedParticipantSerializer
from management.models import Participant


class CrisisListAPIV1(generics.ListAPIView):
    queryset = Crisis.objects.all()
    serializer_class = CrisisSerializer


class ListAffectedParticipantsAPIV1(generics.ListAPIView):
    serializer_class = AffectedParticipantSerializer

    def get_queryset(self):
        crisis_id = self.kwargs.get("crisis_id", None)
        affected_participants = Participant.affected.filter(crisis=crisis_id)
        return affected_participants
