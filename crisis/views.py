# Create your views here.
from django.contrib.auth.models import User
from rest_framework import generics, status
from rest_framework.exceptions import NotFound
from rest_framework.response import Response

from crisis.helpers import generate_username_with_user_data
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

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return self.list(request, *args, **kwargs)

    def perform_create(self, serializer):
        crisis_id = self.kwargs.get("crisis_id", None)
        # First lets create a user.
        validated_data = serializer.validated_data
        user_data = validated_data["user"]
        username = generate_username_with_user_data(user_data=user_data)

        user_data["username"] = username
        user = User.objects.create(**validated_data["user"])
        user.set_unusable_password()
        user.save()

        abilities = validated_data.pop("abilities", [])

        # Now create a particpant.
        validated_data["user"] = user
        validated_data["user_id"] = user.id
        validated_data["crisis_id"] = crisis_id
        participant = Participant.objects.create(**validated_data)
        for abilitiy in abilities:
            participant.abilities.add(abilitiy)
        return

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
