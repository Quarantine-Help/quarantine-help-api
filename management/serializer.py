from rest_framework import fields, serializers
from rest_framework.serializers import ModelSerializer

from authentication.serializer import UserSerializer
from crisis.models import Request, RequestAssignment
from management.models import Ability


class AbilitySerializer(ModelSerializer):
    class Meta:
        model = Ability
        fields = "__all__"


class RequestAssignmentSerializer(ModelSerializer):
    class Meta:
        model = RequestAssignment
        fields = ("status", "id", "created_at", "did_complete")


class RequestSerializer(ModelSerializer):
    assignee = UserSerializer(
        source="assignee.user", allow_null=True, required=False, read_only=True
    )
    assignmentHistory = RequestAssignmentSerializer(
        source="request_assignee",
        allow_null=True,
        required=False,
        read_only=True,
        many=True,
    )
    status = fields.CharField(required=False, allow_null=True)

    def validate(self, attrs):
        attrs = super().validate(attrs)
        # We do not allow people to set attribute to Transit through the API
        # view. al
        if not self.instance:
            return attrs

        if self.instance.status in Request.FINISHED_STATUSES:
            raise serializers.ValidationError("You cannot change this request anymore.")

        if self.instance.status == "T":
            if attrs["status"] not in ["C", "F"]:
                raise serializers.ValidationError(
                    "You can only cancel or mark the request as finished"
                )
            if attrs["description"] != self.instance.description:
                raise serializers.ValidationError(
                    "You will have to cancel this request first."
                )
            if not attrs["deadline"] >= self.instance.deadline:
                raise serializers.ValidationError(
                    "You cannot shorten the deadline now. Please cancel"
                )

        if attrs["status"] == "T":
            raise serializers.ValidationError("Cannot update the status to T")
        return attrs

    class Meta:
        model = Request
        fields = (
            "id",
            "type",
            "deadline",
            "description",
            "assignee",
            "status",
            "assignmentHistory",
            "created_at",
        )
