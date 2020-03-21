from django.contrib.auth.models import User
from django.db import models
from drf_extra_fields import geo_fields
from rest_framework.serializers import ModelSerializer

from crisis.models import Crisis, Participant
from management.serializer import AbilitySerializer


class CrisisSerializer(ModelSerializer):
    class Meta:
        model = Crisis
        fields = "__all__"


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "email")


class ParticipantSerializer(ModelSerializer):
    user = UserSerializer()
    position = geo_fields.PointField(str_points=True)

    class Meta:
        model = Participant
        fields = "__all__"
