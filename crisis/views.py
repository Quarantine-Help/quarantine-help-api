# Create your views here.

from rest_framework import generics
from rest_framework.exceptions import NotFound
from rest_framework.response import Response

from crisis.models import Crisis, Participant
from crisis.serializers import CrisisSerializer, ParticipantSerializer
from management.models import Ability
from management.serializer import AbilitySerializer


class CrisisListAPIV1(generics.ListAPIView):
    queryset = Crisis.objects.all()
    serializer_class = CrisisSerializer


class CreateListParticipantsAPIV1(generics.ListCreateAPIView):
    serializer_class = ParticipantSerializer

    def get_queryset(self):
        crisis_id = self.kwargs.get("crisis_id", None)
        return Participant.objects.filter(crisis=crisis_id)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)

        picked_fk_maps = queryset.values("crisis", "abilities")
        crisis_ids = set()
        abilities_ids = set()

        for picked_fk_map in list(picked_fk_maps):
            crisis_ids.add(picked_fk_map["crisis"])
            abilities_ids.add(picked_fk_map["abilities"])

        serializer = self.get_serializer(page, many=True)
        crises_query_set = Crisis.objects.filter(pk__in=list(crisis_ids))
        crisis_data = CrisisSerializer(crises_query_set, many=True)

        abilities_query_set = Ability.objects.filter(pk__in=list(abilities_ids))
        abilities_data = AbilitySerializer(abilities_query_set, many=True)

        paginated_response = self.get_paginated_response(
            {"participants": serializer.data}
        )
        list_data = paginated_response
        list_data.data["results"]["crises"] = crisis_data.data
        list_data.data["results"]["abilities"] = abilities_data.data
        return Response(list_data.data)
