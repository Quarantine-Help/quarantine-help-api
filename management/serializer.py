from rest_framework import fields
from rest_framework.serializers import ModelSerializer

from authentication.serializer import UserSerializer
from crisis.models import Request

from management.models import Ability


class AbilitySerializer(ModelSerializer):
    class Meta:
        model = Ability
        fields = "__all__"


class RequestSerializer(ModelSerializer):
    assignee = UserSerializer(source="assignee.user", allow_null=True, required=False)
    status = fields.CharField(required=False, allow_null=True)

    class Meta:
        model = Request
        fields = ("type", "deadline", "description", "assignee", "status")
