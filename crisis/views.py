# Create your views here.
from django.contrib.auth.models import User
from rest_framework import generics

from crisis.helpers import generate_username_with_user_data
from crisis.models import Crisis, Participant
from crisis.serializers import CrisisSerializer, ParticipantSerializer


class CrisisListAPIV1(generics.ListAPIView):
    queryset = Crisis.objects.all()
    serializer_class = CrisisSerializer


class CreateListParticipantsAPIV1(generics.ListCreateAPIView):
    serializer_class = ParticipantSerializer

    def get_queryset(self):
        crisis_id = self.kwargs.get("crisis_id", None)
        return Participant.objects.filter(crisis=crisis_id)

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

        # Now create a particpant.
        validated_data["user"] = user
        validated_data["crisis_id"] = crisis_id
        _ = Participant.objects.create(**validated_data)
        return
