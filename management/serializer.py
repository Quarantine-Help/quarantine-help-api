from django.contrib.auth.models import User
from drf_extra_fields import geo_fields
from rest_framework import fields
from rest_framework.serializers import ModelSerializer

from management.models import Ability, Participant


class AbilitySerializer(ModelSerializer):
    class Meta:
        model = Ability
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
