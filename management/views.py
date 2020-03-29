# Create your views here.
import coreapi
import coreschema
from rest_framework import generics
from rest_framework.schemas import AutoSchema

from authentication.models import User
from crisis.helpers import generate_username_with_user_data
from management.models import Participant
from management.schemas import ParticipantCreateSchema
from management.serializer import ParticipantSerializer


# Create your views here.


class CreateParticipantsAPIV1(generics.CreateAPIView):
    serializer_class = ParticipantSerializer
    schema = ParticipantCreateSchema()

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

        # Now create a participant.
        validated_data["user"] = user
        _ = Participant.objects.create(**validated_data)
        return
