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
        fields = ("status", "id", "assigned_at", "did_complete")


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
        if self.instance.status in Request.FINISHED_STATUSES:
            raise serializers.ValidationError("You cannot change this " "anymore.")

        if attrs["status"] == "T":
            raise serializers.ValidationError("Cannot update the status to T")
        # Also, once someone started working on a task, you cannot change
        # stuff. You can only cancel
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
        )
