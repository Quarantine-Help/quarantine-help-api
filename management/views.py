from authentication.models import User
from django.shortcuts import render

# Create your views here.
from rest_framework import generics

from crisis.helpers import generate_username_with_user_data
from management.serializer import ParticipantSerializer
from management.models import Participant


class CreateParticipantsAPIV1(generics.CreateAPIView):
    serializer_class = ParticipantSerializer

    def get_queryset(self):
        crisis_id = self.kwargs.get("crisis_id", None)
        return Participant.objects.filter(crisis=crisis_id)

    def perform_create(self, serializer):
        validated_data = serializer.validated_data
        user_data = validated_data["user"]
        username = generate_username_with_user_data(user_data=user_data)

        user_data["username"] = username
        user = User.objects.create(**validated_data["user"])
        user.set_unusable_password()
        user.save()

        # Now create a particpant.
        validated_data["user"] = user
        _ = Participant.objects.create(**validated_data)
        return
